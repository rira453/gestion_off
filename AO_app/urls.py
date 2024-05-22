
from django.contrib import admin
from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('', views.index, name='index'),
    path('index.html', views.index, name='index'),
    path('ao.html', views.ao, name='ao'),
    path('contact.html', views.contact_view, name='contact'),
    path('marches.html', views.marches, name='marches'),
    path('reglements.html', views.reglements, name='reglements'),
    path('demarches.html', views.demarches, name='demarches'),
    path('false.html', views.false, name='false'),
    path('investissement.html', views.investissement, name='investissement'),
    path('contact.html', views.contact_view, name='contact'),
    path('thank_you.html', views.contact_view, name='thank_you'),
    path('admine.html', views.admine, name='admine'),
    
     path('login.html', sing_in, name='sing_in'),
    path('register.html', sing_up, name='sing_up'),
    path('logout.html', log_out, name='log_out'),
    path('forgot_password.html', forgot_password, name='forgot_password'),
    path('update_password.html', update_password, name='update_password'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('update-password/<uidb64>/<token>/', update_password, name='update_password'),
     path('profile.html', profile_view, name='profile'),
]
