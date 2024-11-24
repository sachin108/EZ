from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from rest_framework.authtoken.models import Token
from .models import Person, UploadedFile
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404
from django.core.signing import Signer, BadSignature
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.contrib.auth import login

from django.utils.crypto import get_random_string

def signup_page(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        user_type = request.POST['user_type']

        user = Person.objects.create_user(username=username, email=email, password=password, user_type=user_type)
        user.is_active = False  
        user.save()
        token = get_random_string(32)  
        user.verification_token = token
        user.save()

        verification_link = request.build_absolute_uri(f"/verify/{user.id}/{token}/")

        subject = "Verify Your Email"
        message = f"Hi {username},\n\nClick the link to verify your email: {verification_link}"
        send_mail(subject, message, 'your-email@gmail.com', [email])

        return redirect('signin')

    return render(request, 'signup.html')

def email_verification(request, user_id, token):
    user = get_object_or_404(Person, id=user_id)

    if user.verification_token == token:
        print(f'token matched : {token}')
        user.is_active = True
        user.verification_token = None  
        user.save()
        login(request, user)
        return render(request, 'email_verification.html')  
    else:
        return render(request, 'email_verification_failed.html')

def congratulations(request):
    return HttpResponse("Email Verified Suucessfully")

def generate_signed_url(file_id):
    signer = Signer()
    signed_file_id = signer.sign(file_id) 
    return signed_file_id

def verify_signed_url(signed_file_id):
    signer = Signer()
    try:
        file_id = signer.unsign(signed_file_id)  
        return file_id
    except BadSignature:
        return None 

@login_required
def download_file(request, signed_file_id):
    file_id = verify_signed_url(signed_file_id)
    if file_id is None:
        raise Http404("Invalid or expired URL")

    file_obj = get_object_or_404(UploadedFile, pk=file_id)

    if request.user.user_type != 'client':
        return HttpResponse("You do not have permission to access this file.", status=403)

    response = HttpResponse(file_obj.file, content_type='application/octet-stream')
    response['Content-Disposition'] = f'attachment; filename="{file_obj.file.name}"'
    return response

@login_required
def list_files_page(request):
    if request.user.user_type == 'client':
        files = UploadedFile.objects.all()
        signed_urls = [generate_signed_url(file.id) for file in files]
        files_and_urls = zip(files, signed_urls)  # Combine files and signed URLs
        return render(request, 'list_files.html', {'files_and_urls': files_and_urls})
    return redirect('signin')

def signin_page(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user_type = request.POST['user_type']

        user = authenticate(username=username, password=password)
        if user and user.user_type == user_type:
            login(request, user)
            if user.user_type == 'ops':
                return redirect('upload')  
            else:
                return redirect('list_files')  
        else:
            return render(request, 'signin.html', {"error": "Invalid credentials or user type."})

    return render(request, 'signin.html')

def upload_page(request):
    if request.user.is_authenticated and request.user.user_type == 'ops':
        if request.method == "POST" and request.FILES.get('file'):
            file = request.FILES['file']
            file_type = file.name.split('.')[-1]
            if file_type in ['pptx', 'docx', 'xlsx']:
                UploadedFile.objects.create(uploaded_by=request.user, file=file, file_type=file_type)
                return render(request, 'upload.html', {"message": "File uploaded successfully!"})
            else:
                return render(request, 'upload.html', {"error": "Invalid file type. Allowed: pptx, docx, xlsx."})
        return render(request, 'upload.html')
    return redirect('signin')



@login_required
def list_files_page(request):
    if request.user.user_type == 'client':
        files = UploadedFile.objects.all()
        signed_urls = [generate_signed_url(file.id) for file in files]
        files_and_urls = zip(files, signed_urls)  
        return render(request, 'list_files.html', {'files_and_urls': files_and_urls})
    
    return redirect('signin')
