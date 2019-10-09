from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Domain_c



# Create your views here.

def domain_check(request):
    domain = Domain_c().querydomain()
    status = []
    lastcheck = []
    forcecheck = []
    for i in domain:
        status.append(Domain_c().querystatus(i))

    for i2 in domain:
        lastcheck.append(Domain_c().querydate(i2))

    for i3 in domain:
        forcecheck.append(Domain_c().queryfc(i3))

    template = loader.get_template('domain_temp/index.html')
    context = {
        'test': domain,
        'test2': status,
        'test3': lastcheck,
        'test4': forcecheck,
    }
    return HttpResponse(template.render(context, request))
def forcecheck(request):
    f_check = Domain_c.updatefc()




