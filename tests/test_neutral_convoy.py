"""Convoys retain queued native routes without retaining a player owner."""
from pathlib import Path
from lupa import LuaRuntime

lua=LuaRuntime()
lua.execute((Path(__file__).resolve().parents[1]/'assets/scar/christmas/yuletide_convoy.scar').read_text())
lua.execute('''
World_Pos=function(x,y,z) return {x=x,y=y,z=z} end
World_GetWidth=function() return 400 end
World_GetLength=World_GetWidth
World_GetHeightAt=function() return 0 end
World_GetTerrainCellType=function() return 1 end
YULE={visits=1,time=1,running=true}
SGroup_CreateIfNotFound=function(name) return {name=name,orders={}} end
UnitEntry_DeploySquads=function(owner,group,units,pos) group.owner=owner;group.position=pos end
Cmd_Move=function(group,target,queued)
    assert(group.owner~=nil,'No commands may be issued to neutral squads')
    assert(queued==(#group.orders>0))
    table.insert(group.orders,target)
end
SGroup_SetWorldOwned=function(group) group.owner=nil;group.neutral=true end
SGroup_SetSelectable=function(group,value) group.selectable=value end
SGroup_SetInvulnerable=function(group,value) group.invulnerable=value end
SGroup_GetPosition=function(group) return group.position end
SGroup_CountSpawned=function() return 1 end
local route={{x=100,y=0,z=0},{x=100,y=0,z=100},{x=0,y=0,z=100}}
local origin=World_Pos(0,0,0)
for _,kind in ipairs({'santa','dasher'}) do
    local member=Yule_ConvoyMember(2,1,kind,origin,route,kind=='dasher' and 12 or nil,0)
    assert(member.owner==nil and member.neutral and member.invulnerable and not member.selectable)
    assert(#member.orders==3)
    YULE.santa={group=member,members={},position=origin}
    Cmd_Move=function() error('Flight must not issue commands or restore player ownership') end
    Yule_Flight()
    assert(member.owner==nil and YULE.santa.position==origin)
    Cmd_Move=function(group,target,queued)
        assert(group.owner~=nil and queued==(#group.orders>0));table.insert(group.orders,target)
    end
end
''')
print('PASS: native orders queued before ownership transfer; Santa and reindeer remain neutral, invulnerable and unselectable throughout flight.')
