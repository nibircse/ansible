#!/usr/bin/python

ANSIBLE_METADATA = {
    'metadata_version': '1.0',
    'status': ['preview'],
    'supported_by': 'curated'
}

DOCUMENTATION = '''
---
module: subutai_stop

short_description: subutai stop module

version_added: "2.5"

description:
    - "Stop containers to subutai"

options:
    container:
        description:
            - name of container
        required: true

extends_documentation_fragment
    - subutai

author:
    - Fernando Silva (fsilva@optimal-dynamics.com)
'''

EXAMPLES = '''
# Stop container
- name: Stop management container
  subutai_stop:
    container: management

'''

RETURN = '''
container:
    description: Container affected
    type: str
message:
    description: The output message that the sample module generates
'''

import subprocess
from ansible.module_utils.basic import AnsibleModule

def run_module():

    # parameters
    module_args = dict(
        container=dict(type='str', required=True),
    )

    # skell to result
    result = dict(
        changed=False,
        container='',
        message=''
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    # check mode, don't made any changes
    if module.check_mode:
        return result

    result['container'] = module.params['container']
    
    # verify if container is already stopped
    out = subprocess.Popen(["/snap/bin/subutai","list", "-i", module.params['container'] ], stdout=subprocess.PIPE).stdout.read()
    if bytes("STOPPED") in out:
        result['changed'] = False
        result['message'] = 'already stopped'
        
    else: 
        # try stop container
        err_msg = subprocess.Popen(["/snap/bin/subutai", "stop", module.params['container']], stderr=subprocess.PIPE).stderr.read()
        if err_msg:
            result['message'] = '[Err] ' + err_msg
            result['changed'] = False
            module.fail_json(msg='[Err] ' + err_msg, **result)

        out = subprocess.Popen(["/snap/bin/subutai","list", "-i", module.params['container'] ], stdout=subprocess.PIPE).stdout.read()
        if bytes("STOPPED") in out:
            result['changed'] = True

    module.exit_json(**result)

def main():
    run_module()

if __name__ == '__main__':
    main()