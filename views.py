from django.shortcuts import render, redirect
from .process import *
from .forms import *
from django.conf import settings
import os


# Create your views here.

def SSRhome(request):
    my_form = SSRinitForm()
    ssr_data = SSRinitModel.objects.all()
    logs = open(os.path.join(settings.BASE_DIR, 'SSRCHECKER/aom/ansible/logs/logs'), 'r')
    if request.method == 'POST':
        my_form = SSRinitForm(request.POST)
        if my_form.is_valid():
            for i in request.POST["IP"].split('\n'):
                data = {'IP': str(i).strip(),
                        'PORT': request.POST['PORT'],
                        'USER': request.POST['USER'],
                        'PASSWORD': request.POST['PASSWORD'],
                        'IDC': request.POST['IDC']}
                if SSRinitForm(data).is_valid():
                    my_form = SSRinitForm(data)
                    my_form.save()
            ssr_data = SSRinitModel.objects.all()
            my_form = SSRinitForm()
    return render(request, 'SSRCHECKER/ssrinit.html', {'form': my_form, 'ssr_data': ssr_data, 'logs': logs.read(), 'logs_recap': SSRsetup().ansiblerecap()})

def SSRinitlogs(request):
    logs = open(os.path.join(settings.BASE_DIR, 'SSRCHECKER/aom/ansible/logs/logs'), 'r')
    return render(request, 'SSRCHECKER/logs.html', {'logs': logs.read(), 'logs_recap': SSRsetup().ansiblerecap()})


def SSRdelete(request, SSRID):
    if request.method == 'GET':
        try:
            domain_id = SSRinitModel.objects.get(id=SSRID)
            domain_id.delete()
            return redirect(SSRhome)
        except:
            return redirect(SSRhome)

def SSRinit(request):
    SSRsetup().ansibleConf()
    SSRsetup().ansibleHosts()
    SSRsetup().ansibleExecute()
    return redirect(SSRinitlogs)




