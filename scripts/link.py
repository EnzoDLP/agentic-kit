#!/usr/bin/env python3
"""Link the kit's layers into the project that holds it at .claude/agentic-kit.

Run from the project root:
    python3 .claude/agentic-kit/scripts/link.py [--local | --shared] [<layer>...]
    python3 .claude/agentic-kit/scripts/link.py --remove

`workflow` is always linked, and a layer brings the layers it requires. Given layers replace the
previous selection (links to layers no longer selected are removed); given none, the previous
selection is kept, which is how links are refreshed after updating the kit. Changes apply from the
next Claude Code session.

--local keeps everything off git: permissions go to .claude/settings.local.json and every path the
kit writes is listed in the repository's exclude file. The mode is remembered (and detected when
the kit folder itself is excluded), so later runs need no flag; --shared switches back.
"""
import json
import os
import subprocess
import sys

KIT = os.path.join('.claude', 'agentic-kit')
REL = os.path.join('..', 'agentic-kit')  # from .claude/<kind>/ to the kit
KINDS = ('rules', 'skills', 'agents')
STATE = os.path.join('.claude', 'agentic-kit.state.json')  # mode, layers, rules last written
SETTINGS = {False: os.path.join('.claude', 'settings.json'),
            True: os.path.join('.claude', 'settings.local.json')}
OPTIONS = {'--local', '--shared', '--remove'}


def die(msg):
    sys.exit(f'link.py: {msg}')


def read_json(path, default):
    return json.load(open(path)) if os.path.exists(path) else default


def write_json(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as fh:
        json.dump(data, fh, indent=2)
        fh.write('\n')


def layers_available():
    root = os.path.join(KIT, 'layers')
    return sorted(d for d in os.listdir(root) if os.path.isdir(os.path.join(root, d)))


def resolve(selected):
    """Selected layers plus what they require, workflow first."""
    out, todo = [], ['workflow', *selected]
    while todo:
        layer = todo.pop(0)
        if layer in out:
            continue
        if layer not in layers_available():
            die(f'unknown layer "{layer}" (available: {", ".join(layers_available())})')
        out.append(layer)
        req = os.path.join(KIT, 'layers', layer, 'requires')
        if os.path.exists(req):
            todo += [line.strip() for line in open(req) if line.strip()]
    return out


def wanted_links(layers):
    """{link path: relative target} for every rules folder, skill and agent of the layers."""
    links = {}
    for layer in layers:
        src = os.path.join(KIT, 'layers', layer)
        if os.path.isdir(os.path.join(src, 'rules')):
            links[os.path.join('.claude', 'rules', f'kit-{layer}')] = os.path.join(
                REL, 'layers', layer, 'rules')
        skills = os.path.join(src, 'skills')
        for skill in sorted(os.listdir(skills)) if os.path.isdir(skills) else []:
            if os.path.isdir(os.path.join(skills, skill)):
                links[os.path.join('.claude', 'skills', f'{layer}-{skill}')] = os.path.join(
                    REL, 'layers', layer, 'skills', skill)
        agents = os.path.join(src, 'agents')
        for agent in sorted(os.listdir(agents)) if os.path.isdir(agents) else []:
            links[os.path.join('.claude', 'agents', agent)] = os.path.join(
                REL, 'layers', layer, 'agents', agent)
    return links


def existing_kit_links():
    found = []
    for kind in KINDS:
        folder = os.path.join('.claude', kind)
        for name in os.listdir(folder) if os.path.isdir(folder) else []:
            path = os.path.join(folder, name)
            if os.path.islink(path) and os.readlink(path).startswith(REL + os.sep):
                found.append(path)
    return found


def apply_links(links):
    """Check every conflict first, so that a refused run changes nothing."""
    for path, target in links.items():
        if os.path.lexists(path) and not (os.path.islink(path) and os.readlink(path) == target):
            if not (os.path.islink(path) and os.readlink(path).startswith(REL + os.sep)):
                die(f'{path} exists and is not a kit link: move it, then run again')
    for path in existing_kit_links():
        if links.get(path) != os.readlink(path):
            os.remove(path)
    for path, target in links.items():
        if not os.path.lexists(path):
            os.makedirs(os.path.dirname(path), exist_ok=True)
            os.symlink(target, path)


def kit_permissions(layers):
    rules = {}
    for layer in layers:
        f = os.path.join(KIT, 'layers', layer, 'permissions.json')
        for kind, items in read_json(f, {'permissions': {}})['permissions'].items():
            rules.setdefault(kind, [])
            rules[kind] += [i for i in items if i not in rules[kind]]
    return rules


def apply_permissions(local, layers, previous):
    """Replace the kit's rules, keep every other rule as it is.

    The kit's rules are those of the current kit plus those written last time (a rule a newer kit
    dropped is removed too). Both settings files are cleaned, so switching mode leaves nothing.
    """
    ours = {r for rs in kit_permissions(layers_available()).values() for r in rs}
    ours |= {r for rs in previous.get('permissions', {}).values() for r in rs}
    wanted = kit_permissions(layers)
    for is_local, path in SETTINGS.items():
        if not os.path.exists(path) and (is_local != local or not layers):
            continue
        data = read_json(path, {})
        perms = data.setdefault('permissions', {})
        for kind in ('ask', 'deny'):
            perms[kind] = [r for r in perms.get(kind, []) if r not in ours]
            if is_local == local:
                perms[kind] += wanted.get(kind, [])
            if not perms[kind]:
                del perms[kind]
        if not perms:
            del data['permissions']
        write_json(path, data)
    return wanted


def exclude_file():
    out = subprocess.run(['git', 'rev-parse', '--git-path', 'info/exclude'],
                         capture_output=True, text=True)
    if out.returncode != 0:
        die('not inside a git repository')
    return out.stdout.strip()


def kit_is_excluded():
    path = exclude_file()
    return os.path.exists(path) and '/' + KIT in open(path).read().splitlines()


def exclude(paths):
    path = exclude_file()
    present = open(path).read().splitlines() if os.path.exists(path) else []
    new = ['/' + p for p in paths if '/' + p not in present]
    if new:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'a') as fh:
            fh.write('\n'.join(['# agentic-kit (local)', *new]) + '\n')


