"""Exercise real purchase/buff/UI Lua without assuming native modifier expiry."""
from pathlib import Path
import xml.etree.ElementTree as ET
from lupa import LuaRuntime

root=Path(__file__).resolve().parents[1]/'assets/scar/christmas'
lua=LuaRuntime()
lua.execute('Core_RegisterModule=function() end; import=function() end')
for name in ('yuletide.scar','yuletide_shop.scar','yuletide_buffs.scar'):
    lua.execute((root/name).read_text(encoding='utf-8-sig'))
lua.execute('''
MAT_EntityType=1; MUT_Multiplication=2; AGS_BP_VILLAGER='villager'; R_ENEMY=1
players={{id=22,slot=1},{id=11,slot=5},{id=33,slot=8,isEliminated=true}}
World_GetPlayerCount=function() return #players end
World_GetPlayerAt=function(i) return players[i].id end
Core_GetPlayersTableEntryFromIndex=function(i) return players[i] end
Player_GetSlotIndex=function(id)
    for _,p in ipairs(players) do if p.id==id then return p.slot end end
    error('Unexpected player')
end
Player_GetDisplayName=function(id) return {LocString='Player '..id} end
localPlayer=11; Game_GetLocalPlayer=function() return localPlayer end
age=1; Player_GetCurrentAge=function() return age end
AGS_IsMutualRelation=function() return false end
Yule_CanReceiveVillagers=function() return false end
now=10.25; World_GetGameTime=function() return now end
blueprintQueries=0
BP_GetEntityBlueprintsWithType=function(kind)
    assert(kind=='villager', 'Must not include worker/trader/cart/fishing-boat types')
    blueprintQueries=blueprintQueries+1
    return {{PropertyBagGroupID=202},{PropertyBagGroupID=101},{PropertyBagGroupID=101}}
end
nextID=0; active={}; removed={}; applicationOrder={}; attempts=0; failAfter=nil
Modifier_Create=function(scope,name,usage,exclusive,value,bp)
    assert(scope==MAT_EntityType and usage==MUT_Multiplication and exclusive==false)
    assert(bp.PropertyBagGroupID==101 or bp.PropertyBagGroupID==202)
    if name=='speed_maximum_modifier' then assert(value==1.3)
    else
        assert(name=='resource_entity_harvest_rate_food' or name=='resource_entity_harvest_rate_wood'
            or name=='resource_entity_harvest_rate_gold' or name=='resource_entity_harvest_rate_stone')
        assert(value==1.5)
    end
    return {name=name,value=value,bp=bp.PropertyBagGroupID}
end
Modifier_ApplyToPlayer=function(mod,player,duration)
    assert(duration==0, 'Script owns expiry; avoid native expiry/removal races')
    attempts=attempts+1
    if failAfter and attempts>failAfter then return nil end
    nextID=nextID+1; mod.player=player
    active[nextID]=mod; table.insert(applicationOrder,mod.bp)
    return nextID
end
Modifier_Remove=function(ids)
    for _,id in ipairs(ids) do
        assert(active[id]~=nil, 'Must not remove already removed or unrelated modifiers')
        active[id]=nil; removed[id]=true
    end
end
timers={}
Rule_AddOneShot=function(callback,delay,data)
    table.insert(timers,{callback=callback,at=now+delay,data=data})
end
local function runTimers()
    for i=#timers,1,-1 do
        if timers[i].at<=now then
            local timer=table.remove(timers,i)
            timer.callback({},timer.data)
        end
    end
end
-- Effects remain until explicitly removed, including on future units.
local function effective(player,bp,name,base)
    local value=base or 1
    for _,mod in pairs(active) do
        if mod.player==player and mod.bp==bp and mod.name==name then value=value*mod.value end
    end
    return value
end
local function reset()
    YULE={running=true,time=0,wallets={[5]=3,[1]=3},raids={1,2,3,4,5,6,7,8},presents={}}
    active={}; removed={}; applicationOrder={}; attempts=0; failAfter=nil; timers={}
    YULE_RAIDS_VERIFIED=false; players[1].isEliminated=false
end
reset()
-- No enemy selection, town centre, or raid capacity is needed for a buff.
assert(Yule_PurchaseNetwork(11,'cheer:0'))
assert(YULE.wallets[5]==2 and YULE.wallets[1]==3)
assert(Yule_CheerSecondsRemaining(11)==30 and Yule_CheerSecondsRemaining(22)==0)
assert(YULE.cheers[5].expires==40.25 and blueprintQueries==1)
assert(#applicationOrder==10 and applicationOrder[1]==101 and applicationOrder[6]==202)
for _,bp in ipairs({101,202}) do
    assert(effective(11,bp,'speed_maximum_modifier')==1.3)
    for _,resource in ipairs({'food','wood','gold','stone'}) do
        assert(effective(11,bp,'resource_entity_harvest_rate_'..resource)==1.5)
    end
end
assert(effective(22,101,'speed_maximum_modifier')==1) -- another player
assert(effective(11,999,'speed_maximum_modifier')==1) -- a non-villager
assert(effective(11,101,'health_maximum_modifier')==1)
assert(effective(11,101,'resource_entity_harvest_rate_gold',2)==3) -- existing eco boost
now=20.75
assert(Yule_CheerSecondsRemaining(11)==20)
-- A newly created villager of either blueprint sees the same player modifier.
local newVillager={owner=11,blueprint=202}
assert(effective(newVillager.owner,newVillager.blueprint,'speed_maximum_modifier')==1.3)

-- Refresh buys a fresh 30 seconds, never 1.3^2 or 1.5^2.
local oldIDs=YULE.cheers[5].modifiers
assert(Yule_PurchaseNetwork(11,'cheer:0') and YULE.wallets[5]==1)
assert(Yule_CheerSecondsRemaining(11)==30 and YULE.cheers[5].expires==50.75)
assert(blueprintQueries==1)
for _,id in ipairs(oldIDs) do assert(removed[id]) end
assert(effective(11,101,'speed_maximum_modifier')==1.3)
assert(effective(11,101,'resource_entity_harvest_rate_gold')==1.5)
-- Failed partial refresh refunds its token and preserves the previous buff.
attempts=0; failAfter=2
assert(not Yule_PurchaseNetwork(11,'cheer:0') and YULE.wallets[5]==1)
assert(YULE.cheers[5].expires==50.75)
assert(effective(11,101,'speed_maximum_modifier')==1.3)
assert(effective(11,101,'resource_entity_harvest_rate_food')==1.5)
failAfter=nil
now=40.25; runTimers() -- original purchase deadline cannot cancel the refresh
assert(effective(11,101,'speed_maximum_modifier')==1.3)
now=50.74; assert(Yule_CheerSecondsRemaining(11)==1)
runTimers(); assert(effective(11,101,'speed_maximum_modifier')==1.3)
now=50.75
assert(Yule_CheerSecondsRemaining(11)==0)
runTimers()
assert(effective(11,101,'speed_maximum_modifier')==1)
assert(effective(11,101,'resource_entity_harvest_rate_gold',2)==2)
Yule_UpdateCheer(Yule_LivePlayers()); assert(YULE.cheers[5]==nil)
assert(next(active)==nil)
-- The periodic simulation tick also cleans up if a one-shot is unavailable
-- after restore; elapsed UI time alone must never discard active modifiers.
YULE.wallets[5]=1; assert(Yule_PurchaseNetwork(11,'cheer:0'))
now=now+31
Yule_UpdateCheer(Yule_LivePlayers())
assert(next(active)==nil and YULE.cheers[5]==nil)
runTimers(); assert(next(active)==nil) -- no double removal from stale timers

-- It works in every age, stays personal, and does not depend on UI state.
for tier=1,4 do
    reset(); age=tier
    assert(Yule_PurchaseNetwork(11,'cheer:0'))
    assert(YULE.wallets[5]==2 and effective(11,101,'speed_maximum_modifier')==1.3)
    assert(effective(22,101,'speed_maximum_modifier')==1)
end
assert(not Yule_PurchaseNetwork(99,'cheer:0'))
assert(not Yule_PurchaseNetwork(33,'cheer:0')) -- eliminated
assert(not Yule_PurchaseNetwork(11,'cheer:-1'))
assert(not Yule_PurchaseNetwork(11,'cheer:0junk'))
YULE.wallets[5]=0; assert(not Yule_PurchaseNetwork(11,'cheer:0'))
YULE.wallets[5]=2; YULE.running=false
assert(not Yule_PurchaseNetwork(11,'cheer:0')); YULE.running=true

-- Each player has independent effects and timers; defeat removes only theirs.
assert(Yule_PurchaseNetwork(22,'cheer:0'))
assert(effective(22,101,'speed_maximum_modifier')==1.3)
players[1].isEliminated=true; Yule_UpdateCheer(Yule_LivePlayers())
assert(YULE.cheers[1]==nil and effective(22,101,'speed_maximum_modifier')==1)
assert(effective(11,101,'speed_maximum_modifier')==1.3)

-- Actual menu shows all three tabs and a buyer-specific countdown.
UI_IsReplay=function() return false end
UI_CreateCommand=function(name) return name end
UI_CreateDataContext=function(data) return data end
UI_AddChild=function(a,b,c,data) capturedXaml=data.Xaml end
UI_SetDataContext=function(name,data) context=data end
YULE_SHOP_UI.created=false; Yule_CreateShop(); Yule_ShopSelectTab('buffs')
assert(context.buffsVisible=='Visible' and context.suppliesVisible=='Collapsed' and context.raidsVisible=='Collapsed')
assert(context.enabled.cheer and not context.enabled.pikes4)
assert(context.cheerStatus=='Active: 30s. Buy again to refresh.')
now=now+12.2; Yule_RefreshShop(); assert(context.cheerStatus=='Active: 18s. Buy again to refresh.')
Yule_RefreshShop(); assert(context.cheerStatus=='Active: 18s. Buy again to refresh.') -- pause
localPlayer=22; Yule_RefreshShop(); assert(not context.enabled.cheer)
assert(context.cheerStatus=='Lasts 30 seconds. Applies to your villagers.')
localPlayer=11
Yule_ShopSelectTab('supplies'); assert(context.buffsVisible=='Collapsed')

-- Game-over cleanup removes only this feature's still-live modifiers.
Rule_Remove=function() end; Yule_EndVisit=function() end; YULE.raids={}
Yule_OnGameOver(); assert(next(YULE.cheers)==nil and not YULE.running)
now=now+40; runTimers(); assert(next(active)==nil)
assert(effective(11,101,'speed_maximum_modifier')==1)
assert(effective(11,101,'resource_entity_harvest_rate_gold',2)==2)
reset(); YULE.cheerBlueprints={}
assert(not Yule_PurchaseNetwork(11,'cheer:0') and YULE.wallets[5]==3)
''')
xaml=ET.fromstring(lua.globals().capturedXaml)
ns='{http://schemas.microsoft.com/winfx/2006/xaml/presentation}'
buttons=xaml.findall('.//'+ns+'Button')
assert len([b for b in buttons if b.get('CommandParameter')=='buffs'])==1
cheer=[b for b in buttons if b.get('CommandParameter')=='cheer']
assert len(cheer)==1 and cheer[0].get('Content')=='Festive Cheer'
assert xaml.find('.//'+ns+'UniformGrid').get('Columns')=='3'
print('PASS: 30-second timed villager-only buff, correct 1.3/1.5 effects, one-token personal purchase in all ages, refresh without stacking, expiry/refund/defeat cleanup and Buffs-tab countdown.')
