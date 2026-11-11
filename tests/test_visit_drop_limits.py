"""Regression checks for successful drop counts, retry bounds and golden odds."""
from pathlib import Path
from lupa import LuaRuntime

lua = LuaRuntime()
lua.execute('Core_RegisterModule=function() end; import=function() end; print=function() end')
root = Path(__file__).resolve().parents[1] / 'assets/scar/christmas'
for filename in ('yuletide.scar', 'yuletide_convoy.scar'):
    lua.execute((root / filename).read_text())

lua.execute('''
World_Pos=function(x,y,z) return {x=x,y=y,z=z} end
World_GetWidth=function() return 240 end; World_GetLength=function() return 240 end
World_GetHeightAt=function() return 0 end; World_GetTerrainCellType=function() return 1 end
local chosen=5
World_GetRand=function(a,b)
    if a==5 then assert(b>=5 and b<=10); return math.min(chosen,b) end
    return a
end
Yule_ConvoyMember=function(owner,bp,name,pos) return {position=pos} end
SGroup_GetPosition=function(group) return group.position end
SGroup_CountSpawned=function() return 1 end
Yule_DestroyGroup=function() end; Yule_Notify=function() end
local players={{id=1},{id=2}}
local function reset(target,existing)
    chosen=target
    YULE={running=true,time=0,visits=0,presents={},raids={},blueprints={santa=1,reindeer={1,2,3,4,5,6,7,8,9}}}
    for i=1,existing or 0 do YULE.presents[i]={} end
end
local realDrop=Yule_DropPresent
local checks,successes=0,0
Yule_DropAreaClear=function() checks=checks+1; return true end
Yule_DropPresent=function()
    successes=successes+1
    YULE.presents[#YULE.presents+1]={}
    return true
end
for target=5,10 do
    reset(target,0); successes=0
    assert(Yule_StartVisit(players) and YULE.santa.dropTarget==target)
    for time=1,60 do YULE.time=time; Yule_UpdateVisit(players) end
    assert(successes==target and #YULE.presents==target and YULE.santa==nil)
end

-- A busy map reserves only the room available, always at least five presents.
reset(10,19); successes=0
assert(Yule_StartVisit(players) and YULE.santa.dropTarget==5)
for time=1,60 do YULE.time=time; Yule_UpdateVisit(players) end
assert(successes==5 and #YULE.presents==24 and YULE.santa==nil)
for existing=20,24 do
    reset(10,existing)
    assert(not Yule_StartVisit(players) and YULE.santa==nil and YULE.visits==0)
end

-- Blockage is retried with bounded work and cannot end a visit below its target.
reset(7,0); successes=0; checks=0
assert(Yule_StartVisit(players))
Yule_DropAreaClear=function() checks=checks+1; return false end
for time=1,50 do YULE.time=time; Yule_UpdateVisit(players) end
assert(checks==8*50 and successes==0 and YULE.santa~=nil)
-- Even an apparently clear point may fail its engine-resolved spawn position.
Yule_DropAreaClear=function() return true end
local resolvedAttempts=0
Yule_DropPresent=function() resolvedAttempts=resolvedAttempts+1; return false end
YULE.time=51; Yule_UpdateVisit(players)
assert(resolvedAttempts==8 and YULE.santa.drops==0)
Yule_DropPresent=function() successes=successes+1; return true end
for time=52,90 do YULE.time=time; Yule_UpdateVisit(players) end
assert(successes==7 and YULE.santa==nil)

-- Full capacity or unavailable land retries in five seconds, not another cycle.
reset(5,0); YULE.nextVisit=0
Yule_StartVisit=function() return false end
Yule_UpdateVisit=function() end; Yule_RefreshShop=function() end
Yule_LivePlayers=function() return players end
Yule_Tick(); assert(YULE.nextVisit==6)

-- Exercise real present creation for all 100 possible rolls, including 40/41.
Yule_DropPresent=realDrop
YULE.blueprints={present='ordinary',golden='golden'}
Entity_CreateENVFacing=function(bp,pos) return {blueprint=bp,position=pos} end
World_GetSpawnablePosition=function(pos) return pos end
Entity_Spawn=function() end; Entity_WarpToPos=function() end
Entity_GetID=function() return 1 end
local golden=0
for roll=1,100 do
    YULE.presents={}
    World_GetRand=function(a,b) assert(a==1 and b==100); return roll end
    assert(Yule_DropPresent({x=0,z=0},players))
    local present=YULE.presents[1]
    assert(present.golden==(roll<=40))
    assert(present.entity.blueprint==(roll<=40 and 'golden' or 'ordinary'))
    if present.golden then golden=golden+1 end
end
assert(golden==40)
''')
print('PASS: exact 5-10 successful drops, capacity reservation, bounded blocked-drop retries, extended visits, short deferred-start retry and exactly 40 golden rolls out of 100.')
