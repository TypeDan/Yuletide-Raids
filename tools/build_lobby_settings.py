"""Generate Yuletide lobby controls using the game's existing enum descriptors."""
from pathlib import Path
import csv
import hashlib
import xml.etree.ElementTree as E

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / 'assets/scar/winconditions/ags_game_mode.rdo'
tree = E.parse(PATH)
sections = tree.find('.//DataProperty[@Name="m_optionSections"]')
owner = tree.find('.//DataObject[@Type="WinCondition::OptionsUIDescriptor"]').get('Id')
parts = {f'm_modPart{i}': n for i, n in enumerate([2056381930, 1258026464, 914958226, 210390474])}
strings = {
    '2004': 'Enemy gift! Enemies share a gold pot; your team shares the deduction, scaled by the collector\'s age.',
    '2008': 'Father Christmas arrives in 5 seconds!',
    '2011': 'Collect one golden token plus a random bonus outcome. Outcome chances are set in the lobby. Deposits appear on nearby clear ground.',
    '2015': 'Father Christmas and his nine reindeer deliver golden presents. First visit at 1:00, then every three minutes. Blocked convoys phase to clear ground.',
    '2021': 'Collect one golden token plus a random bonus outcome. Spend the token in the Golden presents menu.',
}

def uid(key):
    return str(int.from_bytes(hashlib.sha256(('yuletide-lobby:' + key).encode()).digest()[:8], 'big'))

def prop(parent, name, kind, value=None):
    attrs = dict(Name=name, Type=kind)
    if value is not None:
        attrs['Value'] = str(value)
    return E.SubElement(parent, 'DataProperty', attrs)

def loc(parent, field, key, text):
    strings[str(key)] = text
    field_id = uid(parent.get('Id') + ':' + field)
    p = prop(parent, field, 'Object')
    E.SubElement(p, 'DataValue', Name='util::ReflectLocString').text = field_id
    o = E.SubElement(p, 'DataObject', Name='', Type='util::ReflectLocString', Id=field_id, OwnerId=parent.get('Id'))
    for name, value in parts.items():
        prop(o, name, 'UInt32', value)
    prop(o, 'm_locStringKey', 'Int32', key)

def section(key, label_id, label):
    ident = uid(key)
    for child in list(sections):
        if child.get('Id') == ident or child.tag == 'DataValue' and child.text == ident:
            sections.remove(child)
    E.SubElement(sections, 'DataValue', Name='WinCondition::OptionSectionUIDescriptor').text = ident
    o = E.SubElement(sections, 'DataObject', Name='', Type='WinCondition::OptionSectionUIDescriptor', Id=ident, OwnerId=owner)
    prop(o, 'm_featured', 'Bool', 'false')
    prop(o, 'm_key', 'String', key)
    options = prop(o, 'm_options', 'Object')
    loc(o, 'm_feName', label_id, label)
    return o, options

def option(section, key, label_id, label, help_text, values, default):
    owner, options = section
    ident = uid(key)
    E.SubElement(options, 'DataValue', Name='WinCondition::EnumerationOptionUIDescriptor').text = ident
    o = E.SubElement(options, 'DataObject', Name='', Type='WinCondition::EnumerationOptionUIDescriptor', Id=ident, OwnerId=owner.get('Id'))
    prop(o, '#BaseTypes', 'String', 'WinCondition::OptionUIDescriptor#0|')
    prop(o, 'm_key', 'String', key)
    items = prop(o, 'm_enumItems', 'Object')
    for value in values:
        item_id = uid(key + ':' + str(value))
        E.SubElement(items, 'DataValue', Name='WinCondition::OptionEnumItemUIDescriptor').text = item_id
        item = E.SubElement(items, 'DataObject', Name='', Type='WinCondition::OptionEnumItemUIDescriptor', Id=item_id, OwnerId=ident)
        prop(item, 'm_key', 'String', f'yule_value_{value}')
        for field in ('m_feSummaryName', 'm_feName'):
            loc(item, field, 4000 + value, 'Default' if value == -1 else str(value))
        prop(item, 'm_isDefaultValue', 'Bool', str(value == default).lower())
        prop(item, 'm_devOnly', 'Bool', 'false')
    loc(o, 'm_feSummaryName', label_id, label)
    loc(o, 'm_feName', label_id, label)
    loc(o, 'm_feDescriptionTooltip', label_id + 1, help_text)

