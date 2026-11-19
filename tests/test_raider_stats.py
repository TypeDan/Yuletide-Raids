from pathlib import Path
import xml.etree.ElementTree as E
import math
root=Path(__file__).resolve().parents[1]
base=root/'assets/attrib/instances'
# Native tiers, available upgrades, then +20% health and +10% base weapon damage.
expected={
 'archer':[(55,6,0,0),(70,7,1,1),(80,10,2,2),(95,14.4,3,3)],
 'spearman':[(80,7,0,0),(90,9,1,1),(110,11,2,2),(161,16.1,3,3)],
 'manatarms':[(100,8,2,3),(120,11,4,4),(155,14,6,6),(207,19.55,8,9)],
}
for kind,rows in expected.items():
 for age,(hp,attack,melee,ranged) in enumerate(rows,1):
  r=E.parse(base/f'ebps/christmas/yule_{kind}_{age}.xml').getroot()
  h=r.find('./list/template_reference[@value="ebpextensions\\health_ext"]')
  assert math.isclose(float(h.find('float[@name="hitpoints"]').get('value')),hp*1.2)
  assert h.find('enum[@name="allegiance_override"]').get('value')=='enemy_to_all'
  for name,value in [('Melee',melee),('Ranged',ranged)]:
   assert float(h.find(f'./enum_table/float[@name="{name}"]').get('value'))==value
  refs=r.findall('.//instance_reference[@name="non_entity_weapon_wrapper_pbg"]')
  primary=refs[0];assert primary.get('mod')=='7a91e5eaf5e04afb92278936ca4d8a0c'
  weapon=E.parse(base/(primary.get('value').replace('\\','/')+'.xml')).getroot()
  for bound in ['min','max']:
   assert math.isclose(float(weapon.find(f'./group/group[@name="damage"]/float[@name="{bound}"]').get('value')),attack*1.1)
  for ref in refs:
   if ref.get('mod'):
    wr=E.parse(base/(ref.get('value').replace('\\','/')+'.xml')).getroot()
    parent=wr.find('instance_reference[@name="parent_pbg"]').get('value')
    if kind=='spearman' and age==1:assert 'spearman_2' not in parent and 'spearwall_2' not in parent
    if age<4:assert 'incendiary_4' not in parent
main=(root/'assets/scar/christmas/yuletide.scar').read_text()
assert 'Yule_UpgradeRaider' not in main and 'Entity_CompleteUpgrade' not in main
print('PASS: all 12 age stat sets, neutral hostility, native Dark Age spear weapons, no future tier or runtime upgrade dependency.')
