#!/usr/bin/python
# Copyright (c) 2021, Sine Nomine Associates
# BSD 2-Clause License

ANSIBLE_METADATA = {
    'metadata_version': '1.1.',
    'status': ['preview'],
    'supported_by': 'community',
}

DOCUMENTATION = r"""
---
module: openafs_selinux_relabel
short_description: Relabel selinux context for server files.
description:
  - Relabel the server directories after the files have been installed
    and the configuration files updated.
  - Relabel the partition directories and the AlwaysAttach file, when present.
  - Safe the list of directories relabelled in the openafs local facts file
    to avoid running restorecon on subsequent plays.
"""

EXAMPLES = r"""
- name: Relabel
  become: yes
  openafs_selinux_relabel:
"""

RETURN = r"""
"""

import glob
import json
import logging
import logging.handlers
import os
import pprint

from ansible.module_utils.basic import AnsibleModule

log = logging.getLogger('openafs_selinux_relabel')

def setup_logging():
    level = logging.INFO
    fmt = '%(levelname)s %(name)s %(message)s'
    address = '/dev/log'
    if not os.path.exists(address):
        address = ('localhost', 514)
    facility = logging.handlers.SysLogHandler.LOG_USER
    formatter = logging.Formatter(fmt)
    handler = logging.handlers.SysLogHandler(address, facility)
    handler.setFormatter(formatter)
    log.addHandler(handler)
    log.setLevel(level)

# Note: The bosserver creates the /usr/vice/etc directory if it does not
# exist in order to create a symlink to the server configuration. Be sure
# to set the selinux context on /usr/vice before the bosserver starts.
top_dirs = ['/usr/afs', '/usr/vice']

def main():
    setup_logging()
    results = dict(
        changed=False,
    )
    module = AnsibleModule(
            argument_spec=dict(
            ),
            supports_check_mode=False,
    )
    log.info('Parameters: %s', pprint.pformat(module.params))

    def restorecon(*args):
        restorecon = module.get_bin_path('restorecon', required=True)
        cmdargs = [restorecon] + list(args)
        cmdline = ' '.join(cmdargs)
        log.info("Running: %s", cmdline)
        rc, out, err = module.run_command(cmdargs)
        if rc != 0:
            log.error("Command failed: %s, rc=%d, err=%s", cmdline, rc, err)
            module.fail_json(msg="Command failed", cmd=cmdline, out=out, err=err)

    factsfile = '/etc/ansible/facts.d/openafs.fact'
    try:
        with open(factsfile) as fp:
            facts = json.load(fp)
    except:
        facts = {}

    changed = []
    relabelled = facts.get('relabelled', [])

    for path in top_dirs:
        if not os.path.exists(path):
            os.makedirs(path)
        if path not in relabelled:
            restorecon('-i', '-r', path)
            changed.append(path)

    for path in glob.glob('/vicep*'):
        if path not in relabelled:
            restorecon('-i', path)
            changed.append(path)

    for path in glob.glob('/vicep*/AlwaysAttach'):
        if path not in relabelled:
            restorecon(path)
            changed.append(path)

    if changed:
        facts['relabelled'] = sorted(set(relabelled) | set(changed))
        if not os.path.exists(os.path.dirname(factsfile)):
            os.makedirs(os.path.dirname(factsfile))
        with open(factsfile, 'w') as fp:
            json.dump(facts, fp, indent=2)
        results['changed'] = True

    log.info('Results: %s', pprint.pformat(results))
    module.exit_json(**results)

if __name__ == '__main__':
    main()
