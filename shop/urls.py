from django.urls import path

from .views import *

app_name ='shop'
urlpatterns = [
    path('', product_in_category, name='product_all'),
    path('upload/', ProductUploadView.as_view(), name='product_upload'),
    path('delete/<int:pk>/', ProductDeleteView.as_view(), name='product_delete'),
    path('update/<int:pk>', ProductUpdateView.as_view(), name='product_update'),
    path('<slug:category_slug>/', product_in_category, name='product_in_category'),
    path('<int:id>/<product_slug>/', product_detail, name='product_detail'),

]