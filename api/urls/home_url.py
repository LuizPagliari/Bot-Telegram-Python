from django.urls import path 
from django.views.generic import RedirectView

urlpatterns = [
    path('', RedirectView.as_view(url='/orders/'), name='home'),
]
