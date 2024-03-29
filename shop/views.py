from django.shortcuts import render, get_object_or_404
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView
from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied
from django.db.models import Count
from .models import *
from .forms import CommentForm
from cart.forms import AddProductForm


class ProductList(ListView):
    model = Product
    template_name = 'shop/list.html'
    paginate_by = 6

    def get_queryset(self):
        self.current_category = None
        category_slug = self.kwargs.get('slug')
        sort = self.request.GET.get('sort', '')

        if category_slug:
            self.current_category = get_object_or_404(Category, slug=category_slug)
            queryset = Product.objects.filter(category=self.current_category, available_display=True)
        else:
            queryset = Product.objects.filter(available_display=True)

        # 정렬 로직 추가
        if sort == 'price_asc':
            queryset = queryset.order_by('price')
        elif sort == 'price_desc':
            queryset = queryset.order_by('-price')
        elif sort == 'date':
            queryset = queryset.order_by('-created')
        elif sort == 'reviews':
            queryset = queryset.annotate(review_count=Count('comments')).order_by('-review_count')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        products = context.get('object_list')
        for product in products:
            if product.discount_percentage > 0:
                product.discounted_price = product.price - (product.price * product.discount_percentage / 100)
            else:
                product.discounted_price = product.price
        context['products'] = products  # 수정된 products 리스트를 다시 컨텍스트에 할당
        context['categories'] = Category.objects.all()
        return context

def paldoDiscount(requrest):
    products = Product.objects.filter(available_display=True, name__icontains='팔도')
    return render(requrest, 'shop/paldo.html',{'products':products})

def foodDiscount(requrest, category_slug='식품'):
    categories = Category.objects.all()
    current_category = get_object_or_404(Category, slug=category_slug)
    products = Product.objects.filter(available_display=True, category=current_category)

    return render(requrest, 'shop/food.html',
                  {
                      'current_category':current_category,
                      'categories':categories,
                      'products':products

                  })


class CategoryPostList(ProductList):
    def get_queryset(self):
        queryset = super().get_queryset()
        slug = self.kwargs['slug']
        self.category = Category.objects.get(slug=slug)
        queryset = queryset.filter(category=self.category)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(CategoryPostList, self).get_context_data()
        slug = self.kwargs['slug']
        self.category = Category.objects.get(slug=slug)
        context['current_category'] = self.category
        return context




class ProductDetailView(DetailView):
    model = Product
    template_name = 'shop/detail.html'
    context_object_name = 'product'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['add_to_cart'] = AddProductForm(initial={'quantity': 1})
        context['comment_form'] = CommentForm
        return context

class ProductUploadView(CreateView):
    model = Product
    fields = ['name', 'image', 'description', 'price', 'stock', 'category']
    template_name = 'shop/upload.html'

    def form_valid(self, form):
        form.instance.author_id = self.request.user.id
        if form.is_valid():
            form.instance.save()
            return redirect('/')
        else:
            return self.render_to_response({'form':form}) # 회원가입 실패했을때 폼 유지하는거.

class ProductDeleteView(DeleteView):
    model = Product
    success_url = '/'
    template_name = 'shop/delete.html'

class ProductUpdateView(UpdateView):
    model = Product
    fields = ['name', 'image', 'description', 'meta_description', 'price', 'stock']
    template_name = 'shop/update.html'




def new_comment(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.user.is_authenticated:

        if request.method == 'POST':
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.post = product
                comment.author = request.user
                comment.save()
                return redirect(reverse('shop:product_detail', args=[product.pk]))
            else:
                return redirect(reverse('shop:product_detail', args=[product.pk]))
        else:
            raise PermissionDenied # POST 아니면 거부
    else:
        raise PermissionDenied


def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post = comment.post
    if request.user.is_authenticated and request.user == comment.author:
        comment.delete()
        return redirect(reverse('shop:product_detail', args=[post.pk]))
    else:
        raise PermissionDenied

from django.contrib.auth.mixins import LoginRequiredMixin
class CommentUpdate(LoginRequiredMixin, UpdateView):
    model = Comment
    form_class = CommentForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user == self.get_object().author:
            return super(CommentUpdate, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
@login_required(login_url='login')
def comment_vote(request, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    if request.user == comment.author:
        return JsonResponse({'status': 'error', 'message': '본인이 작성한 글은 추천할 수 없습니다.'})
    else:
        comment.voter.add(request.user)
        votes = comment.voter.count()
        return JsonResponse({'status': 'success', 'votes': votes})





# def product_in_category(requrest, category_slug=None):
#     current_category = None
#     categories = Category.objects.all()
#     products = Product.objects.filter(available_display=True)
#     if category_slug:
#         current_category = get_object_or_404(Category, slug = category_slug)
#         products = products.filter(category=current_category)
#     return render(requrest, 'shop/list.html',
#                   {
#                       'current_category':current_category,
#                       'categories':categories,
#                       'products':products
#
#                   })
#
# def product_detail(request, id, product_slug=None):
#     product = get_object_or_404(Product, id=id, slug=product_slug)
#     add_to_cart = AddProductForm(initial={'quantity':1})
#     return render(request, 'shop/detail.html', {'product':product, 'add_to_cart':add_to_cart})