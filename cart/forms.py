from django import forms

# 클라이언트 화면에 입력 폼을 만들어주려고 폼을 쓴다.
# 클라이언트가 입력한 데이터에 대한 전처리를 도와준다.

class AddProductForm(forms.Form):
    quantity = forms.IntegerField()
    is_update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)