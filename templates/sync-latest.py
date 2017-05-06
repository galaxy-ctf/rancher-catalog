#!/usr/bin/env python
import os
import sys
import yaml
import glob


for tpl in sorted(glob.glob("*")):
    if '.py' in tpl: continue
    if 'Makefile' in tpl: continue

    # Get the subdirs + files
    contents = glob.glob(os.path.join(tpl, '*'))
    # Filter out files
    contents = [x[len(tpl) + 1:] for x in contents if '.' not in x]
    # Map to integers
    latest = max(map(int, contents))

    with open(os.path.join(tpl, str(latest), 'rancher-compose.yml'), 'r') as handle:
        data = yaml.load(handle)
        config = data['.catalog']

    sys.stderr.write('%20s %s\n' % (tpl, config['version']))

    with open(os.path.join(tpl, 'config.yml'), 'r+') as handle:
        main_conf = yaml.load(handle)
        for prop in ('name', 'description', 'version'):
            if prop in config:
                main_conf[prop] = str(config[prop]).strip()

        handle.seek(0)
        handle.truncate()
        yaml.dump(main_conf, handle, default_flow_style=False)
