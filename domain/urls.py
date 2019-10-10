from django.urls import path
from .views import *
from .dom_mod.domain2 import *
from .models import Domain_c


urlpatterns = [
    path('', domain_check, name='domcheck' ),
] + [path('fc/', forcecheck)]
