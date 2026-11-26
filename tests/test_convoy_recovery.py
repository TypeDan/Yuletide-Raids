"""Blocked convoys phase to clear ground, requeue native motion and stay neutral."""
from pathlib import Path
from lupa import LuaRuntime

lua = LuaRuntime()
lua.execute((Path(__file__).resolve().parents[1] / 'assets/scar/christmas/yuletide_convoy.scar').read_text())
lua.execute('''
World_Pos=function(x,y,z) return {x=x,y=y,z=z} end
World_GetWidth=function() return 500 end;World_GetLength=World_GetWidth
World_GetHeightAt=function() return 0 end
local origin=World_Pos(0,0,0)
local function group() return {position=origin,neutral=true,orders={}} end
YULE={time=1,running=true,santa={group=group(),members={},position=origin,
    progressPosition=origin,progressCheck=2,dropTarget=12,drops=0,lastDelivery=0}}
for i=1,9 do YULE.santa.members[i]={group=group()} end
SGroup_GetPosition=function(g) return g.position end
SGroup_CountSpawned=function() return 1 end
local phases=0
SGroup_WarpToPos=function(g,p) phases=phases+1;g.position=p end
SGroup_SetPlayerOwner=function(g,p) g.owner=p;g.neutral=false end
SGroup_SetWorldOwned=function(g) g.owner=nil;g.neutral=true end
SGroup_SetSelectable=function(g,v) g.selectable=v end
SGroup_SetInvulnerable=function(g,v) g.invulnerable=v end
Cmd_Move=function(g,p,queued)
    assert(g.owner==27)
    if not queued then g.orders={} end
    table.insert(g.orders,p)
end
Yule_LivePlayers=function() return {{id=27},{id=9}} end
Yule_PositionNear=function(p) return World_Pos(p.x+2,0,p.z+2) end
Yule_RandomWaypoint=function(p) return World_Pos(-p.x,0,-p.z) end
local searches=0
Yule_FindDeliveryArea=function()
    searches=searches+1
    return searches==1 and origin or World_Pos(100,0,100)
end
Yule_Flight();assert(phases==0)
YULE.time=2;Yule_Flight();assert(phases==10 and searches==2)
local all={YULE.santa.group}
for _,m in ipairs(YULE.santa.members) do table.insert(all,m.group) end
for _,g in ipairs(all) do
    assert(g.neutral and g.owner==nil and g.invulnerable and not g.selectable)
    assert(#g.orders==64)
end
assert(YULE.santa.position.x==100 and YULE.santa.progressCheck==4)
-- Native movement is left alone once it is progressing.
YULE.santa.group.position=World_Pos(120,0,100)
YULE.time=4;Yule_Flight();assert(phases==10)
-- No safe site must never destroy the convoy or warp onto blocked ground.
Yule_FindDeliveryArea=function() return nil end
YULE.time=6;Yule_Flight();assert(phases==10 and YULE.santa.group.neutral)
''')
print('PASS: bounded stuck recovery, meaningful relocation, all ten units neutral and protected, native orders resumed, moving convoy untouched and no-clear-site safety.')
