from django.urls import path
from .views import *

app_name = 'customerService'
urlpatterns = [
    # path('', FAQ, name='FAQ'),
    path('', cs_list, name='csList'),
    path('cs/<int:pk>/', cs_detail, name='detail'),
    path('upload/', upload_view, name='csUpload'),
]