from django import forms

from .models import Order

class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'address', 'postal_code','city']


# orderCreateView에서 사용하고 ordercompleteview에서 주문완료처리함