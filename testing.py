import os, json

logs = open(os.path.join('/home/yroll/Documents/argus-test/web/argus-yroll_rei-afda6c350dd7d5079b28affe07e7704ce1ab9ee9/', 'SSRCHECKER/aom/ansible/logs/logs'), 'r').read()

IPS = ['192.168.11.51','192.168.11.21', '192.168.11.23']
final = []
ipinfo = {}
for i in IPS:
    for i2 in logs.split('PLAY RECAP')[-1].split('\n'):
        if i in i2:
            final.append(i2)

for i in final:
    ipinfo[i.split(':')[0].strip()] = i.split(':')[-1].strip().split()
print(json.dumps(ipinfo, indent=4))
for key, value in ipinfo.items():
    if "unreachable=1" in value:
        print(key)
        print('unreachable')

    elif "failed=1" in value:
        print(key)
        print('failed')

    else:
        print(key)
        print('ok')








