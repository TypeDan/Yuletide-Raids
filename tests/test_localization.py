"""Catch text references that require another mod's localization to be installed."""
from pathlib import Path
import csv
import re
import uuid
import xml.etree.ElementTree as E

root = Path(__file__).resolve().parents[1]
project = E.parse(root / 'Yuletide Raids.aoe4mod')
identity = uuid.UUID(next(n.text for n in project.iter() if n.tag.endswith('}ID')))
parts = tuple(int.from_bytes(identity.bytes_le[i:i+4], 'little') for i in range(0,16,4))
with (root / 'assets/locdb/More Advanced Game Settings_en.csv').open(encoding='utf-8-sig', newline='') as f:
    rows = list(csv.reader(f))[1:]
strings = {row[0]: row[-1] for row in rows if row}
assert len(strings) == len(rows), 'Duplicate English string IDs'
checked = 0
for path in (root / 'assets').rglob('*'):
    if path.suffix not in ('.scar', '.rdo', '.xml', '.xaml'):
        continue
    text = path.read_text(encoding='utf-8-sig')
    for guid, key in re.findall(r'\$([\da-fA-F]{32}):(\d+)', text):
        assert guid.lower() == identity.hex, f'{path}: external mod text namespace {guid}'
        assert strings.get(key), f'{path}: missing English string {key}'
        checked += 1
    if path.suffix == '.scar':
        for key in re.findall(r'Yule_Notify\((\d+)\)', text):
            assert strings.get(key), f'{path}: missing event string {key}'
            checked += 1
    if path.suffix == '.rdo':
        for obj in E.fromstring(text).iter('DataObject'):
            if obj.get('Type') != 'util::ReflectLocString':
                continue
            actual = tuple(int(obj.find(f'./DataProperty[@Name="m_modPart{i}"]').get('Value')) for i in range(4))
            assert actual == parts, f'{path}: external descriptor text namespace {actual}'
            key = obj.find('./DataProperty[@Name="m_locStringKey"]').get('Value')
            assert strings.get(key), f'{path}: missing descriptor string {key}'
            checked += 1
main = (root / 'assets/scar/christmas/yuletide.scar').read_text()
assert f'YULE_LOC = "${identity.hex}:"' in main
assert checked > 2000, 'Localization scan unexpectedly incomplete'
print(f'PASS: {checked} text references resolve inside Yuletide with English strings; no other mod required.')
