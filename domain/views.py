from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Domain_c
from .dom_mod.domain2 import domain_forcecheck



# Create your views here.

def domain_check(request):
    domain = Domain_c().querydomain()
    status = []
    lastcheck = []
    forcecheck = []
    domainline = []
    for i in domain:
        status.append(Domain_c().querystatus(i))
    for i2 in domain:
        lastcheck.append(Domain_c().querydate(i2))
    for i3 in domain:
        forcecheck.append(Domain_c().queryfc(i3))
    for i4 in domain:
        domainline.append(Domain_c().queryrow(i4)[:4])
    context = {
        'domain': domain,
        'status': status,
        'lastcheck': lastcheck,
        'forcecheck': forcecheck,
        'domainline': domainline
    }
    template = loader.get_template('domain_temp/index.html')
    return HttpResponse(template.render(context, request))
def forcecheck(request):
    context = {
        "testing": "test"
    }
    template = loader.get_template('domain_temp/index.html')
    return HttpResponse(template.render(context, request))