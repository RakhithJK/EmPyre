from lib.common import helpers
import os
import string


class Module:

    def __init__(self, mainMenu, params=[]):

        # metadata info about the module, not modified during runtime
        self.info = {
            # name for the module that will appear in module menus
            'Name': 'SOCKSv5 proxy',

            # list of one or more authors for the module
            'Author': ['@klustic'],

            # more verbose multi-line description of the module
            'Description': ('Extend a SOCKSv5 proxy into your target network'),

            # True if the module needs to run in the background
            'Background': True,

            # File extension to save the file as
            # no need to base64 return data
            'OutputExtension': None,

            'NeedsAdmin': False,

            # True if the method doesn't touch disk/is reasonably opsec safe
            'OpsecSafe': True,

            # list of any references/other comments
            'Comments': [
                'Modified from: https://github.com/klustic/AlmondRocks',
                'Use the server found in that Github repo with this module.'
            ]
        }

        # any options needed by the module, settable during runtime
        self.options = {
            # format:
            #   value_name : {description, required, default_value}
            'Agent': {
                # The 'Agent' option is the only one that MUST be in a module
                'Description'   :   'Agent to proxy through',
                'Required'      :   True,
                'Value'         :   ''
            },
            'HOST': {
                'Description'   :   'Host running the AlmondRocks server',
                'Required'      :   True,
                'Value'         :   ''
            },
            'PORT': {
                'Description'   :   'AlmondRocks server port',
                'Required'      :   True,
                'Value'         :   ''
            },
            'NoSSL': {
                'Description'   :   'Disable SSL (NOT RECOMMENDED!)',
                'Required'      :   False,
                'Value'         :   'false'
            }
        }

        self.mainMenu = mainMenu
        if params:
            for option, value in params:
                if option in self.options:
                    self.options[option]['Value'] = value

    def generate(self):
        moduleSource = os.path.join(self.mainMenu.installPath, 'data/module_source/socks_source.py')
        try:
            with open(moduleSource) as f:
                script_template = string.Template(f.read())
        except Exception as e:
            print helpers.color('[!] Error reading {}: {}'.format(str(moduleSource), e))
            return ""

        options = {x.lower(): y for x, y in self.options.items()}
        host = options.get('host', {}).get('Value')
        port = options.get('port', {}).get('Value')
        if options.get('nossl', {}).get('Value', 'false').lower() == 'true':
            no_ssl = True
        else:
            no_ssl = False

        return script_template.substitute(host=host, port=port, no_ssl=no_ssl)