from django.shortcuts import render, redirect, get_object_or_404
from functools import wraps
from django.http import HttpResponse, JsonResponse
from front.models import User, Contact, Order, OrderDetail, Payment
from django.contrib import messages
from django.utils.text import slugify
from .models import Category, FoodType, Dish

def indexAdmin(request):
    return render(request, 'adminIndex.html')


def authenticated_only(view_func):
    @wraps(view_func)
    def wrapped_view(request, *args, **kwargs):
        if not 'name' in request.session:
            messages.error(request, 'Please Login')
            return redirect('loginUser')  # Redirect to your login page
        if 'name' in request.session:
            if request.session['role'] == "Admin":
                return view_func(request, *args, **kwargs)
            else:
                messages.error(request, 'Access Denied')
                return redirect('index')
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


def adminFoodType(request):
    food_type = FoodType.objects.all()
    return render(request, 'food_type/adminFoodType.html', {'food_type': food_type})

def createFoodType(request):
    if request.method == 'POST':
        type = request.POST['type']

        try:
            category = FoodType.objects.create(
                type=type,
            )
            messages.success(request, "Food Type created successfully!")
            return redirect('adminFoodType')

        except ValueError as e:
            messages.error(request, str(e))
            return redirect('adminFoodType')

    return render(request, 'food_type/adminFoodType.html')


def deleteFoodType(request):
    if request.method == 'POST':
        food_type_id = request.POST['food_type_id']
        try:
            food_type = FoodType.objects.filter(id=food_type_id).first()
            if food_type:
                food_type.delete()
                messages.success(request, 'Food Type deleted successfully.')
                return redirect('adminFoodType')
            else:
                messages.error(request, 'An error occured while deleting food type.')
                return redirect('adminFoodType')
        except ValueError as e:
            messages.error(request, str(e))
            return redirect('adminFoodType')
    return redirect('adminFoodType')



def adminDish(request):
    dishes = Dish.objects.all()
    return render(request, 'dish/adminDish.html', {'dishes': dishes})

def createDish(request):
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
            return redirect('adminDish')

        except ValueError as e:
            messages.error(request, str(e))
            return redirect('createDish')

    return render(request, 'dish/createDish.html', {'categories': categories, 'food_types': food_types})


def deleteDish(request):
    if request.method == 'POST':
        dish_id = request.POST['dish_id']
        try:
            dish = Dish.objects.filter(id=dish_id).first()
            if dish:
                dish.delete()
                messages.success(request, 'Dish deleted successfully.')
                return redirect('adminDish')
            else:
                messages.error(request, 'An error occured while deleting dish.')
                return redirect('adminDish')
        except ValueError as e:
            messages.error(request, str(e))
            return redirect('adminDish')
    return redirect('adminDish')



def editDish(request, id):
    food_types = FoodType.objects.all()
    categories = Category.objects.all()
    dish = Dish.objects.filter(id=id).first()
    return render(request, 'dish/editDish.html', {'categories': categories, 'food_types': food_types, 'dish': dish})


def updateDish(request, id):
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
            return redirect('adminDish')

        except ValueError as e:
            messages.error(request, str(e))
            return redirect('editDish', id=id)

    # Render the edit form with the existing dish data
    return render(request, 'dish/editDish.html', {'categories': categories, 'food_types': food_types, 'dish': dish})

def adminContact(request):
    contacts = Contact.objects.all()
    return render(request, 'contact/adminContact.html', {'contacts': contacts})


def adminOrder(request):
    orders = Order.objects.all()
    return render(request, 'order/orderIndex.html', {'orders': orders})

def adminOrderDetail(request, code):
    order = Order.objects.filter(order_code=code).first()
    payment = Payment.objects.filter(order_code=code).first()
    order_details = OrderDetail.objects.filter(order_code=code)
    return render(request, 'order/orderDetail.html', {'order': order, 'payment': payment, 'order_details': order_details})

def adminOrderUpdateStatus(request, code):
    if request.method == 'POST':
        order = Order.objects.filter(order_code=code).first()
        payment = Payment.objects.filter(order_code=code).first()
        order_details = OrderDetail.objects.filter(order_code=code)

        if request.POST['status'] == 'Way':
            for item in order_details:
                product = Dish.objects.filter(name=item.name).first()
                if product:
                    updateStock = int(product.stock) - int(item.quantity)
                    product.stock = updateStock
                    product.save()
        
        if request.POST['status'] == 'Delievered':
            payment.status = "Completed"
            payment.save()

        order.status = request.POST['status']
        order.save()

        messages.success(request, 'Status updated successfully.')
        return redirect('adminOrderDetail', code)


    return redirect('adminOrderDetail', code)