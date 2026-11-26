"""Verify gifts follow Santa while preserving spacing and native spawn safety."""
from pathlib import Path
from lupa import LuaRuntime

lua = LuaRuntime()
lua.execute('Core_RegisterModule=function() end; import=function() end')
root = Path(__file__).resolve().parents[1] / 'assets/scar/christmas'
for name in ('yuletide.scar', 'yuletide_convoy.scar'):
    lua.execute((root / name).read_text())
lua.execute('''
math.randomseed(97531)
World_Pos=function(x,y,z) return {x=x,y=y,z=z} end
World_GetWidth=function() return 600 end
World_GetLength=World_GetWidth
World_GetHeightAt=function() return 0 end
World_GetTerrainCellType=function() return 1 end
World_GetRand=function(a,b)
    if a==8 and b==12 then return 12 end
    return math.random(a,b)
end
local players={{id=2},{id=1}}
Yule_LivePlayers=function() return players end
Yule_RefreshShop=function() end; Yule_UpdateCheer=function() end
Yule_FindOpener=function() return nil end
local notices=0
Yule_Notify=function() notices=notices+1 end
Sound_Play2D=function() end
local liveGroups=0; local maxGroups=0; local deployed=0
SGroup_CreateIfNotFound=function(name) return {name=name,orders={}} end
UnitEntry_DeploySquads=function(owner,group,units,pos)
    group.owner=owner;group.position=pos;group.live=true
    liveGroups=liveGroups+1;maxGroups=math.max(maxGroups,liveGroups);deployed=deployed+1
end
Cmd_Move=function(group,pos,queued)
    assert(group.owner~=nil and queued==(#group.orders>0))
    table.insert(group.orders,pos)
end
SGroup_SetWorldOwned=function(group) group.owner=nil;group.neutral=true end
SGroup_SetSelectable=function(group,value) group.selectable=value end
SGroup_SetInvulnerable=function(group,value) group.invulnerable=value end
SGroup_GetPosition=function(group) return group.position end
SGroup_CountSpawned=function(group) return group.live and 1 or 0 end
SGroup_DestroyAllSquads=function(group)
    assert(group.live); group.live=false;liveGroups=liveGroups-1
end
SGroup_Destroy=function() end
EGroup_CreateIfNotFound=function() return {} end
EGroup_Clear=function() end; Player_GetAllEntitiesNearMarker=function() end
local building=false
EGroup_ForEach=function(group,fn) if building then fn(group,1,{}) end end
Entity_IsOfType=function() return true end
local id=0; local destroyed=0; local sites={}; local times={}; local override=nil
Entity_CreateENVFacing=function(bp,pos)
    id=id+1;return {id=id,position=pos,live=true}
end
World_GetSpawnablePosition=function(pos) return override or pos end
Entity_Spawn=function() end
Entity_WarpToPos=function(entity,pos)
    local cart=SGroup_GetPosition(YULE.santa.group)
    assert((pos.x-cart.x)^2+(pos.z-cart.z)^2<=YULE_CONFIG.maxDropOffset^2,
        'Gift appeared away from the actual cart')
    entity.position=pos;table.insert(sites,pos);table.insert(times,YULE.time)
end
Entity_GetID=function(entity) return entity.id end
Entity_IsValid=function() return true end
Entity_Destroy=function(entity) entity.live=false;destroyed=destroyed+1 end
YULE.running=true
YULE.blueprints={santa=1,reindeer={1,2,3,4,5,6,7,8,9},present=2,golden=3}
assert(YULE_CONFIG.firstVisit==60 and YULE.nextVisit==60)
for i=1,59 do Yule_Tick(); assert(YULE.santa==nil and #sites==0) end
Yule_Tick()
assert(YULE.time==60 and #sites==1 and YULE.santa.drops==1)
assert(YULE.santa.dropTarget==12 and #YULE.santa.members==9 and notices==2)
local first=sites[1]

-- An immediately collected present must still stop this location being reused.
YULE.presents={}
assert(not Yule_DropAreaClear(first,players))
for i=1,5 do Yule_Tick(); assert(#sites==1 and deployed==10) end
for i=1,44 do Yule_Tick() end
assert(#sites==1 and deployed==10 and YULE.santa.drops==1 and notices==2,
    'Stationary Santa must wait instead of scattering gifts elsewhere')

-- Engine placement can move a valid candidate back beside an earlier gift.
override=first
local before=#sites;local count=destroyed
assert(not Yule_DropPresent(World_Pos(250,0,250),players))
assert(#sites==before and destroyed==count+1)
override=nil

-- Even a clear engine-resolved point is invalid if far from Santa.
override=World_Pos(250,0,250)
before=#sites;count=destroyed
assert(not Yule_DropPresent(World_Pos(0,0,0),players,World_Pos(0,0,0)))
assert(#sites==before and destroyed==count+1)
override=nil

-- Move along a route and verify every gift appears beside the cart, while
-- instant collection cannot bypass the spacing history or create extra Santas.
for tick=350,800 do
    local step=math.floor((tick-350)/10)
    if YULE.santa then
        YULE.santa.group.position=World_Pos(-240+(step%5)*120,0,-240+(math.floor(step/5)%5)*120)
    end
    YULE.presents={} -- simulate instant collection after each successful drop
    Yule_Tick()
    if YULE.santa then
        local groups={YULE.santa.group}
        for _,m in ipairs(YULE.santa.members) do table.insert(groups,m.group) end
        for _,g in ipairs(groups) do
            assert(g.neutral and g.owner==nil and g.invulnerable and not g.selectable)
        end
    else break end
end
assert(#sites==12 and YULE.visits==1 and YULE.santa==nil and notices==2)
assert(maxGroups==10 and liveGroups==0 and deployed==10)
for i,a in ipairs(sites) do
    if i>1 then assert(times[i]-times[i-1]>=YULE_CONFIG.dropMin) end
    for j,b in ipairs(sites) do
        if i~=j then assert((a.x-b.x)^2+(a.z-b.z)^2>=Yule_DropSpacing()^2) end
    end
end
-- Crowded/water maps fail safely without an announcement or a partial convoy.
building=true
local n=YULE.visits
assert(not Yule_StartVisit(players) and YULE.visits==n and liveGroups==0)
building=false
World_GetTerrainCellType=function() return 2 end
assert(not Yule_StartVisit(players) and YULE.visits==n)
assert(not Yule_DropAreaClear(nil,players))
''')
print('PASS: first drop at 1:00 with a five-second warning, 12 gifts beside actual Santa positions, stationary cart waits, pairwise spacing after pickups, remote native placement rejected, neutral single convoy, bounded blocked/water handling.')
