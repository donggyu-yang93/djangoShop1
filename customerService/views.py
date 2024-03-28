from django.shortcuts import render, redirect
from .models import CsList, Comment
from .forms import UploadForm

def cs_list(request):
    lists = CsList.objects.all()
    return render(request, 'customerService/contact.html', {'lists': lists})

def cs_detail(request, pk):
    lists = CsList.objects.get(pk=pk)
    comments = Comment.objects.filter(cs_list=lists)
    return render(request, 'customerService/detail.html', {'lists': lists, 'comments': comments})

def upload_view(request):
    if request.method == 'POST':
        form = UploadForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = UploadForm()
    return render(request, 'customerService/upload.html', {'form': form})


# def FAQ(request):
#     lists = csList.objects.get(pk=pk)
#     return render(request, 'customerService/faq.html',)