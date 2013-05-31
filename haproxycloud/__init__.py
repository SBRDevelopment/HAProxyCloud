import yaml
import logging
import os
import sys
import subprocess
import glob

from mako.template import Template

from haproxycloud.cloud import get_instances
from haproxycloud.utils import merge_array_recursive

__version__ = "0.0.1"

logging.getLogger().setLevel(logging.INFO)

class HAProxyCloud(object):
    
    def __init__(self, args):
        self._config = {}
        self._output = None
        self._load_config(args.config)
    
    def _load_config(self, path):
    
        for yaml_file in glob.glob(path):
            
            config = {}
            with open(yaml_file) as config_file:
                config = yaml.load(config_file)
            
            if config is not None:
                self._config = merge_array_recursive(self._config, config)
        
                if 'include' in config:
                    for include in config['include']:
                        self._load_config(include)
    
    def _generate_configuration(self):
        frontends = self._config.get('frontend', {})
        backends = self._config.get('backend', {})
        
        for backend in backends.values():
            backend['instances'] = get_instances(backend.get('tags', None))
        
        return Template(filename=self._config['template']).render(frontends=frontends, backends=backends)
    
    def has_changed(self):
        self._output = self._generate_configuration()
        
        current_configuration = ''
        if os.path.isfile(self._config['output']):
            with open(self._config['output'], 'r') as ifstream:
                current_configuration = ifstream.read()
                
        if current_configuration != self._output:
            logging.info("HAProxyCloud has detected changes in the haproxy configuration.")
            return True
        else:
            logging.info("HAProxyCloud has not detected any changes to the haproxy configuration.")
            return False
    
    def test_configuration(self, config_file):
        command = '''/usr/sbin/haproxy -f %s -c''' % config_file
        return subprocess.call(command.split(' ')) == 0
    
    def update_configuration(self):
        out_file = self._config['output']
        tmp_file = out_file + ".tmp"
        
        # Save the new file contents to a temp file
        with open(tmp_file, 'w') as ofstream:
            ofstream.write(self._output)
            
        # First check to make sure the  
        if self.test_configuration(tmp_file):
            
            # Rename the configuration
            os.rename(out_file, out_file + ".orig")
            logging.info("HAProxy configuration renamed to %s" % out_file + ".orig")
            
            # Rename the temp file
            os.rename(tmp_file, out_file)
            logging.info("HAProxy configuration updated")
                        
        else:
            logging.error("HAProxy configuration is invalid configuration file will not be updated.")
            sys.exit(1)
            
    def reload(self):
        command = '''service haproxy reload'''
        logging.info("HAProxy restarted")
        return subprocess.call(command.split(' '))