def main(argv):
    unknown = [a for a in argv if a.startswith('-') and a not in OPTIONS]
    if unknown:
        die(f'unknown option {unknown[0]} (options: {", ".join(sorted(OPTIONS))})')
    if '--local' in argv and '--shared' in argv:
        die('--local and --shared are exclusive')
    selected = [a for a in argv if not a.startswith('-')]
    remove = '--remove' in argv
    if remove and selected:
        die('--remove takes no layer: it removes them all')
    if not os.path.isdir(os.path.join(KIT, 'layers')):
        die(f'run from the project root, with the kit at {KIT}')

    previous = read_json(STATE, {})
    if '--local' in argv or '--shared' in argv:
        local = '--local' in argv
    elif 'local' in previous:
        local = previous['local']
    else:
        local = kit_is_excluded()

    current = previous.get('layers') or [  # no state file: read the selection from the links
        os.path.basename(p)[len('kit-'):] for p in existing_kit_links()
        if os.path.dirname(p) == os.path.join('.claude', 'rules')]
    layers = [] if remove else resolve(selected or current)
    links = wanted_links(layers)
    apply_links(links)
    wanted = apply_permissions(local, layers, previous)
    if remove:
        if os.path.exists(STATE):
            os.remove(STATE)
        print('Kit links and permissions removed. The kit folder itself is left in place.')
        return
    write_json(STATE, {'local': local, 'layers': layers, 'permissions': wanted})
    if local:
        exclude([KIT, SETTINGS[True], STATE, *sorted(links)])
    print(f'Linked ({"local" if local else "shared"}): {", ".join(layers)} '
          f'({len(links)} links, permissions in {SETTINGS[local]}).')
    print('Start a new Claude Code session to load them.')


if __name__ == '__main__':
    main(sys.argv[1:])
