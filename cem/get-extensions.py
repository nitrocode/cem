#!/usr/bin/env python3
import json
from pathlib import Path


home = str(Path.home())
pref_loc = f'{home}/.config/chromium/Default/Preferences'
with open(pref_loc, 'rb') as f:
    json_pref = f.read()
json_prefd = json.loads(json_pref)
extension_uids = [*json_prefd['protection']['macs']['extensions']['settings'].keys()]
for uid in extension_uids:
    print(uid)
