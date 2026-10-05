
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth import login as django_login, authenticate
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Car, CarImage, CarVariant, CarModel, Rental, RentalStatus
from django.db.models import Q

User = get_user_model()

# Create your views here.
def home(request):
    
    car = Car.objects.all()
    car.order_by('variant__model__year')

    if request.user.is_authenticated:
        return render(request, 'home.html', {"user": request.user})
    return render(request, 'home.html', {'car': car})

def about(request):
    completed_orders_count = Rental.objects.filter(status__name='Completed').count()
    customers_count = User.objects.filter(user_type__type_name='Customer').count()
    free_vehicles_count = Car.objects.filter(availability=True).count()
    total_vehicles_count = Car.objects.count()
    
    return render(request, 'about.html', {"user": request.user, "completed_orders_count": completed_orders_count, "customers_count": customers_count, "free_vehicles_count": free_vehicles_count, "total_vehicles_count": total_vehicles_count})

def contact(request):
    print(request.path)
    return render(request, 'contact.html', {"user": request.user})

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = authenticate(request, username=email, password=password)

        if user:
            django_login(request, user)
            return redirect('home')
        
        return render(request, 'login.html', {'error': 'Invalid Credentials'})
            
    elif request.user.is_authenticated:
        return redirect('home')
    
    return render(request, 'login.html')

        
def carList(request):

    cars_list = Car.objects.all()
    cars_list.order_by('variant__model__year')
    query_params = request.GET
    
    minPrice = query_params.get('minPrice', None)
    maxPrice = query_params.get('maxPrice', None)
    categories = query_params.get('categories', None)

    if minPrice and maxPrice:
        cars_list = cars_list.filter(price_per_day__gte=minPrice, price_per_day__lte=maxPrice)

    if categories:
        categories = categories.split(',')
        filter_conditions = Q()
        for category in categories:
            filter_conditions |= Q(variant__model__category__name=category)
        cars_list = cars_list.filter(filter_conditions)    

    p = Paginator(cars_list, 1)
    # get the page number from the request
    page_number = request.GET.get('page')

    try:
        cars = p.get_page(page_number)
    
    except PageNotAnInteger:
        cars = p.get_page(1)
    
    # if the page number is greater than the total number of pages
    except EmptyPage:
        cars = p.get_page(p.num_pages)

    return render(request, 'carList.html', {"user": request.user, "cars": cars})

def carDetail(request, car_id):

    car = Car.objects.get(car_id=car_id)
    images = car.images.all()

    if request.method == 'POST':
        pickup_date = request.POST['pickdate']
        drop_date = request.POST['dropdate']
        address = request.POST['address']
        phone_number = request.POST['phonenumber']

    return render(request, 'carDetail.html', {"user": request.user, "car": car, "car_images": images})

def userDashboard(request):
    return render(request, 'userdashboard.html')


def signup(request):
    if request.method == 'POST':
        firstname = request.POST['first_name']
        lastname = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']

        if User.objects.filter(email=email).exists():
            return render(request, 'signup.html', {'error': 'Email already exists'})
        
        # Create the user
        user = User.objects.create_user(email=email, password=password, first_name=firstname, last_name=lastname)
        user.save()
            
        # Authenticate and login the user
        user = authenticate(request, username=email, password=password)
        if user is not None:
            django_login(request, user)
            return redirect('home')
        else:
            return render(request, 'signup.html', {'error': 'Authentication failed'})
        
    elif request.user.is_authenticated:
        return redirect('home')

    return render(request, 'signup.html')
