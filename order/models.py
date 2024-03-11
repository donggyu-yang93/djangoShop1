from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from coupon.models import Coupon
from shop.models import Product

class Order(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    address = models.CharField(max_length=250)
    postal_code = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)

    coupon = models.ForeignKey(Coupon, on_delete=models.PROTECT, related_name='order_coupon', null=True, blank=True)
    discount = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100000)])

    class Meta:
        ordering = ['-created']


    # 관리자페이지 등에서 객체자체를 출력할때 뭘 보여줄거냐고. 장고에서출력
    def __str__(self):
        return 'Order {}'.format(self.id)

    def get_total_product(self):
        return sum(item.get_item_price() for item in self.items.all())

    def get_total_price(self):
        total_product = self.get_total_product()
        return total_product - self.discount


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='order_products')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1) # 마이너스 주문하면안대니까

    # 오브젝트 출력. 뭐 출력할거냐고.
    def __str__(self):
        return str(self.id)

    def get_item_price(self):
        return self.price * self.quantity



from .iamport import payments_prepare, find_transaction
import hashlib

# 결제정보 매니저로 관리해줌. 새로 트랜잭션 만들었을때 오더정보를 갖게 해줌
# 결제가 되면 트랜잭션으로 보관. 결제가 되면 결제가 되었다고 변경. 주문하다가 실패하더래도 기존 정보를 보관해야하니깐.
class OrderTransactionManager(models.Manager):
    def create_new(self, order, amount, success=None, transaction_status=None):
        if not order:
            raise ValueError("주문 정보 오류")
        order_hash = hashlib.sha1(str(order.id).encode('utf-8')).hexdigest() #sha1 = 암호화
        email_hash = str(order.email).split("@")[0]
        final_hash = hashlib.sha1((order_hash + email_hash).encode('utf-8')).hexdigest()[:10]
        merchant_order_id = str(final_hash)

        payments_prepare(merchant_order_id, amount)

        transaction = self.model(
            order=order,
            merchant_order_id=merchant_order_id,
            amount=amount
        )

        if success is not None:
            transaction.success = success
            transaction.transaction_status = transaction_status

        try:
            transaction.save()
        except Exception as e:
            print("save error", e)

        return transaction.merchant_order_id

    #결제정보 검토. 일치하지 않으면 None
    def get_transaction(self, merchant_order_id):
        result = find_transaction(merchant_order_id)
        if result['status'] == 'paid':
            return result
        else:
            return None

#결제 정보
class OrderTransaction(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    merchant_order_id = models.CharField(max_length=120, null=True, blank=True)
    transaction_id = models.CharField(max_length=120, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0) # 0원 이하면 안되니까.
    transaction_status = models.CharField(max_length=220, null=True, blank=True) # 포트원에 보면 길이 정해져서 오지만 테스트용은 그냥 길게.
    type = models.CharField(max_length=120, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    objects = OrderTransactionManager()

    def __str__(self):
        return str(self.order.id)

    class Meta:
        ordering = ['-created']



def order_payment_validation(sender, instance, created, *args, **kwargs):
    if instance.transaction_id:
        iamport_transaction = OrderTransaction.objects.get_transaction(merchant_order_id=instance.merchant_order_id)

        merchant_order_id = iamport_transaction['merchant_order_id']
        imp_id = iamport_transaction['imp_id']
        amount = iamport_transaction['amount']

        local_transaction = OrderTransaction.objects.filter(merchant_order_id=merchant_order_id,
                                                            transaction_id=imp_id,
                                                            amount=amount
                                                            ).exists()

        if not iamport_transaction or not local_transaction:
            raise ValueError("비정상 거래입니다.")


# 시그널(일이 끝나면 바로 다음일을 지정해줌)
# 결제 정보가 생성된 후에 호출할 함수를 연결해준다.
from django.db.models.signals import post_save
post_save.connect(order_payment_validation, sender=OrderTransaction)