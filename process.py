from django.conf import settings
from .models import *
from subprocess import *
import os


class SSRsetup():
    def __init__(self):
        self.ansiblefile = os.path.join(settings.BASE_DIR, 'SSRCHECKER/aom/ansible/ansible.cfg')
        self.hostsfile = os.path.join(settings.BASE_DIR, 'SSRCHECKER/aom/ansible/hosts')
        self.ansible_conf = {
            'inventory' : os.path.join(settings.BASE_DIR, 'SSRCHECKER/aom/ansible/hosts'),
            'library' : os.path.join(settings.BASE_DIR, 'SSRCHECKER/aom/ansible/my_modules'),
            'local_tmp' : os.path.join(settings.BASE_DIR, 'SSRCHECKER/aom/ansible/tmp'),
            'roles_path' : os.path.join(settings.BASE_DIR, 'SSRCHECKER/aom/ansible/roles'),
            'log_path': os.path.join(settings.BASE_DIR, 'SSRCHECKER/aom/ansible/logs'),
            'host_key_checking' : False,
            'deprecation_warnings' : False,
            'command_warnings' : False
        }

    def ansibleConf(self):
        open(self.ansiblefile, 'w').close()
        open(self.ansiblefile, 'a').write('[defaults]\n')
        for key, value in self.ansible_conf.items():
            open(self.ansiblefile, 'a').write('{} = {}\n'.format(key, value))


    def ansibleHosts(self):
        open(self.hostsfile, 'w').close()
        ssr_hosts = ['[ssr_init]\n', '[ssr_config]\n']
        for ssr_host in ssr_hosts:
            open(self.hostsfile, 'a').write(ssr_host)
            for data in SSRinitModel.objects.all():
                open(self.hostsfile, 'a').write('{} ansible_ssh_port={} ansible_ssh_user={} ansible_ssh_pass={}\n'.format(data.IP, data.PORT, data.USER, data.PASSWORD))
        open(self.hostsfile, 'a').write('[multi:children]\nssr_init\nssr_config\n[multi:vars]\nAUTH_BASIC_ENABLED=False\nHOST_KEY_CHECKING=False\nANSIBLE_HOST_KEY_CHECKING=False\n')

    def ansibleExecute(self):
        ansiblehosts = os.path.join(settings.BASE_DIR, 'SSRCHECKER/aom/ansible/hosts')
        ansible_main = os.path.join(settings.BASE_DIR, 'SSRCHECKER/aom/ansible/main.yml')
        limit = 'ssr_init,ssr_config'
        tags = 'initialization_ssr,config_ssr'
        os.system("ansible-playbook -i {} {} --ssh-common-args='-o StrictHostKeyChecking=no' --limit {} --tags {} > {} &".format(ansiblehosts, ansible_main, limit, tags, os.path.join(settings.BASE_DIR, 'SSRCHECKER/aom/ansible/logs/logs')))


    def ansiblerecap(self):
        logs = open(os.path.join(settings.BASE_DIR, 'SSRCHECKER/aom/ansible/logs/logs'), 'r').read()
        if "PLAY RECAP" in logs.strip('\n'):
            return True

class SSRsave():
    def ssrlogs(self):
        logs = open(os.path.join(settings.BASE_DIR, 'SSRCHECKER/aom/ansible/logs/logs'), 'r').read()

        if "fatal" in logs.strip('\n') or "unreachable=1" in logs.strip('\n'):
            return logs.strip('\n')