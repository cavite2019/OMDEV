from celery import Celery
import time, requests

CELERY_PREFIX = "test"
CELERY_BROKER = 'redis://10.167.11.205:6379/0'
CELERY_BACKEND = CELERY_BROKER
app = Celery(CELERY_PREFIX,broker=CELERY_BROKER,backend=CELERY_BACKEND)


if __name__ == '__main__':
    t = app.send_task('dns.call_by_name',args=('g_cDNS.getRRCache',),queue='qcoleslaw')
    #domains = []
    #for i in t.get().keys():
    #    domains.append(i.encode('utf-8'));
    domains = [i for i in t.get().keys()]
    t.forget()
    check = []
    for i in range(0,10):
        for domain in domains:
            check.append(domain)
            if domain not in check:
                r = requests.get("http://v.juhe.cn/siteTools/app/NewDomain/query.php?key=0066ee95da11143ef165f348ccd105a8&domainName={0}".format(domain))
            else:
                break

elif __name__ != '__main__':
    print("test")
