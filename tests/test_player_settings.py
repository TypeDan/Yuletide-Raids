"""Exercise lobby descriptor selections through the shared Lua settings/modules."""
from pathlib import Path
import xml.etree.ElementTree as ET
from lupa import LuaRuntime

root = Path(__file__).resolve().parents[1]
lua = LuaRuntime()
lua.execute('Core_RegisterModule=function() end; AGS_Print=function() end')
scar = root / 'assets/scar'
for name in ('ags_global_settings.scar', 'gameplay/ags_population_capacity.scar', 'gameplay/ags_handicaps.scar', 'gameplay/ags_team_balance.scar'):
    lua.execute((scar/name).read_text(encoding='utf-8-sig'))

# Derive every enum index from the actual ordered UI references, rather than
# inventing option tables that could conceal a broken descriptor.
descriptor = ET.parse(scar/'winconditions/ags_game_mode.rdo')
selections = {
    'option_player_setting_slot_1_population': 'max_population_250',
    'option_player_setting_slot_2_economic': 'slot_handicap_2',
    'option_player_setting_slot_8_military': 'slot_handicap_1_5',
}
options = {}
for section in descriptor.findall('.//DataObject[@Type="WinCondition::OptionSectionUIDescriptor"]'):
    key = section.find('DataProperty[@Name="m_key"]').get('Value')
    if key not in ('section_outer_handicap_settings', 'section_outer_military_handicap_settings', 'section_outer_population_settings'):
        continue
    opts = section.find('DataProperty[@Name="m_options"]')
    options[key] = {}
    for ref in opts.findall('DataValue'):
        obj = opts.find(f'DataObject[@Id="{ref.text}"]')
        name = obj.find('DataProperty[@Name="m_key"]').get('Value')
        enums = obj.find('DataProperty[@Name="m_enumItems"]')
        items = {}
        selected = None
        for index, enum_ref in enumerate(enums.findall('DataValue')):
            item = enums.find(f'DataObject[@Id="{enum_ref.text}"]')
            item_key = item.find('DataProperty[@Name="m_key"]').get('Value')
            items[item_key] = index
            if item.find('DataProperty[@Name="m_isDefaultValue"]').get('Value') == 'true':
                assert selected is None, f'Multiple defaults: {name}'
                selected = index
        assert selected is not None
        if name in selections:
            selected = items[selections[name]]
        options[key][name] = {'enum_items': items, 'enum_value': selected}