visits = section('section_yuletide', 3100, 'Santa & presents')
for key, label_id, label, default in (
    ('minimum_presents', 3102, 'Minimum gifts', 8),
    ('maximum_presents', 3104, 'Maximum gifts', 12),
):
    option(visits, key, label_id, label,
           'Santa first arrives at 1:00, then every three minutes, with four bell bursts starting five seconds beforehand. Choose 1-20 gifts per visit. Reversed minimum/maximum values are swapped. Every pickup gives one golden token plus a bonus outcome.',
           range(1, 21), default)
for key, label_id, label, default in (
    ('team_gold_weight', 3106, 'Team gold weight', 40),
    ('enemy_gold_weight', 3108, 'Enemy gift weight', 40),
    ('gold_deposit_weight', 3110, 'Gold ore weight', 10),
    ('stone_deposit_weight', 3112, 'Stone ore weight', 10),
):
    option(visits, key, label_id, label,
           'Bonus outcome weight. Defaults 40/40/10/10 give 40%/40%/10%/10%. Chance is this weight divided by the total. Zero disables an outcome; all zero means golden tokens only. Enemy gifts split one 100/150/200/300 gold pot among living enemies and split one equal deduction among your living team, using the collector\'s age. Gold cannot fall below zero; unpaid shares are not charged to other allies.',
           range(0, 101, 5), default)

wallets = section('section_yuletide_wallets', 3120, 'Tokens: players 1-4')
wallets_high = section('section_yuletide_wallets_high', 3140, 'Tokens: players 5-8')
amounts = list(range(21)) + [25, 50, 100]
option(wallets, 'starting_tokens', 3122, 'Default tokens',
       'Golden tokens given to every player at match start unless their lobby-slot override is set. The default is zero.', amounts, 0)
for slot in range(1, 9):
    option(wallets if slot <= 4 else wallets_high, f'starting_tokens_{slot}', 3124 + (slot - 1) * 2, f'Player {slot}',
           f'Starting golden tokens for lobby slot {slot}, including the host and AI. Default uses the Default tokens amount in the players 1-4 group.', [-1] + amounts, -1)

# Put the three compact Yuletide columns before the inherited advanced settings.
# Featured win/game conditions remain in the game's own top row.
custom_ids = {uid(key) for key in ('section_yuletide', 'section_yuletide_wallets', 'section_yuletide_wallets_high')}
custom = [child for child in sections if child.get('Id') in custom_ids or child.tag == 'DataValue' and child.text in custom_ids]
for child in custom:
    sections.remove(child)
for index, child in enumerate(custom):
    sections.insert(index, child)

ids = [o.get('Id') for o in tree.iter('DataObject')]
assert len(ids) == len(set(ids)), 'Duplicate object identifiers'
E.indent(tree, space='  ')
tree.write(PATH, encoding='utf-8', xml_declaration=True)
for path in (ROOT / 'assets/locdb').glob('*.csv'):
    with path.open(encoding='utf-8-sig', newline='') as f:
        rows = list(csv.reader(f))
    existing = {row[0]: row for row in rows[1:] if row}
    for key, value in strings.items():
        if key in existing:
            existing[key][-1] = value
        else:
            rows.append([key] + [''] * (len(rows[0]) - 2) + [value])
    with path.open('w', encoding='utf-8', newline='') as f:
        csv.writer(f).writerows(rows)
print('Generated delivery weights, 1-20 gift bounds, common and eight lobby-slot starting wallets.')
