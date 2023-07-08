from django.shortcuts import render, redirect
from functools import wraps
from django.http import HttpResponse, JsonResponse
from front.models import User
from django.contrib import messages
from django.utils.text import slugify
from .models import Category

def indexAdmin(request):
    return render(request, 'adminIndex.html')


def authenticated_only(view_func):
    @wraps(view_func)
    def wrapped_view(request, *args, **kwargs):
        if not 'name' in request.session:
            return redirect('loginUser')  # Redirect to your login page
        return view_func(request, *args, **kwargs)
    return wrapped_view

def adminProfile(request):
    return render(request, 'adminProfile.html')

def editProfile(request):
    if request.method == "POST":
        name = request.POST['name']
        contact = request.POST['contact']

        try:
            if User.objects.filter(id=request.POST['id']).exists():
                user = User.objects.filter(id=request.POST['id']).first()
                user.name = name
                user.phone = contact
                user.save()
                request.session['name'] = name
                request.session['contact'] = contact
                messages.success(request, 'User profile updated successfully!')
                return redirect('editProfile')
            else:
                messages.error(request, 'User not authentciated!')
                return redirect('editProfile')
        
        except ValueError as e:
            messages.error(request, str(e))
            return redirect('editProfile')
    return render(request, 'adminProfile.html')


def adminCategory(request):
    categories = Category.objects.all()
    return render(request, 'category/adminCategory.html', {'categories': categories})

def createCategory(request):
    if request.method == 'POST':
        name = request.POST['name']
        image = request.FILES.get('file')

        # Convert name to lowercase and replace spaces with hyphens
        slug = slugify(name)

        try:
            # Check if a category with the same slug already exists
            if Category.objects.filter(slug=slug).exists():
                raise ValueError('Category already exists.')

            # Create a new category object
            category = Category.objects.create(
                name=name,
                slug=slug,
                image=image
            )
            messages.success(request, "Category created successfully!")
            # Redirect to a success page or do any other necessary operations
            return redirect('adminCategory')  # Replace 'success-page' with your desired URL or view name

        except ValueError as e:
            messages.error(request, str(e))
            return redirect('createCategory')

    return render(request, 'category/createCategory.html')


def deleteCategory(request):
    if request.method == 'POST':
        category_id = request.POST['category_id']
        try:
            category = Category.objects.filter(id=category_id).first()
            if category:
                category.delete()
                messages.success(request, 'Category deleted successfully.')
                return redirect('adminCategory')
            else:
                messages.error(request, 'An error occured while deleting category.')
                return redirect('adminCategory')
        except ValueError as e:
            messages.error(request, str(e))
            return redirect('adminCategory')
    return redirect('adminCategory')