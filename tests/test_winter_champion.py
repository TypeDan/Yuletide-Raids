"""Run actual purchase code: ownership, cap, refunds, lifetime and network selection."""
from pathlib import Path
from lupa import LuaRuntime
root=Path(__file__).resolve().parents[1]
lua=LuaRuntime()
for file in ('yuletide_shop.scar','yuletide_buffs.scar'):
    lua.execute((root/'assets/scar/christmas'/file).read_text())
lua.execute('''
MAT_Entity=1; MAT_Weapon=2; MUT_Multiplication=3
AGS_BP_MILITARY='military';AGS_BP_BUILDING='building';AGS_BP_VILLAGER='villager'
YULE={running=true,wallets={[2]=30,[7]=30},champions={}}
players={{id=11},{id=22}}
Yule_LivePlayers=function() return players end
Player_GetSlotIndex=function(p) return p==11 and 2 or 7 end
Player_GetCurrentAge=function() return 1 end
Game_GetLocalPlayer=function() return 11 end
entities={}
for i=1,10 do entities[i]={id=i,owner=11,alive=true,military=true,hardpoints=2} end
entities[11]={id=11,owner=22,alive=true,military=true,hardpoints=2}
entities[12]={id=12,owner=11,alive=true,villager=true}
entities[13]={id=13,owner=11,alive=true,military=true,building=true}
entities[14]={id=14,alive=true,military=true,world=true}
Entity_IsValid=function(id) return entities[id]~=nil end
Entity_FromID=function(id) return entities[id] end
Entity_IsAlive=function(e) return e.alive end
Entity_GetID=function(e) return e.id end
Entity_IsOfType=function(e,t) return e[t]==true end
World_OwnsEntity=function(e) return e.world==true end
Entity_GetPlayerOwner=function(e) assert(not e.world);return e.owner end
Entity_GetWeaponHardpointCount=function(e) return e.hardpoints end
active={};nextID=0;fail=false
Modifier_Create=function(scope,name,usage,exclusive,value,target)
    assert(usage==MUT_Multiplication and value==1.2 and not exclusive)
    if scope==MAT_Weapon then assert(name=='damage_weapon_modifier' and (target=='hardpoint_01' or target=='hardpoint_02'))
    else assert(scope==MAT_Entity and target==nil) end
    return {name=name,target=target,value=value,scope=scope}
end
Modifier_ApplyToEntity=function(mod,e,duration)
    assert(duration==0); if fail and mod.name=='armor_scalar_for_ranged_damage' then return nil end
    nextID=nextID+1;mod.entity=e.id;active[nextID]=mod;return {nextID}
end
Modifier_Remove=function(ids)
    for _,id in ipairs(ids) do
        if type(id)=='table' then Modifier_Remove(id) else active[id]=nil end
    end
end
for _,target in ipairs({0,11,12,13,14,999}) do
    assert(not Yule_PurchaseNetwork(11,'champion:'..target))
    assert(YULE.wallets[2]==30)
end
for i=1,5 do assert(Yule_PurchaseNetwork(11,'champion:'..i)) end
assert(YULE.wallets[2]==15 and Yule_ChampionCount(11)==5)
local count=0;for _,mod in pairs(active) do count=count+1 end;assert(count==30)
assert(not Yule_PurchaseNetwork(11,'champion:6')) -- cap
assert(not Yule_PurchaseNetwork(11,'champion:1')) -- no stacking
assert(not Yule_PurchaseNetwork(22,'champion:1')) -- cannot target enemy
assert(Yule_PurchaseNetwork(22,'champion:11')) -- separate owner cap
assert(YULE.wallets[7]==27 and Yule_ChampionCount(22)==1)
entities[1].alive=false
assert(Yule_ChampionCount(11)==4)
assert(Yule_PurchaseNetwork(11,'champion:6')) -- death frees a slot immediately
assert(Yule_ChampionCount(11)==5 and YULE.wallets[2]==12)
entities[2].owner=22;Yule_UpdateChampions() -- conversion removes blessing
assert(Yule_ChampionCount(11)==4 and Yule_ChampionCount(22)==1)
assert(Yule_PurchaseNetwork(22,'champion:2'))
fail=true;local before=YULE.wallets[2]
assert(not Yule_PurchaseNetwork(11,'champion:7') and YULE.wallets[2]==before)
for _,mod in pairs(active) do assert(mod.entity~=7) end -- atomic rollback
fail=false;YULE.wallets[2]=2
assert(not Yule_PurchaseNetwork(11,'champion:7'))
YULE.wallets[2]=3;assert(Yule_PurchaseNetwork(11,'champion:7'));assert(YULE.wallets[2]==0)
for _,bad in ipairs({'champion:-1','champion:7.5','champion:7:8','champion:abc',string.rep('1',50)}) do
    assert(not Yule_PurchaseNetwork(11,bad))
end
Yule_ClearChampions();assert(#YULE.champions==0 and next(active)==nil)
YULE.wallets[2]=9
Player_GetAllEntities=function(p) local out={};for _,e in pairs(entities) do if e.owner==p then table.insert(out,e) end end;return out end
EGroup_ForEach=function(g,fn) for i,e in ipairs(g) do fn(g,i,e) end end
Misc_IsEntitySelected=function(e) return e.selected end
Network_CallEvent=function(name,payload) sent={name,payload} end
entities[8].selected=true
Yule_ShopBuy('champion');assert(sent[1]=='Yule_PurchaseNetwork' and sent[2]=='champion:8')
assert(#YULE.champions==0) -- UI only emits a request
assert(Yule_PurchaseNetwork(11,sent[2]))
sent=nil;Yule_ShopBuy('champion');assert(sent==nil) -- already blessed
entities[8].selected=false;entities[9].selected=true;entities[10].selected=true
Yule_ShopBuy('champion');assert(sent==nil) -- select exactly one
entities[10].selected=false;Yule_ShopBuy('champion');assert(sent[2]=='champion:9')
-- Simulation acts on transmitted ID even if local selection changes later.
entities[9].selected=false;entities[10].selected=true
assert(Yule_PurchaseNetwork(11,sent[2]))
assert(YULE.champions[2].id==9)
YULE.running=false;assert(not Yule_PurchaseNetwork(11,'champion:10'))
''')
print('PASS: per-unit 1.2 modifiers, all weapons, 3-token cost, owner authority, 5 living slots, no stacking, death/conversion cleanup, refunds and synchronized selection.')
