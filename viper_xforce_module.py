# This file is part of Viper - https://github.com/viper-framework/viper
# Ahhh xforce integration

import os
import requests
import json
import base64

from viper.common.out import cyan
from viper.common.abstracts import Module
from viper.core.session import __sessions__
from viper.core.config import Config

cfg = Config()


class xforce(Module):
    cmd = 'xforce'
    description = 'checks xforce for intel on the IOC'
    authors = ['ahhh', 'Dan Borges']

    def __init__(self):
        super(xforce, self).__init__()

    def run(self):
        super(xforce, self).run()
		# Get our keys
        self.key = cfg.xforce.xforce_key
        if self.key is None:
            self.log('error', 'This command requires you configure your key and password in the conf file')
            return
        self.password = cfg.xforce.xforce_password
        if self.password is None:
            self.log('error', 'This command requires you configure your key and password in the conf file')
            return
        # Check our session
        if not __sessions__.is_set():
            self.log('error', "No open session")
            return
        # Get our md5
        if os.path.exists(__sessions__.current.file.path):
            filehash = __sessions__.current.file.md5
            # Query xforce			
            try:
                url = "https://api.xforce.ibmcloud.com/malware/" + filehash
                token = base64.b64encode(self.key + ":" + self.password)
                headers = {'Authorization': "Basic " + token, 'Accept': 'application/json'}
                response = requests.get(url, params='', headers=headers, timeout=20)
                all_json = response.json()
                results = json.dumps(all_json, indent=4, sort_keys=True) 
                self.log('info', 'XForce Results: %s' % (results))
                return				
            except:
              self.log('error', 'Issues calling XForce')
              return			  
        else:
            self.log('error', 'No file found')
            return

