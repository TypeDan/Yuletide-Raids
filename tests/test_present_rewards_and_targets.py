"""Run with Python + lupa; exercise the shipped Lua reward and shop functions."""
from pathlib import Path
from lupa import LuaRuntime

lua = LuaRuntime()
lua.execute('Core_RegisterModule=function() end; import=function() end')
root = Path(__file__).resolve().parents[1] / 'assets/scar/christmas'
for filename in ('yuletide.scar', 'yuletide_shop.scar', 'yuletide_buffs.scar'):
    lua.execute((root / filename).read_text())

lua.execute('''
RT_Gold=1; RT_Food=2; RT_Wood=3; RT_Stone=4; R_ENEMY=1; R_ALLY=2
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
names={[11]='Host',[22]='Morgan',[33]='Alex & Bea <Raid>',[44]='Ally',[55]='Defeated'}
Player_GetDisplayName=function(id) return {LocString=names[id]} end
AGS_IsMutualRelation=function(a,b,r)
    if r==R_ALLY then return a==11 and (b==44 or b==55) end
    return a==11 and (b==22 or b==33)
end
Player_GetCurrentAge=function() return 1 end
Game_GetLocalPlayer=function() return 11 end
Yule_CanReceiveVillagers=function() return true end
UI_SetDataContext=function(name,data) context=data end
Network_CallEvent=function(name,message) networkMessage=message end
Yule_Notify=function() end
paid={}; deposits={}; deployed={}
Player_GetResource=function() return 1000 end
Player_AddResource=function(id,resource,n) paid[id]=(paid[id] or 0)+n end
BP_GetEntityBlueprint=function(name) return name end
-- Clearance and engine-resolved positions are exercised separately.
Yule_SpawnSafeDeposit=function(position,outcome)
    local name=outcome==3 and 'resource_gold_deposit_small' or 'resource_stone_deposit_small'
    deposits[name]=(deposits[name] or 0)+1
    return true
end
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
assert(paid[11]==0 and paid[22]==2000 and paid[33]==2000)
assert(paid[44]==0 and paid[55]==nil)
assert(deposits.resource_gold_deposit_small==10 and deposits.resource_stone_deposit_small==10)
assert(YULE_CONFIG.goldenChance==nil)

-- Both pots use the collector's age; recipients' ages never multiply them.
for age,total in ipairs({100,150,200,300}) do
    Player_GetCurrentAge=function(id) return id==11 and age or 4 end
    paid={}
    Yule_Reward(players[1],{},2,players)
    assert(paid[22]==total/2 and paid[33]==total/2)
    assert(paid[11]==-total/2 and paid[44]==-total/2 and paid[55]==nil)
end
players[3].isEliminated=true
paid={}; Yule_Reward(players[1],{},2,players)
assert(paid[22]==300 and paid[33]==nil)
players[3].isEliminated=nil
Player_GetCurrentAge=function() return 1 end

-- Each teammate pays their share, capped at available gold, without redistribution.
for age,cost in ipairs({100,150,200,300}) do
    Player_GetCurrentAge=function(id) return id==11 and age or 1 end
    Player_GetResource=function(id) return id==11 and 35 or 1000 end
    paid={}; Yule_Reward(players[1],{},2,players)
    assert(paid[11]==-35 and paid[44]==-cost/2 and paid[55]==nil)
    assert(paid[22]==cost/2 and paid[33]==cost/2)
end
Player_GetResource=function() return 0 end
paid={}; Yule_Reward(players[1],{},2,players)
assert(paid[11]==0 and paid[44]==0 and paid[22]==150)
Player_GetResource=function() return 1000 end
Player_GetCurrentAge=function() return 1 end

-- Unequal 4v2 / 3v2 / 1v3 teams: each side's total remains exactly one pot.
local savedRelations=AGS_IsMutualRelation
local savedSlots=Yule_PlayerSlot
Yule_PlayerSlot=function(id) return id end
for _,sizes in ipairs({{4,2},{3,2},{1,3}}) do
    local roster={}
    for i=1,sizes[1] do table.insert(roster,{id=i}) end
    for i=1,sizes[2] do table.insert(roster,{id=10+i}) end
    table.insert(roster,{id=99,isEliminated=true})
    AGS_IsMutualRelation=function(a,b,r) return r==R_ALLY and b<10 or r==R_ENEMY and b>=10 end
    for age,pot in ipairs({100,150,200,300}) do
        Player_GetCurrentAge=function(id) return id==1 and age or 4 end
        paid={}; Yule_Reward(roster[1],{},2,roster)
        local debit,credit=0,0
        for id,delta in pairs(paid) do
            if id<10 then debit=debit-delta else credit=credit+delta end
        end
        assert(debit==pot and credit==pot and paid[99]==nil)
        if sizes[1]==3 and pot==100 then assert(paid[1]==-34 and paid[2]==-33 and paid[3]==-33) end
        if sizes[2]==3 and pot==100 then assert(paid[11]==34 and paid[12]==33 and paid[13]==33) end
        local first=paid
        local reversed={}; for i=#roster,1,-1 do table.insert(reversed,roster[i]) end
        paid={}; Yule_Reward(roster[1],{},2,reversed)
        for id,delta in pairs(first) do assert(paid[id]==delta) end
    end
end
paid={}; Yule_Reward({id=1},{},2,{{id=1},{id=99,isEliminated=true}})
assert(next(paid)==nil) -- No living enemies means no charge.
AGS_IsMutualRelation=savedRelations; Yule_PlayerSlot=savedSlots
Player_GetCurrentAge=function() return 1 end

-- UI, request payload, receiver and wallet must all agree on the lobby slot.
YULE={running=true,time=0,nextVisit=999,wallets={[5]=20},raids={},presents={}}
YULE_SHOP_UI.created=true
Yule_ShopNextTarget()
assert(YULE_SHOP_UI.targetIndex==2 and context.targetLabel=='Enemy: Alex & Bea <Raid>')
Yule_ShopBuy('pikes1'); assert(networkMessage=='pikes1:2')
assert(Yule_PurchaseNetwork(11,networkMessage)); assert(deployed[#deployed]==33)
Yule_ShopNextTarget()
assert(YULE_SHOP_UI.targetIndex==8 and context.targetLabel=='Enemy: Morgan')
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

-- Duplicate, missing and long names affect only display, never routing.
names[22]='Same name'; names[33]='Same name'
Yule_RefreshShop(); assert(context.targetLabel=='Enemy: Same name (P8)')
names[22]=nil
Yule_RefreshShop(); assert(context.targetLabel=='Enemy: Player 8')
names[22]=string.rep('Long name ',30)
Yule_RefreshShop(); assert(context.targetLabel=='Enemy: '..names[22])
Yule_ShopBuy('pikes1'); assert(networkMessage=='pikes1:8')
names[22]='Morgan'; names[33]='Alex & Bea <Raid>'

-- Every pickup credits the same lobby-slot wallet and rolls one reward.
Yule_UpdateVisit=function() end
Yule_FindOpener=function() return players[1] end
Entity_IsValid=function() return true end
Entity_Destroy=function() end
World_GetRand=function() return 1 end
YULE.presents={{id=101,entity=101,position={x=0,z=0},expires=100,golden=true}}
Yule_Tick(); assert(YULE.wallets[5]==19 and #YULE.presents==0)
Yule_Tick(); assert(YULE.wallets[5]==19)
Yule_RefreshShop(); assert(context.wallet=='Golden presents: 19')

-- Ordinary pickup uses the new weighted draw and is consumed only once.
paid={}; local pickupRolls=0
World_GetRand=function(a,b) assert(a==1 and b==100); pickupRolls=pickupRolls+1; return 41 end
YULE.presents={{id=102,entity=102,position={x=0,z=0},expires=100,golden=false}}
Yule_Tick(); assert(paid[22]==50 and paid[33]==50 and paid[11]==-50 and paid[44]==-50)
Yule_Tick(); assert(pickupRolls==1 and paid[22]==50 and YULE.wallets[5]==20)

-- Found gold is shared with living teammates, once per collected present.
paid={}; pickupRolls=0
World_GetRand=function(a,b) assert(a==1 and b==100); pickupRolls=pickupRolls+1; return 1 end
YULE.presents={{id=103,entity=103,position={x=0,z=0},expires=100,golden=false}}
Yule_Tick(); assert(paid[11]==50 and paid[44]==50 and paid[22]==nil and paid[33]==nil and paid[55]==nil)
Yule_Tick(); assert(pickupRolls==1 and paid[11]==50 and paid[44]==50)

-- Purchased gold uses the buyer's age and stays entirely with the buyer.
for age,total in ipairs({100,150,200,300}) do
    Player_GetCurrentAge=function() return age end
    paid={}; YULE.wallets[5]=1
    assert(Yule_PurchaseNetwork(11,'gold:0') and YULE.wallets[5]==0)
    assert(paid[11]==total)
    assert(paid[22]==nil and paid[33]==nil and paid[44]==nil and paid[55]==nil)
    assert(not Yule_PurchaseNetwork(11,'gold:0'))
end
''')
print('PASS: shared found gold, buyer-only purchased gold in all ages, 40/40/10/10 ordinary rewards, guaranteed tokens plus outcomes, lobby-slot raid targets, wallet and one-time pickups.')
