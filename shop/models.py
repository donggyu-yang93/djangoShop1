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



class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='products')
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True, unique=True, allow_unicode=True)
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='author_question')
    image = models.ImageField(upload_to='shop/products/%Y/%m/%d', blank=True)
    description = models.TextField(blank=True)
    # 위는 상세페이지 설명 검색용. 검색하면 나오는 요약정보.
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
        return reverse('shop:product_detail', args=[self.id])

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True) # allow_unicode 있어야 한글 안깨지고 slug가 됨
        super(Product, self).save(*args, **kwargs)


class Comment(models.Model):
    post = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')  # comments로 써야 해.
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_comment')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    voter = models.ManyToManyField(User, related_name='comment_votes')  # 댓글 추천

    @property
    def get_count(self):
        return Comment.objects.filter(post=self.post).count()

    def __str__(self):
        return f'{self.author}::{self.content}'

    def get_absolute_url(self):
        return f'{self.post.get_absolute_url()}#comment-{self.pk}'

    def get_avatar_url(self):
        return f'https://doitdjango.com/avatar/id/1525/b75de63e8975ed88/svg/{self.author.email}.png'

    def comment_count(self):
        return Comment.objects.filter(post=self.post).count()
