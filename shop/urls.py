from django.urls import path

from .views import *

app_name ='shop'
urlpatterns = [
    path('', ProductList.as_view(), name='product_all'),
    path('category/<str:slug>/', CategoryPostList.as_view(), name='category_page'),  # 카테고리
    path('upload/', ProductUploadView.as_view(), name='product_upload'),
    path('delete/<int:pk>/', ProductDeleteView.as_view(), name='product_delete'),
    path('update/<int:pk>', ProductUpdateView.as_view(), name='product_update'),
    path('update_comment/<int:pk>/', CommentUpdate.as_view(), name='comment_update'),
    path('<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    # path('<slug:category_slug>/', ProductList.as_view(), name='product_in_category'),




    path('food', foodDiscount, name='food'),
    path('paldo', paldoDiscount, name='paldo'),
    path('<int:pk>/new_comment/', new_comment),
    path('delete_comment/<int:pk>/', delete_comment, name='delete_comment'),
    path('vote_comment/<int:comment_pk>/', comment_vote, name='vote_comment'),


]