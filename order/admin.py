import csv
import datetime
from django.contrib import admin
from .models import Order, OrderItem
from django.http import HttpResponse

def export_to_csv(modeladmin, request, queryset):
    opts = modeladmin.model._meta
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment;filename={}.csv'.format(opts.verbose_name)
    writer = csv.writer(response)

    fields = [field for field in opts.get_fields() if not field.many_to_many and not field.one_to_many]
    writer.writerow([field.verbose_name for field in fields])

    for obj in queryset:
        data_row = []
        for field in fields:
            value = getattr(obj, field.name)
            if isinstance(value, datetime.datetime):
                value = value.strftime("%Y-%m-%d")
            data_row.append(value)
        writer.writerow(data_row)
    return response
export_to_csv.short_description = 'CSV로 추출'


class OrderItemInline(admin.TabularInline): #Tabular - 테이블형태로 보여주겠다.
    model = OrderItem
    raw_id_fields = ['product'] # product가 외래키라서 raw_id필드 안하면 셀렉버튼으로만 클릭이 됨. 이걸 쓰면 값을 텍스트로 편하게 보여줌


class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email', 'address', 'postal_code', 'city', 'paid', 'created', 'updated']
    list_filter = ['paid', 'created', 'updated']
    inlines = [OrderItemInline] # 다른 모델과 연결되어있는 경우 한페이지 표시하고 싶을 때
    actions = [export_to_csv] # 관리자페이지에 글 지우기하는 그 액션버튼에 추가하는거임

admin.site.register(Order, OrderAdmin)
