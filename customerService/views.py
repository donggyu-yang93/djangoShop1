from django.shortcuts import render
from .models import CsList, Comment

def cs_list(request):
    lists = CsList.objects.all()
    return render(request, 'customerService/contact.html', {'lists': lists})

def cs_detail(request, pk):
    lists = CsList.objects.get(pk=pk)
    comments = Comment.objects.filter(cs_list=lists)
    return render(request, 'customerService/detail.html', {'lists': lists, 'comments': comments})


# def FAQ(request):
#     lists = csList.objects.get(pk=pk)
#     return render(request, 'customerService/faq.html',)