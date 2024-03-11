
from django.shortcuts import render
from .models import *
from cart.cart import Cart
from .forms import *



# 장바구니 첫페이지
def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        # 2. 입력받은 정보를 후처리 3. 잘 입력하면 여기서 끝나지만
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if cart.coupon:
                order.coupon = cart.coupon
                # order.discount = cart.coupon.amount
                order.discount = cart.get_discount_total() # 계산식을 더 구현하려면 이쪽으로.
            order.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity']
                                         )
            cart.clear()
            return render(request, 'order/create.html', {'order': order})
    else: # 1.주문자 정보를 입력받는페이지
        form = OrderCreateForm()
        # 1.5 여기를 거쳐서 if로 간다. 4. 3의 입력이 부족하면 다시 여기로 거친다.
    return render(request, 'order/create.html', {'cart': cart, 'form': form})

#주문완료 이후 보이는 페이지
# Ajax 쓸건데 안되는 환경에서도 주문해야할때 이페이지. Ajax 쓰면 위에로직
def order_complete(request):
    order_id = request.GET.get('order_id')
    order = Order.objects.get(id=order_id)
    # order = get_object_or_404(Order, id=order_id) 둘다같음
    return render(request, 'order/complete.html', {'order': order})

from django.views.generic.base import View
from django.http import JsonResponse

class OrderCreateAjaxView(View):
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({"authenticated": False}, status=403)

        cart = Cart(request)
        form = OrderCreateForm(request.POST)

        if form.is_valid():
            order = form.save(commit=False)
            if cart.coupon:
                order.coupon = cart.coupon
                order.discount = cart.get_discount_total()
            order.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity']
                                         )
            cart.clear()
            data = {
                "order_id": order.id
            }
            return JsonResponse(data)
        else:
            return JsonResponse({}, status=401)


class OrderCheckoutAjaxView(View):
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({"authenticated": False}, status=403)

        order_id = request.POST.get('order_id')
        order = Order.objects.get(id=order_id)
        amount = request.POST.get('amount')

        try:
            merchant_order_id = OrderTransaction.objects.create_new(
                order=order,
                amount=amount
            )
        except:
            merchant_order_id = None

        if merchant_order_id is not None:
            data = {
                "works": True,
                "merchant_id": merchant_order_id
            }
            return JsonResponse(data)
        else:
            return JsonResponse({}, status=401)


class OrderImpAjaxView(View):
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({"authenticated": False}, status=403) #LoginRequiredMixin으로 하면 Json이 안된대.

        order_id = request.POST.get('order_id')
        order = Order.objects.get(id=order_id)
        merchant_id = request.POST.get('merchant_id')
        imp_id = request.POST.get('imp_id')
        amount = request.POST.get('amount')

        try:
            trans = OrderTransaction.objects.get(
                order=order,
                merchant_order_id=merchant_id,
                amount=amount
            )
        except:
            trans = None

        if trans is not None:
            trans.transaction_id = imp_id
            trans.success = True
            trans.save() # 여기까지 되면 model의 payment 유효검사로 넘어가는거임. 실패시 else로 튐.
            order.paid = True
            order.save()

            data = {
                "works": True
            }

            return JsonResponse(data)
        else:
            return JsonResponse({}, status=401)

