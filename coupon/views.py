

from django.shortcuts import redirect
from django.utils import timezone
## 사용기간을 쓸거면 타임존으로 해야 실제시간으로 해줌
from django.views.decorators.http import require_POST

from .models import Coupon
from .forms import AddCouponForm

@require_POST
def add_coupon(request):
    now = timezone.now()
    form = AddCouponForm(request.POST)
    if form.is_valid():
        code = form.cleaned_data['code']

        try:  ## code exact 하면 대소문자 구별, iexcat 하면 대소문자 안구별
            coupon = Coupon.objects.get(code__iexact=code, use_from__lte=now, use_to__gte=now, active=True)
            request.session['coupon_id'] = coupon.id

        except Coupon.DoesNotExist:
            request.session['coupon_id'] = None

    return redirect('cart:detail')