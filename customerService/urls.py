from django.urls import path
from .views import *

app_name = 'customerService'
urlpatterns = [
    # path('', FAQ, name='FAQ'),
    path('', cs_list, name='csList'),
    path('detail/<int:pk>/', cs_detail, name='detail'),
]