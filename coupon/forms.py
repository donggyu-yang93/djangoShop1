from django import forms

class AddCouponForm(forms.Form):
    code = forms.CharField(label='쿠폰 코드를 입력하세요')