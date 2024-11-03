from django.shortcuts import render
from django.http import HttpResponse
from .forms import ImageUploadForm
from .models import ImageUpload
from PIL import Image
import os
from io import BytesIO

# compressor/views.py

from django.shortcuts import render

# Define the image_list view
def image_list(request):
    # Logic for displaying images or other content
    # Example: Fetch images from the database or a folder
    # Here, we’re simply rendering a template for demonstration.
    return render(request, 'image_list.html')  # Ensure this template exists or change to an existing template

# Compress and resize the image based on percentage
def compress_image(image, format, quality=80, resize_percentage=100):
    img = Image.open(image)
    
    # Calculate the new dimensions based on the percentage
    if resize_percentage != 100:
        width, height = img.size
        new_width = int(width * (resize_percentage / 100))
        new_height = int(height * (resize_percentage / 100))
        img = img.resize((new_width, new_height), Image.LANCZOS)

    # Save the compressed image to an in-memory file
    img_io = BytesIO()
    if format.lower() in ['jpg', 'jpeg']:
        img = img.convert("RGB")  # JPEG requires RGB mode
        img.save(img_io, format="JPEG", quality=quality, optimize=True)
    elif format.lower() == "png":
        img.save(img_io, format="PNG", optimize=True)
    elif format.lower() == "gif":
        img.save(img_io, format="GIF", optimize=True)
    elif format.lower() == "webp":
        img.save(img_io, format="WEBP", quality=quality, optimize=True)

    img_io.seek(0)  # Seek to the start of the file-like object
    return img_io  # Return the in-memory file object

# Handle the upload and compression
def upload_image(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image_instance = form.save(commit=False)  # Prevent saving to the database
            uploaded_file = request.FILES['image']  # Get the uploaded file
            extension = uploaded_file.name.split('.')[-1]  # Get the file extension

            # Get the compression quality from the form (default is 80)
            quality = int(request.POST.get('quality', 80))

            # Get the resize percentage from the form (default is 100%)
            resize_percentage = int(request.POST.get('resize_percentage', 100))

            # Compress the image and get an in-memory file-like object
            compressed_image_io = compress_image(uploaded_file, extension, quality, resize_percentage)

            # Create a response for file download
            response = HttpResponse(compressed_image_io, content_type=f'image/{extension.lower()}')
            response['Content-Disposition'] = f'attachment; filename="{os.path.splitext(uploaded_file.name)[0]}-compressed.{extension}"'

            return response  # Return the downloadable compressed image file
    else:
        form = ImageUploadForm()

    return render(request, 'upload_image.html', {'form': form})
