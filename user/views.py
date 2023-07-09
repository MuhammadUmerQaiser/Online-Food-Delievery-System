from django.shortcuts import render, redirect, get_object_or_404
from functools import wraps
from django.http import HttpResponse, JsonResponse
from front.models import User
from django.contrib import messages
from django.utils.text import slugify
from superUser.models import Category, FoodType, Dish

def indexUser(request):
    return render(request, 'userIndex.html')


def authenticated_only(view_func):
    @wraps(view_func)
    def wrapped_view(request, *args, **kwargs):
        if not 'name' in request.session:
            messages.error(request, 'Please Login')
            return redirect('loginUser')
        if 'name' in request.session:
            if request.session['role'] == "Owner":
                return view_func(request, *args, **kwargs)
            else:
                messages.error(request, 'Access Denied')
                return redirect('index')
    return wrapped_view

def userProfile(request):
    return render(request, 'userProfile.html')

def editUserProfile(request):
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
                return redirect('editUserProfile')
            else:
                messages.error(request, 'User not authentciated!')
                return redirect('editUserProfile')
        
        except ValueError as e:
            messages.error(request, str(e))
            return redirect('editUserProfile')
    return render(request, 'userProfile.html')


def userDish(request):
    user_id = request.session['id']
    dishes = Dish.objects.filter(user_id=user_id)
    return render(request, 'dish/userDish.html', {'dishes': dishes})

def createUserDish(request):
    food_types = FoodType.objects.all()
    categories = Category.objects.all()
    if request.method == 'POST':
        name = request.POST['name']
        price = request.POST['price']
        description = request.POST['description']
        stock = request.POST['stock']
        category_id = request.POST['category_id']
        food_type_id = request.POST['food_type_id']
        user_id = request.session['id']
        image = request.FILES.get('image')
        slug = slugify(name)

        try:
            if Dish.objects.filter(slug=slug).exists():
                raise ValueError('Dish already exists.')
            dish = Dish.objects.create(
                name=name,
                price=price,
                description=description,
                stock=stock,
                category_id=category_id,
                food_type_id=food_type_id,
                user_id=user_id,
                image=image,
                slug=slug,
            )
            messages.success(request, "Dish created successfully!")
            return redirect('userDish')

        except ValueError as e:
            messages.error(request, str(e))
            return redirect('createUserDish')

    return render(request, 'dish/createUserDish.html', {'categories': categories, 'food_types': food_types})


def deleteUserDish(request):
    if request.method == 'POST':
        dish_id = request.POST['dish_id']
        try:
            dish = Dish.objects.filter(id=dish_id).first()
            if dish:
                dish.delete()
                messages.success(request, 'Dish deleted successfully.')
                return redirect('userDish')
            else:
                messages.error(request, 'An error occured while deleting dish.')
                return redirect('userDish')
        except ValueError as e:
            messages.error(request, str(e))
            return redirect('userDish')
    return redirect('userDish')



def editUserDish(request, id):
    food_types = FoodType.objects.all()
    categories = Category.objects.all()
    dish = Dish.objects.filter(id=id).first()
    return render(request, 'dish/editUserDish.html', {'categories': categories, 'food_types': food_types, 'dish': dish})


def updateUserDish(request, id):
    food_types = FoodType.objects.all()
    categories = Category.objects.all()
    dish = Dish.objects.filter(id=id).first()
    if request.method == 'POST':
        name = request.POST['name']
        price = request.POST['price']
        description = request.POST['description']
        stock = request.POST['stock']
        category_id = request.POST['category_id']
        food_type_id = request.POST['food_type_id']
        user_id = request.session['id']
        image = request.FILES.get('image')
        slug = slugify(name)

        try:
            if Dish.objects.filter(slug=slug).exclude(id=id).exists():
                raise ValueError('Dish already exists.')

            # Update the dish data
            dish.name = name
            dish.price = price
            dish.description = description
            dish.stock = stock
            dish.category_id = category_id
            dish.food_type_id = food_type_id
            dish.user_id = user_id
            dish.slug = slug

            # Update the dish image if provided
            if image:
                dish.image = image

            dish.save()

            messages.success(request, "Dish updated successfully!")
            return redirect('userDish')

        except ValueError as e:
            messages.error(request, str(e))
            return redirect('editUserDish', id=id)

    # Render the edit form with the existing dish data
    return render(request, 'dish/editUserDish.html', {'categories': categories, 'food_types': food_types, 'dish': dish})