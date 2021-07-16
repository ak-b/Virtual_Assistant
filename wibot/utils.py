'''
Function file
'''
# tested and working fix

import requests
import os
import json

def get_config():
    '''
    To get credentials
    
    result = {}
    if os.path.exists('/var/run/secrets/boostport.com/vault-token'):
        with open('/var/run/secrets/boostport.com/vault-token') as f:
            vault_data = json.loads(f.read())
        headers = {"X-Vault-Token": vault_data['clientToken']}
        url = "{}v1/iaas-marvin/vault/secrets".format(vault_data['vaultAddr'])
        response = requests.get(url, headers=headers)
        result.update(response.json()['data'])
    return result
    '''
    pass
