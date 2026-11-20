"""Show only the local player's applied bonuses and engine-reported cap."""
from pathlib import Path
import xml.etree.ElementTree as ET
from lupa import LuaRuntime

root=Path(__file__).resolve().parents[1]
lua=LuaRuntime()
lua.execute('Core_RegisterModule=function() end; AGS_Print=function() end')
for name in ('ags_global_settings.scar','gameplay/ags_handicaps.scar',
             'gameplay/ags_population_capacity.scar','specials/ags_bonus_hud.scar'):
    lua.execute((root/'assets/scar'/name).read_text(encoding='utf-8-sig'))
lua.execute(r'''
local slots={[11]=1,[22]=2,[88]=8}
PLAYERS={{id=88},{id=22},{id=11}}
Player_GetSlotIndex=function(id) return slots[id] end
AGS_GLOBAL_SETTINGS.PlayerHandicaps.Economic.SecondSlot=1.5
AGS_GLOBAL_SETTINGS.PlayerHandicaps.Military.SecondSlot=1.25
AGS_GLOBAL_SETTINGS.PlayerPopulationCaps.SecondSlot=250
CT_Personnel=1; cap=200
Player_GetMaxPopulationCapOverride=function(id,kind) assert(id==22 and kind==1); return cap end
local data=AGS_BonusHUD_Data(PLAYERS[2])
assert(data.text=='Eco pending\nMilitary pending\nPop 200 / 250')
assert(data.visibility=='Visible' and data.colour=='#FFFFC567')
-- Exercise the real application functions before reporting bonuses as applied.
MAT_EntityType=1; MUT_Multiplication=2; MUT_Addition=3
AGS_BP_BUILDING='building'; AGS_BP_WORKER='worker'; AGS_BP_UNIT_CLASS='unit'
BP_GetEntityBlueprintsWithType=function(kind) return {{PropertyBagGroupID=kind}} end
Modifier_Create=function(scope,name,usage,exclusive,value,bp) return {name=name,value=value} end
applied=0
Modifier_ApplyToPlayer=function(m,id) assert(id==22); applied=applied+1 end
Player_ClearPopCapOverride=function(id) assert(id==22); cap=250 end
AGS_Handicaps_OnPlay(); AGS_PopulationCapacity_OnPlay()
assert(applied==19)
data=AGS_BonusHUD_Data(PLAYERS[2])
assert(data.text=='Eco +50%\nMilitary +25%\nPop 250' and data.colour=='#FFE1E7DE')
assert(AGS_BonusHUD_Data(PLAYERS[1]).visibility=='Collapsed')
assert(AGS_BonusHUD_Data(PLAYERS[3]).visibility=='Collapsed')
-- Display engine changes, including a mismatch, rather than echoing configuration.
cap=200; assert(AGS_BonusHUD_Data(PLAYERS[2]).text:find('Pop 200 / 250',1,true))
cap=325; PLAYERS[2].AGS_Team={index=3}; AGS_TEAM_BALANCE_TEAM_BONUS={[3]=75}
assert(AGS_BonusHUD_Data(PLAYERS[2]).text:find('Pop 325',1,true))
assert(AGS_BonusHUD_Data(PLAYERS[2]).colour=='#FFE1E7DE')

replay=false; localPlayer=22; rules={}; children=0
UI_IsReplay=function() return replay end
Game_GetLocalPlayer=function() return localPlayer end
UI_CreateDataContext=function(data) return data end
UI_AddChild=function(parent,kind,id,props)
    assert(parent=='ScarNotReplay' and id=='AGS_BonusHUD' and props.IsHitTestVisible==false)
    children=children+1; capturedXaml=props.Xaml
end
UI_SetDataContext=function(id,data) assert(id=='AGS_BonusHUD'); context=data end
Rule_Exists=function(f) return rules[f]~=nil end
Rule_AddInterval=function(f,n) assert(n==1 and not rules[f]); rules[f]=true end
Rule_Remove=function(f) rules[f]=nil end
AGS_BonusHUD_OnPlay(); assert(children==1 and context.text:find('Eco +50%',1,true))
AGS_BonusHUD_OnPlay(); assert(children==1) -- no duplicate panel or timer
localPlayer=11; AGS_BonusHUD_Update(); assert(context.visibility=='Collapsed')
localPlayer=22; AGS_BonusHUD_Update(); assert(context.visibility=='Visible')
PLAYERS[2].isEliminated=true; AGS_BonusHUD_Update(); assert(context.visibility=='Collapsed')
PLAYERS[2].isEliminated=false
AGS_BonusHUD_OnGameRestore(); assert(children==2 and context.visibility=='Visible')
replay=true; AGS_BonusHUD_Update(); assert(context.visibility=='Collapsed')
AGS_BonusHUD_OnGameRestore(); assert(children==2)
replay=false; AGS_BonusHUD_OnPlay(); assert(children==3)
AGS_BonusHUD_OnGameOver(); assert(context.visibility=='Collapsed' and next(rules)==nil)
''')
xaml=ET.fromstring(lua.globals().capturedXaml)
assert xaml.get('IsHitTestVisible')=='False'
print('PASS: own-player applied bonuses, live cap/mismatch, team transfer, hidden defaults, defeat/replay hiding, restore and non-blocking XAML.')
