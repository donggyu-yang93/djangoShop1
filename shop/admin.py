from django.contrib import admin
from .models import *

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id','name','slug']
    prepopulated_fields = {'slug':['name',]}

admin.site.register(Category, CategoryAdmin)
admin.site.register(Comment)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id','name','slug','category','price','discount_percentage','stock','available_display','available_order','created','updated']
    list_filter = ['available_display','created','updated','category']
    prepopulated_fields = {'slug':('name',)} # 장고 공식홈피는 튜플로되어있는데 위에처럼 리스트가능
    list_editable = ['price','discount_percentage','stock','available_display','available_order']

