"""Exercise lobby parsing, arrival/bell timing and guaranteed token pickups."""
from pathlib import Path
import xml.etree.ElementTree as E
from lupa import LuaRuntime

root = Path(__file__).resolve().parents[1]
lua = LuaRuntime()
lua.execute('Core_RegisterModule=function() end; import=function() end; print=function() end')
for name in ('yuletide.scar', 'yuletide_shop.scar', 'yuletide_settings.scar'):
    lua.execute((root / 'assets/scar/christmas' / name).read_text())
lua.execute('''
local function option(value) return {enum_value=17,enum_items={['yule_value_'..value]=17}} end
Yule_SetupSettings({})
assert(table.concat(YULE_CONFIG.presentWeights,",")=="60,20,10,10")
assert(YULE_CONFIG.minGiftsPerVisit==8 and YULE_CONFIG.giftsPerVisit==12)
for slot=1,8 do assert(YULE_CONFIG.startingTokens[slot]==0) end
Yule_SetupSettings({section_yuletide={minimum_presents=option(20),maximum_presents=option(3),
    team_gold_weight=option(5),enemy_gold_weight=option(0),gold_deposit_weight=option(10),stone_deposit_weight=option(5)},
    section_yuletide_wallets={starting_tokens=option(7),starting_tokens_1=option(25),starting_tokens_8=option(0)}})
assert(YULE_CONFIG.minGiftsPerVisit==3 and YULE_CONFIG.giftsPerVisit==20)
assert(YULE_CONFIG.startingTokens[1]==25 and YULE_CONFIG.startingTokens[8]==0 and YULE_CONFIG.startingTokens[2]==7)
local counts={0,0,0,0}
for roll=1,20 do
    World_GetRand=function(a,b) assert(a==1 and b==20);return roll end
    local result=Yule_RollPresentOutcome();counts[result]=counts[result]+1
end
assert(counts[1]==5 and counts[2]==0 and counts[3]==10 and counts[4]==5)
assert(Yule_LobbyNumber(option(999),12,1,20)==12)
assert(Yule_LobbyNumber({enum_value=9,enum_items={bad=9}},12,1,20)==12)
assert(Yule_LobbyNumber(nil,12,1,20)==12)
Player_GetSlotIndex=function(id) return ({[41]=1,[5]=8,[91]=2})[id] end
local players={{id=5},{id=91},{id=41}}
YULE.wallets={};Yule_InitializeWallets(players)
assert(YULE.wallets[1]==25 and YULE.wallets[8]==0 and YULE.wallets[2]==7)
YULE.wallets[1]=3;Yule_InitializeWallets(players);assert(YULE.wallets[1]==3)
Yule_SetupSettings({section_yuletide_wallets={starting_tokens=option(7),starting_tokens_4=option(2)},
    section_yuletide_wallets_high={starting_tokens_5=option(25),starting_tokens_8=option(0)}})
assert(YULE_CONFIG.startingTokens[4]==2 and YULE_CONFIG.startingTokens[5]==25)
assert(YULE_CONFIG.startingTokens[6]==7 and YULE_CONFIG.startingTokens[8]==0)

Yule_SetupSettings({})
YULE={running=true,time=0,nextVisit=YULE_CONFIG.firstVisit,presents={},raids={},wallets={}}
Yule_RefreshShop=function() end;Yule_UpdateCheer=function() end
Yule_LivePlayers=function() return players end
local warnings={};local arrivals={};local bells={}
Sound_Play2D=function(sound)
    assert(sound=='taunt_007');table.insert(bells,YULE.time)
end
Loc_Empty=function() return '' end;ECV_Title=3
UI_CreateEventCue=function(title,description,template,icon,sound,visibility,lifetime)
    assert(title==YULE_LOC..'2008' and sound=='taunt_007')
    assert(visibility==ECV_Title and lifetime==5)
    table.insert(warnings,YULE.time)
    table.insert(bells,YULE.time)
end
Yule_StartVisit=function() table.insert(arrivals,YULE.time);YULE.santa={ends=YULE.time+10};return true end
Yule_UpdateVisit=function() if YULE.santa and YULE.time>=YULE.santa.ends then YULE.santa=nil end end
for time=1,600 do Yule_Tick() end
assert(#arrivals==4 and #warnings==4 and #bells==16)
for i,time in ipairs(arrivals) do
    assert(time==60+(i-1)*180 and warnings[i]==time-5)
    for burst=1,4 do assert(bells[(i-1)*4+burst]==time-6+burst) end
end
-- Normal announcements retain their notification cue rather than repeating bells.
UI_CreateEventCue=function(title,description,template,icon,sound)
    assert(sound=='sfx_ui_event_queue_med_priority_play')
end
Yule_Notify(2001);Yule_Notify(2004)

-- Every outcome, including disabled bonuses, gives exactly one private token.
YULE.santa=nil;YULE.nextVisit=9999
Entity_IsValid=function() return true end;Entity_Destroy=function() end
Yule_FindOpener=function() return players[3] end
local rewards={}
Yule_Reward=function(opener,pos,result) assert(opener.id==41);table.insert(rewards,result) end
for i,roll in ipairs({1,61,81,91}) do
    World_GetRand=function(a,b) assert(a==1 and b==100);return roll end
    YULE.presents={{id=i,entity=i,position={},expires=9999,golden=true}}
    Yule_Tick();Yule_Tick()
    assert(YULE.wallets[1]==i and #rewards==i and rewards[i]==i and #YULE.presents==0)
end
YULE_CONFIG.presentWeights={0,0,0,0}
World_GetRand=function() error('Disabled bonuses must not roll') end
YULE.presents={{id=5,entity=5,position={},expires=9999}}
Yule_Tick();assert(YULE.wallets[1]==5 and #rewards==4)
assert(YULE.wallets[8]==nil and YULE.wallets[2]==nil)
''')

rdo = E.parse(root / 'assets/scar/winconditions/ags_game_mode.rdo')
objects = list(rdo.iter('DataObject'))
ids = {o.get('Id') for o in objects}
assert len(ids) == len(objects)
for key, expected in [('section_yuletide', 6), ('section_yuletide_wallets', 5), ('section_yuletide_wallets_high', 4)]:
    section = next(o for o in objects if o.find(f'./DataProperty[@Name="m_key"][@Value="{key}"]') is not None)
    options = section.findall('./DataProperty[@Name="m_options"]/DataObject')
    assert len(options) == expected
    for o in options:
        items = o.findall('./DataProperty[@Name="m_enumItems"]/DataObject')
        assert sum(i.find('./DataProperty[@Name="m_isDefaultValue"]').get('Value') == 'true' for i in items) == 1
        assert all(i.get('OwnerId') == o.get('Id') for i in items)
print('PASS: compact lobby groups, old/new eight-slot wallets, four bells at 55/56/57/58, 60-second arrival and 180-second cadence, guaranteed tokens and weighted outcomes.')

# Verify the lobby defaults agree with the runtime fallback distribution.
for key, expected in [('team_gold_weight',60),('enemy_gold_weight',20),('gold_deposit_weight',10),('stone_deposit_weight',10)]:
    option=next(o for o in objects if o.find(f'./DataProperty[@Name="m_key"][@Value="{key}"]') is not None)
    default=next(i for i in option.findall('./DataProperty[@Name="m_enumItems"]/DataObject') if i.find('./DataProperty[@Name="m_isDefaultValue"]').get('Value')=='true')
    assert default.find('./DataProperty[@Name="m_key"]').get('Value')==f'yule_value_{expected}'
