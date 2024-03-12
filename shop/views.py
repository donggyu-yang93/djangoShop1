from django.shortcuts import render, get_object_or_404
from django.views.generic import CreateView, UpdateView, DeleteView
from django.shortcuts import redirect
from .models import *
from cart.forms import AddProductForm


def product_in_category(requrest, category_slug=None):
    current_category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available_display=True)
    if category_slug:
        current_category = get_object_or_404(Category, slug = category_slug)
        products = products.filter(category=current_category)
    return render(requrest, 'shop/list.html',
                  {
                      'current_category':current_category,
                      'categories':categories,
                      'products':products

                  })

def product_detail(request, id, product_slug=None):
    product = get_object_or_404(Product, id=id, slug=product_slug)
    add_to_cart = AddProductForm(initial={'quantity':1})
    return render(request, 'shop/detail.html', {'product':product, 'add_to_cart':add_to_cart})

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