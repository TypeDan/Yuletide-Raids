"""Deposits must never spawn on units, even if the engine moves a candidate."""
from pathlib import Path
from lupa import LuaRuntime

lua = LuaRuntime()
lua.execute('Core_RegisterModule=function() end; import=function() end')
lua.execute((Path(__file__).resolve().parents[1]/'assets/scar/christmas/yuletide.scar').read_text())
lua.execute((Path(__file__).resolve().parents[1]/'assets/scar/christmas/yuletide_shop.scar').read_text())
lua.execute('''
OT_Player=1; OT_Neutral=2; RT_Gold=1; R_ALLY=2
players={{id=1},{id=2},{id=3,isEliminated=true}}
World_GetPlayerCount=function() return #players end
World_GetPlayerAt=function(i) return players[i].id end
Player_GetSlotIndex=function(p) return p end
Player_GetCurrentAge=function() return 1 end
AGS_IsMutualRelation=function(a,b,r) return r==R_ALLY and b==2 end
World_GetTerrainCellType=function(x,z) return x<0 and 2 or 1 end
SGroup_CreateIfNotFound=function() return {} end
EGroup_CreateIfNotFound=function() return {} end
SGroup_CountSpawned=function(g) return g.n or 0 end
EGroup_CountSpawned=SGroup_CountSpawned
obstacles={}
local function query(player,g,pos,radius,owner,kind)
    assert(radius>=8); g.n=0
    for _,o in ipairs(obstacles) do
        if o.kind==kind and (o.player==player and owner==OT_Player or o.player==0 and owner==OT_Neutral)
            and (o.x-pos.x)^2+(o.z-pos.z)^2<radius^2 then g.n=g.n+1 end
    end
end
World_GetSquadsNearPoint=function(p,g,pos,r,o) query(p,g,pos,r,o,'squad') end
World_GetEntitiesNearPoint=function(p,g,pos,r,o) query(p,g,pos,r,o,'entity') end
for _,kind in ipairs({'squad','entity'}) do
    for player=0,3 do
        obstacles={{kind=kind,player=player,x=0,z=0}}
        assert(not Yule_DepositAreaClear({x=0,z=0}))
        assert(Yule_DepositAreaClear({x=20,z=20}))
    end
end
assert(not Yule_DepositAreaClear({x=-1,z=0}))
BP_GetEntityBlueprint=function(name) return name end
created={}; spawned={}; destroyed={}; paid={}; notices={}
Entity_CreateENVFacing=function(bp,pos)
    local e={bp=bp,pos=pos}; table.insert(created,e); return e
end
Entity_Destroy=function(e) destroyed[e]=true end
Entity_Spawn=function(e) table.insert(spawned,e) end
Entity_WarpToPos=function(e,pos) assert(Yule_DepositAreaClear(pos)); e.pos=pos end
Player_AddResource=function(p,r,n) paid[p]=(paid[p] or 0)+n end
Yule_Notify=function(n) table.insert(notices,n) end
-- Candidate is clear, but the engine resolves the first one onto the collector.
obstacles={{kind='squad',player=1,x=0,z=0}}
local attempts=0
Yule_PositionNear=function(pos,radius)
    attempts=attempts+1; assert(radius>=12)
    return {x=20+attempts,z=0}
end
World_GetSpawnablePosition=function(pos)
    if attempts==1 then return {x=0,z=0} end
    return pos
end
assert(Yule_SpawnSafeDeposit({x=0,z=0},3,players))
assert(#created==2 and destroyed[created[1]] and #spawned==1)
assert(spawned[1].bp=='resource_gold_deposit_small' and spawned[1].pos.x==22)
-- Repeated bad resolved positions are bounded; fallback splits the fixed pot.
created={}; spawned={}; attempts=0
World_GetSpawnablePosition=function() return {x=0,z=0} end
Yule_Reward(players[1],{x=0,z=0},4,players)
assert(attempts==24 and #spawned==0 and #created==24)
for _,e in ipairs(created) do assert(destroyed[e]) end
assert(paid[1]==50 and paid[2]==50 and paid[3]==nil)
assert(notices[#notices]==2003)
-- No valid resolved position also falls back safely.
World_GetSpawnablePosition=function() return nil end
assert(not Yule_SpawnSafeDeposit({x=0,z=0},3,players))
-- Odd totals are conserved and awarded deterministically in lobby order.
paid={}; Yule_ShareTeamGold(players[1],players,301)
assert(paid[1]==151 and paid[2]==150 and paid[3]==nil)
''')
print('PASS: collector, enemy, eliminated and neutral clearance; resolved overlap rejection; bounded retries; safe fallback and conserved team gold.')