lua.globals().options = lua.table_from(options, recursive=True)
lua.execute('''
AGS_GlobalSettings_SetupSettings(options)
assert(AGS_GLOBAL_SETTINGS.PlayerPopulationCaps.FirstSlot==250)
assert(AGS_GLOBAL_SETTINGS.PlayerHandicaps.Economic.SecondSlot==2)
assert(AGS_GLOBAL_SETTINGS.PlayerHandicaps.Military.EighthSlot==1.5)
-- Internal index, legacy stored slot and team must never determine recipients.
PLAYERS={{id=81,slotIndex=1,raceName='english'},
         {id=21,slotIndex=8,raceName='english'},
         {id=11,slotIndex=2,raceName='english'}}
local slots={[81]=8,[21]=2,[11]=1}
Player_GetSlotIndex=function(p) return slots[p] end
unregistered={}
Core_UnregisterModule=function(name) unregistered[name]=true end
AGS_PopulationCapacity_UpdateModuleSettings(); AGS_Handicaps_UpdateModuleSettings()
assert(not unregistered.AGS_PopulationCapacity and not unregistered.AGS_Handicaps)
assert(AGS_PopulationCapacity_GetPlayerMaximum(PLAYERS[3])==250)
assert(AGS_PopulationCapacity_GetPlayerMaximum(PLAYERS[2])==200)
MAT_Player=1; MAT_EntityType=2; MUT_Addition=3; MUT_Multiplication=4
AGS_CIV_MONGOL='mongol'; modifiers={}; maxCaps={}
Modifier_Create=function(scope,name,usage,exclusive,value,bp)
    return {scope=scope,name=name,usage=usage,value=value,bp=bp}
end
Modifier_ApplyToPlayer=function(mod,p) mod.player=p; table.insert(modifiers,mod) end
local function engineMaximum(p)
    local result=200
    for _,mod in ipairs(modifiers) do
        if mod.player==p and mod.name=='max_personnel_cap_player_modifier' then result=result+mod.value end
    end
    return result
end
Player_ClearPopCapOverride=function(p) maxCaps[p]=engineMaximum(p) end
Player_SetPopCapOverride=function() error('Fixed population must not bypass houses') end
AGS_PopulationCapacity_PresetFinalize()
-- Simulate a stale fixed cap; clearing it restores the maximum modifier.
maxCaps[11]=200
AGS_PopulationCapacity_OnPlay(); assert(maxCaps[11]==250)
assert(maxCaps[21]==nil and maxCaps[81]==nil)
AGS_PopulationCapacity_OnPlay(); assert(maxCaps[11]==250) -- no stacking
AGS_GLOBAL_SETTINGS.MaximumPopulation=300
modifiers={}
AGS_PopulationCapacity_PresetFinalize(); AGS_PopulationCapacity_OnPlay()
assert(maxCaps[11]==250 and maxCaps[21]==300 and maxCaps[81]==300)
CT_Personnel=1
Player_GetMaxPopulationCapOverride=function(p) return maxCaps[p] or 200 end
AGS_TeamBalance_IncreaseMaxCapPopulation(PLAYERS[3],75)
assert(engineMaximum(11)==325)
AGS_GLOBAL_SETTINGS.MaximumPopulation=200
maxCaps[21]=nil
AGS_TeamBalance_IncreaseMaxCapPopulation(PLAYERS[2],50)
assert(maxCaps[21]==nil) -- default civ bonuses remain modifier-driven

AGS_BP_BUILDING='building'; AGS_BP_WORKER='worker'; AGS_BP_UNIT_CLASS='unit'
BP_GetEntityBlueprintsWithType=function(kind)
    if kind=='worker' then return {{PropertyBagGroupID=101},{PropertyBagGroupID=102}} end
    return {{PropertyBagGroupID=201}} -- duplicate in military/building lists
end
modifiers={}; AGS_Handicaps_OnPlay()
local economic,military=0,0
for _,mod in ipairs(modifiers) do
    assert(mod.scope==MAT_EntityType)
    if mod.bp.PropertyBagGroupID==101 or mod.bp.PropertyBagGroupID==102 then
        assert(mod.player==21 and mod.value==2 and mod.usage==MUT_Multiplication)
        economic=economic+1
    else
        assert(mod.player==81)
        military=military+1
    end
end
assert(economic==18 and military==5)
assert(PLAYERS[2].AGS_HandicapApplied.economic==2 and PLAYERS[2].AGS_HandicapApplied.military==nil)
assert(PLAYERS[1].AGS_HandicapApplied.military==1.5 and PLAYERS[1].AGS_HandicapApplied.economic==nil)
assert(PLAYERS[3].AGS_HandicapApplied==nil)
AGS_Handicaps_ApplyPerPlayer(); assert(#modifiers==23) -- no stacking
-- Military-only setup must remain enabled even when every eco setting is off.
AGS_GLOBAL_SETTINGS.PlayerHandicaps.Economic.SecondSlot=0
assert(AGS_Handicaps_HasAnyBonus())
AGS_GLOBAL_SETTINGS.PlayerHandicaps.Military.EighthSlot=0
assert(not AGS_Handicaps_HasAnyBonus())

-- All eight slots with simultaneous eco, military and custom population.
-- Reverse world order and deliberately set misleading legacy slot fields.
local keys={'FirstSlot','SecondSlot','ThirdSlot','FourthSlot','FifthSlot','SixthSlot','SeventhSlot','EighthSlot'}
PLAYERS={}; modifiers={}; maxCaps={}
AGS_HANDICAPS_ECO_MODIFIERS={}; AGS_HANDICAPS_MIL_MODIFIERS={}
for slot,key in ipairs(keys) do
    local id=100+slot; slots[id]=slot
    PLAYERS[9-slot]={id=id,slotIndex=9-slot,raceName='english'}
    AGS_GLOBAL_SETTINGS.PlayerHandicaps.Economic[key]=1+slot/10
    AGS_GLOBAL_SETTINGS.PlayerHandicaps.Military[key]=1+slot/20
    AGS_GLOBAL_SETTINGS.PlayerPopulationCaps[key]=250+slot*25
end
AGS_PopulationCapacity_PresetFinalize(); AGS_PopulationCapacity_OnPlay(); AGS_Handicaps_OnPlay()
for _,p in ipairs(PLAYERS) do
    local slot=slots[p.id]
    assert(maxCaps[p.id]==250+slot*25)
    assert(p.AGS_HandicapApplied.economic==1+slot/10)
    assert(p.AGS_HandicapApplied.military==1+slot/20)
end
local counts={}
for _,mod in ipairs(modifiers) do
    if mod.scope==MAT_EntityType then
    local slot=slots[mod.player]; counts[slot]=(counts[slot] or 0)+1
    local expected=mod.bp.PropertyBagGroupID==201 and (1+slot/20) or (1+slot/10)
    if mod.usage==MUT_Addition then expected=expected-1 end
    assert(mod.value==expected)
    end
end
for slot=1,8 do assert(counts[slot]==23) end

-- Host-only population increase: default global cap, every boost disabled.
-- Run with the host first/last internally and on the host/guest client.
-- Population must remain enabled without the handicap module keeping it alive.
local hostOption=options.section_outer_population_settings.option_player_setting_slot_1_population
for _,cap in ipairs({250,300,500}) do
    hostOption.enum_value=hostOption.enum_items['max_population_'..cap]
    AGS_GlobalSettings_SetupSettings({section_outer_population_settings=options.section_outer_population_settings})
    AGS_GLOBAL_SETTINGS.MaximumPopulation=200
    AGS_GLOBAL_SETTINGS.MinimumPopulation=0
    AGS_GLOBAL_SETTINGS.MinimumPopulationReset=false
    for _,key in ipairs(keys) do
        AGS_GLOBAL_SETTINGS.PlayerHandicaps.Economic[key]=0
        AGS_GLOBAL_SETTINGS.PlayerHandicaps.Military[key]=0
    end
    for _,race in ipairs({'english','mongol'}) do
        for _,hostFirst in ipairs({true,false}) do
            for _,localID in ipairs({501,502}) do
                local host={id=501,slotIndex=7,raceName=race,isHuman=true,isLocal=localID==501}
                local guest={id=502,slotIndex=1,raceName='english',isHuman=true,isLocal=localID==502}
                local ai={id=503,slotIndex=2,raceName='english',isHuman=false,isLocal=false}
                slots[501]=1; slots[502]=2; slots[503]=3
                PLAYERS=hostFirst and {host,guest,ai} or {guest,ai,host}
                Game_GetLocalPlayer=function() return localID end
                unregistered={}; modifiers={}; maxCaps={[501]=200,[502]=200,[503]=200}
                AGS_PopulationCapacity_UpdateModuleSettings(); AGS_Handicaps_UpdateModuleSettings()
                assert(not unregistered.AGS_PopulationCapacity and unregistered.AGS_Handicaps)
                AGS_PopulationCapacity_PresetFinalize(); AGS_PopulationCapacity_OnPlay()
                assert(AGS_PopulationCapacity_GetPlayerMaximum(host)==cap)
                assert(maxCaps[501]==cap and maxCaps[502]==200 and maxCaps[503]==200)
                local hostMaximum,hostHousing=nil,nil
                for _,mod in ipairs(modifiers) do
                    if mod.player==501 and mod.name=='max_personnel_cap_player_modifier' then hostMaximum=mod.value end
                    if mod.player==501 and mod.name=='personnel_cap_player_modifier' then hostHousing=mod.value end
                end
                assert(hostMaximum==cap-200)
                assert(hostHousing==(race=='mongol' and cap-200 or 0))
            end
        end
    end
end
''')
print('PASS: host-only 250/300/500 caps with everyone else at 200 (host/guest clients, reordered players, English/Mongols); descriptor selections; all eight combined bonuses/caps; no stacking.')
