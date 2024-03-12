from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify

class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    meta_description = models.TextField(blank=True)
    # 메타디스크립션 설명임 pk가능성있어서 dbindex트루 allowunicode는 한글작성용
    slug = models.SlugField(max_length=200, db_index=True, unique=True, allow_unicode=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_in_category', args=[self.slug])

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='products')
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True, unique=True, allow_unicode=True)
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='author_question')
    image = models.ImageField(upload_to='shop/products/%Y/%m/%d', blank=True)
    description = models.TextField(blank=True)
    # 위는 상세페이지 설명 밑은su를빠르게한다?
    meta_description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2) # 소수점 두개 포함해서 10자리 숫자임
    stock = models.PositiveIntegerField()
    available_display = models.BooleanField('Display', default=True)
    available_order = models.BooleanField('Order', default=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created', '-updated']
        index_together = [['id', 'slug']]


    #관리자창에서 나오는거
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.id, self.slug])

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True) # allow_unicode 있어야 한글 안깨지고 slug가 됨
        super(Product, self).save(*args, **kwargs)

