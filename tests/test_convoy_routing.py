from pathlib import Path
from lupa import LuaRuntime

lua = LuaRuntime()
lua.execute('Core_RegisterModule=function() end; import=function() end')
root = Path(__file__).resolve().parents[1] / 'assets/scar/christmas'
lua.execute((root / 'yuletide.scar').read_text())
lua.execute((root / 'yuletide_convoy.scar').read_text())
lua.execute('''
World_Pos=function(x,y,z) return {x=x,y=y,z=z} end
World_GetWidth=function() return 240 end
World_GetLength=function() return 400 end
World_GetHeightAt=function() return 7 end
World_GetTerrainCellType=function() return 1 end
World_GetRand=function(a,b) return math.random(a,b) end
Player_GetStartingPosition=function() error('Must not use a player base') end
Player_IsHuman=function() error('Human slots must not bias routes') end
Yule_Notify=function() end
Yule_ConvoyMember=function(owner,blueprint,name,position)
    return {owner=owner,position=position}
end
SGroup_GetPosition=function(group) return group.position end

local function routes(players)
    math.randomseed(7241)
    YULE={visits=0,time=0,blueprints={santa=1,reindeer={1,2,3,4,5,6,7,8,9}}}
    local result={}
    for i=1,40 do
        assert(Yule_StartVisit(players))
        local santa=YULE.santa
        result[#result+1]=santa.position
        result[#result+1]=santa.destination
        assert(#santa.members==9)
    end
    return result
end
local a=routes({{id=1},{id=2}})
local b=routes({{id=8},{id=7},{id=6},{id=5},{id=4},{id=3},{id=2},{id=1}})
for i,p in ipairs(a) do
    assert(p.x==b[i].x and p.z==b[i].z, 'Player count or order changed the route')
    assert(math.abs(p.x)<=96 and math.abs(p.z)<=176 and p.y==7)
end

-- Sampling covers the map rather than choosing the farthest candidate or a base.
math.randomseed(5821)
local quadrants={0,0,0,0}
for i=1,4000 do
    local p=Yule_RandomMapPosition()
    local q=1+(p.x>=0 and 1 or 0)+(p.z>=0 and 2 or 0)
    quadrants[q]=quadrants[q]+1
end
for _,count in ipairs(quadrants) do assert(count>850 and count<1150) end
World_GetRand=function() return 0 end
local center=Yule_RandomWaypoint(World_Pos(90,0,170))
assert(center.x==0 and center.z==0)

-- Reject water and safely skip a visit when no land sample is available.
local terrainCalls=0
World_GetTerrainCellType=function()
    terrainCalls=terrainCalls+1
    return terrainCalls<4 and 2 or 1
end
assert(Yule_RandomMapPosition()~=nil and terrainCalls==4)
World_GetTerrainCellType=function() return 2 end
local calls=0; World_GetRand=function() calls=calls+1; return 0 end
assert(Yule_RandomMapPosition()==nil and calls==128)
local origin=World_Pos(1,0,2)
assert(Yule_RandomWaypoint(origin)==origin)
YULE.santa=nil
local visits=YULE.visits
assert(not Yule_StartVisit({{id=1},{id=2}}))
assert(YULE.santa==nil and YULE.visits==visits)
assert(not Yule_StartVisit({}))
''')
print('PASS: map-wide random routes, identical routes for different player counts/order, water rejection, bounded sampling and safe failed visits.')
