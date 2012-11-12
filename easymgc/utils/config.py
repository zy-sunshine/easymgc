import os
import threading
import simplejson as json
from . import printer

class ConfigNotExistKey(Exception):
    pass

class Config_SubCategory(object):
    def __init__(self, sself, section):
        self.__dict__['confobj'] = sself
        self.__dict__['section'] = section
    
    def __getattr__(self, key):
        confobj = self.__dict__['confobj']
        section = self.__dict__['section']
        #if not confobj.has_option(section, key):
        #    confobj.set(section, key, None)
        #try:
        #ret = self.__dict__['sself'].__dict__['confobj'][section][key]
        ret = confobj[section][key]
        #except:
        #    import pdb;pdb.set_trace()
        return ret

    def __setattr__(self, key, value):
        confobj = self.__dict__['confobj']
        section = self.__dict__['section']
        confobj[section][key] = value
        
    def items(self):
        confobj = self.__dict__['confobj']
        section = self.__dict__['section']
        return confobj[section].items()
        
    def keys(self):
        confobj = self.__dict__['confobj']
        section = self.__dict__['section']
        return confobj[section].keys()
    
class Config(object):
    def __init__(): #@NoSelf
        "disable the __init__ method, and this config class current not thread safely"
    
    __inst = None # make it so-called private

    __lock = threading.Lock() # used to synchronize code

    @staticmethod
    def get_instance():
        Config.__lock.acquire()
        if not Config.__inst:
            Config.__inst = object.__new__(Config)
            object.__init__(Config.__inst)
            printer.d('Config.get_instance --> Create a Config Instance\n')
            Config.__inst.init()
        Config.__lock.release()
        return Config.__inst
        
    def init(self):
        self.__dict__['confobj'] = {}
        self.__dict__['secobjs'] = {}
        conf_file = os.path.dirname(os.path.abspath(__file__))+'/config.json'
        if not os.path.exists(conf_file):
            printer.exception('Config.init --> Cannot load config file %s\n' % conf_file)
        self.load_from_file(conf_file)
        
    def __getattr__(self, key):
        confobj = self.__dict__['confobj']
        secobjs = self.__dict__['secobjs']
        if secobjs.has_key(key):
            return secobjs[key]
        else:
            raise ConfigNotExistKey(key)
        
        
    def save_to_file(self, conf_file):
        printer.d('Config.save_to_file --> %s\n' % conf_file)
        confobj = self.__dict__['confobj']
        with open(conf_file, 'w') as configfile:
            json.dump(self.__dict__['confobj'], fp=configfile, indent=4)
        
    def load_from_file(self, conf_file):
        printer.d('Config.load_from_file --> %s\n' % conf_file)
        with open(conf_file, 'r') as configfile:
            self.__dict__['confobj'].clear()
            self.__dict__['confobj'].update(json.load(configfile))
        confobj = self.__dict__['confobj']
        secobjs = self.__dict__['secobjs']
        secobjs.clear()
        for key in confobj.keys():
            secobjs[key] = Config_SubCategory(confobj, key)
        
    def dump(self):
        confobj = self.__dict__['confobj']
        secobjs = self.__dict__['secobjs']
        for key in secobjs.keys():
            for key, value in secobjs[key].items():
                print key, value

    def __del__(self):
        printer.d('Config.__del__ --> %s' % self)
        
    def keys(self, secname=None):
        confobj = self.__dict__['confobj']
        secobjs = self.__dict__['secobjs']
        if secname is not None:
            return secobjs[secname].keys()
        else:
            return confobj.keys()
            
def TestConfig_SaveConfig():
    mc = Config.get_instance()
    mc.LOAD.teststring = 'stringstring test test abcde'
    mc.RUN.pkgarr_probe = [['/dev/sda1', 'ntfs', '/dev/sda1'], ['/dev/sda2',
    'ntfs', '/dev/sda2'], ['/dev/sda5', 'linux-swap(v1)', '/dev/sda5'],
    ['/dev/sda6', 'ext3', '/dev/sda6'], ['/dev/sda7', 'ext4', '/dev/sda7'],
    ['/dev/sda8', 'ntfs', '/dev/sda8']]

    mc.save_to_file('t-config.json')
    mc2 = Config.get_instance()
    mc.dump()
    print '-'*40
    mc2.dump()
    
def TestConfig_LoadConfig():
    mc = Config.get_instance()
    mc2 = Config.get_instance()
    mc2.load_from_file('t-config.json')
    mc.dump()
    print '-'*40
    mc2.dump()
    
def TestConfig_LoadConfig2():
    mc = Config.get_instance()
    mc.load_from_file('t-config.json')
    mc.dump()
    print '-'*40
    mc2 = Config.get_instance()
    mc2.load_from_file('/tmpfs/step_conf/step_3.json')
    mc.dump()
    
if __name__ == '__main__':
    TestConfig_SaveConfig()
    TestConfig_LoadConfig()
    TestConfig_LoadConfig2()
