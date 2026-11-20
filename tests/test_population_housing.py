"""Maximum capacity must not grant housing, including per-slot and team transfers."""
from pathlib import Path
from lupa import LuaRuntime
root=Path(__file__).resolve().parents[1]
lua=LuaRuntime()
lua.execute('Core_RegisterModule=function() end; AGS_Print=function() end')
for name in ['ags_global_settings.scar','gameplay/ags_population_capacity.scar','gameplay/ags_team_balance.scar']:
    lua.execute((root/'assets/scar'/name).read_text(encoding='utf-8-sig'))
lua.execute('''
MAT_Player=1; MUT_Addition=2; CT_Personnel=1; AGS_CIV_MONGOL='mongol'
local state={}; local slots={}
Player_GetSlotIndex=function(id) return slots[id] end
Modifier_Create=function(scope,name,usage,exclusive,value,bp) return {name=name,value=value} end
Modifier_ApplyToPlayer=function(m,id)
    local p=state[id]
    if m.name=='max_personnel_cap_player_modifier' then p.maximum=p.maximum+m.value
    elseif m.name=='personnel_cap_player_modifier' then p.housing=p.housing+m.value
    else error(m.name) end
end
Player_ClearPopCapOverride=function(id) state[id].fixed=nil end
Player_SetPopCapOverride=function() error('This bypasses houses') end
local function housing(id)
    local p=state[id]; return p.fixed or math.min(p.housing,p.maximum)
end
local keys={'FirstSlot','SecondSlot','ThirdSlot','FourthSlot','FifthSlot','SixthSlot','SeventhSlot','EighthSlot'}
for _,maximum in ipairs({250,300,500}) do
    for _,global in ipairs({false,true}) do
        PLAYERS={}; state={}; slots={}
        AGS_GLOBAL_SETTINGS.MaximumPopulation=global and maximum or 200
        AGS_GLOBAL_SETTINGS.MinimumPopulation=0; AGS_GLOBAL_SETTINGS.MinimumPopulationReset=false
        for slot,key in ipairs(keys) do
            local id=100+slot; slots[id]=slot
            local race=slot==3 and 'mongol' or 'english'
            state[id]={maximum=200,housing=race=='mongol' and 200 or 15}
            PLAYERS[9-slot]={id=id,slotIndex=9-slot,raceName=race}
            AGS_GLOBAL_SETTINGS.PlayerPopulationCaps[key]=(not global and slot<=3) and maximum or 0
        end
        AGS_PopulationCapacity_PresetFinalize()
        state[101].fixed=maximum -- also clears the previous release's bad override on restore
        AGS_PopulationCapacity_OnPlay()
        for id,p in pairs(state) do
            local expected=(global or slots[id]<=3) and maximum or 200
            assert(p.maximum==expected)
            assert(housing(id)==(slots[id]==3 and expected or 15))
        end
        state[101].housing=25 -- a completed house adds ten usable places
        assert(housing(101)==25)
        state[101].housing=maximum+20
        assert(housing(101)==maximum) -- enough houses reach the chosen ceiling
        state[101].housing=15
        assert(housing(101)==15) -- losing houses reduces available population again
        AGS_PopulationCapacity_OnPlay(); AGS_PopulationCapacity_OnGameRestore()
        assert(state[101].maximum==maximum and housing(101)==15) -- no stacking
        local host=nil
        for _,p in ipairs(PLAYERS) do if p.id==101 then host=p end end
        AGS_TeamBalance_IncreaseMaxCapPopulation(host,75)
        assert(state[101].maximum==maximum+75 and housing(101)==15)
    end
end
-- Every lobby slot can have its own ceiling without receiving free housing.
PLAYERS={}; state={}; slots={}
AGS_GLOBAL_SETTINGS.MaximumPopulation=200
AGS_GLOBAL_SETTINGS.MinimumPopulation=0
AGS_GLOBAL_SETTINGS.MinimumPopulationReset=false
local independentCaps={250,300,350,400,450,500,550,600}
for slot,key in ipairs(keys) do
    local id=200+slot; slots[id]=slot
    state[id]={maximum=200,housing=10,fixed=independentCaps[slot]}
    PLAYERS[9-slot]={id=id,slotIndex=9-slot,raceName='english'}
    AGS_GLOBAL_SETTINGS.PlayerPopulationCaps[key]=independentCaps[slot]
end
AGS_PopulationCapacity_PresetFinalize()
AGS_PopulationCapacity_OnPlay()
for slot,maximum in ipairs(independentCaps) do
    local id=200+slot
    assert(state[id].maximum==maximum, 'wrong maximum for slot '..slot)
    assert(housing(id)==10, 'free housing for slot '..slot)
    state[id].housing=20
    assert(housing(id)==20)
    state[id].housing=maximum+20
    assert(housing(id)==maximum)
    state[id].housing=10
    assert(housing(id)==10)
end
AGS_PopulationCapacity_OnGameRestore()
for slot,maximum in ipairs(independentCaps) do
    assert(state[200+slot].maximum==maximum and housing(200+slot)==10)
end
''')
print('PASS: independent ceilings for all eight slots, global settings, normal house growth/loss, Mongol housing, repeated play/restore and team transfer without free housing.')
