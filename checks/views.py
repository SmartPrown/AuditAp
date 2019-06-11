
# Create your views here.
from django.shortcuts import render, HttpResponseRedirect, render_to_response, redirect
from django.core.files.storage import FileSystemStorage
from django.contrib import auth
from django.conf import settings
from .processing.header import XLdocument, XLRDError


import os


def login(request):
    if (request.method == "POST"):
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)

        if user is not None and user.is_active:
            auth.login(request, user)

            return redirect('direct_file')
        else:
            return render(request, 'log_in.html', {
                'error_message': "Wrong username or password",
            })

    return render(request, 'log_in.html')



def direct_file(request):
    if not request.user.is_authenticated:
        return redirect('log_in')

    if (request.method == "POST" and ('upload' in request.FILES) and request.FILES['upload']):
        try:

            ufile = request.FILES['upload']
            materiality = float(request.POST['materiality'])
            print(materiality)
            fs = FileSystemStorage()

            filename = fs.save(ufile.name, ufile)
            profitFileName = filename + "_profit.xlsx"
            lossFileName = filename + "_loss.xlsx"

            doc = XLdocument(materiality,
                             os.path.join(settings.MEDIA_ROOT, filename),
                             proft_path = os.path.join(settings.MEDIA_ROOT, profitFileName),
                             loss_path = os.path.join(settings.MEDIA_ROOT, lossFileName),
                             )
            doc.search_and_devide()

            uploaded_file_url = fs.url(filename)
            lossFileUrl = fs.url(lossFileName)

            profitFileUrl = fs.url(profitFileName)


            return render(request, 'direct_file.html', {
                'uploaded_file_url': uploaded_file_url,
                'name': filename,
                'loss_url': lossFileUrl,
                'profit_url': profitFileUrl,
                'user_name': request.user.username
            })
        except XLRDError:
            return render(request, 'direct_file.html', {
                'upload_error': "Wrong file format",
                'user_name': request.user.username
            })

    elif (request.method == "POST" and ('upload' not in request.FILES)):
        return render(request, 'direct_file.html', {
            'upload_error': "No file uploaded",
            'user_name': request.user.username
        })

    return render(request, 'direct_file.html', { 'user_name': request.user.username})


def log_out(request):
    auth.logout(request)
    return redirect('log_in')
