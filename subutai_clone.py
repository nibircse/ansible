#!/usr/bin/python

ANSIBLE_METADATA = {
    'metadata_version': '1.0',
    'status': ['preview'],
    'supported_by': 'curated'
}

DOCUMENTATION = '''
---
module: subutai_clone

short_description: subutai clone module

version_added: "2.5"

description:
    - "clone containers in subutai"

options:
    parent:
        description:
            - name of parent
        required: true
    child:
        description:
            - name of child
        required: true
    env:
        description:
            - env id
        required: false
    ipaddr:
        description:
            - ip address
        required: false
    token:
        description:
            - token
        required: false
    kurjun_token:
        description:
            - kurjun token
        required: false

extends_documentation_fragment
    - subutai

author:
    - Fernando Silva (fsilva@optimal-dynamics.com)
'''

EXAMPLES = '''
# clone container
- name: clone nginx container
  subutai_clone:
    parent: nginx
    child: nginx2
    
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
        parent=dict(type='str', required=True),
        child=dict(type='str', required=False),
        env=dict(type='str', required=False),
        ipaddr=dict(type='str', required=False),
        token=dict(type='str', required=False),
        kurjun_token=dict(type='str', required=False),
        
    )

    # skell to result
    result = dict(
        changed=False,
        parent='',
        env='', 
        child='',
        ipaddr='', 
        token='',
        kurjun_token='',
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    # check mode, don't made any changes
    if module.check_mode:
        return result

    result['parent'] = module.params['parent']
    result['child'] =  module.params['child']
    result['env'] =  module.params['env']
    result['ipaddr'] = module.params['ipaddr']
    result['token'] = module.params['token']
    result['kurjun_token'] =  module.params['kurjun_token']

    args=[]
    if module.params['env']:
        args.append("--env")
        args.append(module.params['env'])

    if module.params['ipaddr']:
        args.append("--ipaddr")
        args.append(module.params['ipaddr'])

    if module.params['token']:
        args.append("--token")
        args.append(module.params['token'])

    if module.params['kurjun_token']:
        args.append("--kurjun_token")
        args.append(module.params['kurjun_token'])

    out = subprocess.Popen(["/snap/bin/subutai","clone", module.params['parent'], module.params['child']] + args, stdout=subprocess.PIPE).stdout.read()
    
    result['changed'] = True

    module.exit_json(**result)

def main():
    run_module()

if __name__ == '__main__':
    main()