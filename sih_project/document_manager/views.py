from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.http import HttpResponse
from .models import Document
from .forms import DocumentUploadForm
from .utils import perform_ocr
from bson import ObjectId
from django.conf import settings
from gridfs import GridFS
from datetime import datetime
from .utils import allowed_file




def index(request):
    # You can render any template for the index page (home or dashboard)
    return render(request, 'index.html')  # Make sure the template exists in your templates folder


# Login view
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('dashboard')  # This should redirect to the dashboard
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('login')
    return render(request, 'index.html')


# Signup view
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been created!')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

# Dashboard view
@login_required
def dashboard(request):
    documents = Document.objects.filter(owner=request.user)
    return render(request, 'dashboard.html', {'documents': documents})

# Document upload view
@login_required
def upload_document(request):
    if request.method == 'POST' and request.FILES['document']:
        document_file = request.FILES['document']
        if allowed_file(document_file.name):
            file_data = document_file.read()
            fs = GridFS(settings.MONGO_DB)
            file_id = fs.put(file_data, filename=document_file.name)
            ocr_text = perform_ocr(file_data, document_file.name.split('.')[-1].lower())
            Document.objects.create(
                owner=request.user,
                type=request.POST.get('document_type', 'other'),
                status='Pending',
                file_id=file_id,
                ocr_text=ocr_text,
                filename=document_file.name,
                date_uploaded=datetime.now()
            )
            messages.success(request, 'Document uploaded successfully')
            return redirect('dashboard')
    return render(request, 'upload_document.html')
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# View document view
@login_required
def view_document(request, file_id):
    document = get_object_or_404(Document, id=file_id)  # Use the correct field for lookup
    return render(request, 'view_document.html', {'document': document})

# Download document view
@login_required
def download_document(request, file_id):
    document = get_object_or_404(Document, file_id=file_id, owner=request.user)
    fs = GridFS(settings.MONGO_DB)
    file_data = fs.get(ObjectId(document.file_id))
    return HttpResponse(file_data.read(), content_type='application/octet-stream', headers={
        'Content-Disposition': f'attachment; filename={document.filename}'
    })

# Update OCR view
@login_required
def update_ocr(request, file_id):
    document = get_object_or_404(Document, file_id=file_id, owner=request.user)
    fs = GridFS(settings.MONGO_DB)
    file_data = fs.get(ObjectId(document.file_id)).read()
    ocr_text = perform_ocr(file_data, document.filename.split('.')[-1].lower())
    document.ocr_text = ocr_text
    document.save()
    messages.success(request, 'OCR text updated successfully')
    return redirect('view_document', file_id=file_id)

def logout_view(request):
    logout(request)
    return redirect('login')