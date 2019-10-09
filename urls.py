from django.urls import path
from .views import *

urlpatterns = [
    path('', domain_check, name='domcheck' ),
    #path('', forc )
]
