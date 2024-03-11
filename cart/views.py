from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
## 포스트로만 접근가능

# Create your views here.
from shop.models import Product
from coupon.forms import AddCouponForm
from .forms import AddProductForm
from .cart import Cart

# 장바구니 담기
@require_POST
def add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)

    # 클라이언트 - 서버로 데이터 전달
    # 유효성검사, sql 인젝션 전처리 를 대비해야하는데 그걸 대신해주는게 form
    form = AddProductForm(request.POST)

    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product, quantity=cd['quantity'], is_update=cd['is_update'])

    return redirect('cart:detail')

def remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:detail')

def detail(request):
    cart = Cart(request)
    add_coupon = AddCouponForm()
    for product in cart:
        product['quantity_form'] = AddProductForm(initial= {'quantity':product['quantity'], 'is_update':True})

    return render(request, 'cart/detail.html', {'cart': cart,
                                                'add_coupon':add_coupon})