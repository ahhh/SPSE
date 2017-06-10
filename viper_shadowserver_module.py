# This file is part of Viper - https://github.com/viper-framework/viper
# Ahhh template module

import os
import requests


from viper.common.out import cyan
from viper.common.abstracts import Module
from viper.core.session import __sessions__


class shadowserver(Module):
    cmd = 'shadowserver'
    description = 'checks ShadowServer for intel on the IOC'
    authors = ['ahhh', 'Dan Borges']

    def __init__(self):
        super(shadowserver, self).__init__()

    def run(self):
        super(shadowserver, self).run()

        if not __sessions__.is_set():
            self.log('error', "No open session")
            return

        if os.path.exists(__sessions__.current.file.path):
            filehash = __sessions__.current.file.md5
            try:
                url = "https://innocuous.shadowserver.org/api/?query=" + filehash
                results = requests.get(url)
                self.log('info', 'ShadowServer Results: %s' % (results.text))
            except:
              self.log('error', 'Issues calling ShadowServer')            
        else:
            self.log('error', 'No file found')
