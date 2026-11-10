"""Run with Python + lupa; exercise the shipped Lua reward and shop functions."""
from pathlib import Path
from lupa import LuaRuntime

lua = LuaRuntime()
lua.execute('Core_RegisterModule=function() end; import=function() end')
root = Path(__file__).resolve().parents[1] / 'assets/scar/christmas'
for filename in ('yuletide.scar', 'yuletide_shop.scar'):
    lua.execute((root / filename).read_text())

lua.execute('''
RT_Gold=1; RT_Food=2; RT_Wood=3; RT_Stone=4; R_ENEMY=1
-- Internal order deliberately disagrees with lobby slots, including gaps.
players={{id=11,slot=5},{id=22,slot=8},{id=33,slot=2},
         {id=44,slot=1},{id=55,slot=4,isEliminated=true}}
World_GetPlayerCount=function() return #players end
World_GetPlayerAt=function(i) return players[i].id end
Core_GetPlayersTableEntryFromIndex=function(i) return players[i] end
Player_GetSlotIndex=function(id)
    for _,p in ipairs(players) do if p.id==id then return p.slot end end
    error('Unknown player')
end
AGS_IsMutualRelation=function(a,b) return a==11 and (b==22 or b==33 or b==55) end
Player_GetCurrentAge=function() return 1 end
Game_GetLocalPlayer=function() return 11 end
Yule_CanReceiveVillagers=function() return true end
UI_SetDataContext=function(name,data) context=data end
Network_CallEvent=function(name,message) networkMessage=message end
Yule_Notify=function() end
paid={}; deposits={}; deployed={}
Player_AddResource=function(id,resource,n) paid[id]=(paid[id] or 0)+n end
BP_GetEntityBlueprint=function(name) return name end
Entity_CreateENVFacing=function(name,position)
    deposits[name]=(deposits[name] or 0)+1
    return {name=name,position=position}
end
World_GetSpawnablePosition=function(position) return position end
Entity_Spawn=function() end; Entity_WarpToPos=function() end
Yule_DeployPurchasedRaid=function(buyer,target,offer)
    assert(buyer.id==11 and offer.tier==1)
    deployed[#deployed+1]=target.id
    return true
end

-- Exhaust every possible roll: exact proportions and correct reward effects.
local counts={0,0,0,0}
local rngCalls=0
for roll=1,100 do
    World_GetRand=function(a,b) assert(a==1 and b==100); rngCalls=rngCalls+1; return roll end
    local outcome=Yule_RollPresentOutcome()
    counts[outcome]=counts[outcome]+1
    Yule_Reward(players[1],{x=0,y=0,z=0},outcome,Yule_LivePlayers())
end
assert(rngCalls==100)
assert(counts[1]==40 and counts[2]==40 and counts[3]==10 and counts[4]==10)
assert(paid[11]==12000 and paid[22]==6000 and paid[33]==6000)
assert(paid[44]==nil and paid[55]==nil)
assert(deposits.resource_gold_deposit_small==10 and deposits.resource_stone_deposit_small==10)
assert(YULE_CONFIG.goldenChance==20)

-- UI, request payload, receiver and wallet must all agree on the lobby slot.
YULE={running=true,time=0,nextVisit=999,wallets={[5]=20},raids={},presents={}}
YULE_SHOP_UI.created=true
Yule_ShopNextTarget()
assert(YULE_SHOP_UI.targetIndex==2 and context.targetLabel=='Enemy: player 2   >')
Yule_ShopBuy('pikes1'); assert(networkMessage=='pikes1:2')
assert(Yule_PurchaseNetwork(11,networkMessage)); assert(deployed[#deployed]==33)
Yule_ShopNextTarget()
assert(YULE_SHOP_UI.targetIndex==8 and context.targetLabel=='Enemy: player 8   >')
Yule_ShopBuy('pikes1'); assert(networkMessage=='pikes1:8')
assert(Yule_PurchaseNetwork(11,networkMessage)); assert(deployed[#deployed]==22)
assert(YULE.wallets[5]==18 and YULE.wallets[1]==nil)
assert(not Yule_PurchaseNetwork(11,'pikes1:3')) -- old internal-order target
assert(not Yule_PurchaseNetwork(11,'pikes1:1')) -- ally
assert(not Yule_PurchaseNetwork(11,'pikes1:4')) -- eliminated
assert(not Yule_PurchaseNetwork(11,'pikes1:5')) -- self
assert(not Yule_PurchaseNetwork(99,'pikes1:2'))
assert(YULE.wallets[5]==18)
Yule_ShopNextTarget(); assert(YULE_SHOP_UI.targetIndex==2)
players[3].isEliminated=true
Yule_RefreshShop(); assert(YULE_SHOP_UI.targetIndex==0)
assert(context.targetLabel=='Choose enemy' and not context.enabled.pikes1)
Yule_ShopNextTarget(); assert(YULE_SHOP_UI.targetIndex==8)
assert(not Yule_PurchaseNetwork(11,'pikes1:2'))
players[3].isEliminated=false

-- A golden pickup credits the same lobby-slot wallet and never rolls a reward.
Yule_UpdateVisit=function() end
Yule_FindOpener=function() return players[1] end
Entity_IsValid=function() return true end
Entity_Destroy=function() end
World_GetRand=function() error('Golden pickups must not roll ordinary rewards') end
YULE.presents={{id=101,entity=101,position={x=0,z=0},expires=100,golden=true}}
Yule_Tick(); assert(YULE.wallets[5]==19 and #YULE.presents==0)
Yule_Tick(); assert(YULE.wallets[5]==19)
Yule_RefreshShop(); assert(context.wallet=='Golden presents: 19')

-- Ordinary pickup uses the new weighted draw and is consumed only once.
paid={}; local pickupRolls=0
World_GetRand=function(a,b) assert(a==1 and b==100); pickupRolls=pickupRolls+1; return 41 end
YULE.presents={{id=102,entity=102,position={x=0,z=0},expires=100,golden=false}}
Yule_Tick(); assert(paid[22]==150 and paid[33]==150 and paid[11]==nil)
Yule_Tick(); assert(pickupRolls==1 and paid[22]==150 and YULE.wallets[5]==19)
''')
print('PASS: exact 40/40/10/10 rewards, unchanged golden tokens, reordered/gapped lobby slots, correct raid recipients, eliminated targets, wallet and pickup consistency.')
