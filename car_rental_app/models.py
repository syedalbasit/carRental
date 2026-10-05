from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator 
from django.contrib.auth.models import AbstractUser
from .manager import UserManager    

class UserType(models.Model):
    type_id = models.AutoField(primary_key=True)
    type_name = models.CharField(max_length=20)

    def __str__(self):
        return self.type_name

class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    address = models.CharField(max_length=200, blank=True)
    phone = models.CharField(max_length=15, blank=True)
    user_type = models.ForeignKey(UserType, on_delete=models.SET_NULL, null=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.first_name + ' ' + self.last_name
    
    
class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    description = models.TextField()

    def __str__(self):
        return self.name
    
class Transmission(models.Model):
    transmission_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    description = models.TextField(null=True)

    def __str__(self):
        return self.name
    
    
class FuelType(models.Model):
    fuel_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name
    
    
class FuelType(models.Model):
    fuel_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name
    
    
class CarModel(models.Model):
    model_id = models.AutoField(primary_key=True)
    manufacturer = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    category = models.ForeignKey(Category, related_name="car_models", on_delete= models.SET_NULL, null=True)
    seating_capacity = models.IntegerField(null=True, blank=True)
    year = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.manufacturer + ' ' + self.name + ' ' + str(self.year)
    

class CarVariant(models.Model):
    variant_id = models.AutoField(primary_key=True)
    variant_name = models.CharField(max_length=50, blank=True, null=True)
    model = models.ForeignKey(CarModel, related_name="variants", on_delete=models.SET_NULL, null=True)
    transmission = models.ForeignKey(Transmission, on_delete=models.SET_NULL, null=True)
    fuel_type = models.ForeignKey(FuelType, on_delete=models.SET_NULL, null=True)
    engine = models.IntegerField()
    horsepower = models.IntegerField()
    mileage = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.model.manufacturer} {self.model.name} {self.model.year} ( {self.variant_name} )"

class CarImage(models.Model):
    image_id = models.AutoField(primary_key=True)
    car = models.ForeignKey('Car', related_name="images", on_delete=models.CASCADE)
    image = models.ImageField(upload_to='car_images/')

    def __str__(self):
        return self.image.url

class Car(models.Model):
    car_id = models.AutoField(primary_key=True)
    variant = models.ForeignKey(CarVariant, on_delete=models.SET_NULL, null=True)
    color = models.CharField(max_length=50)
    price_per_day = models.IntegerField()
    license_number = models.CharField(max_length=15)
    main_image = models.ForeignKey(CarImage, related_name="main_image", on_delete=models.SET_NULL, null=True)
    availability = models.BooleanField()

    def __str__(self):
        return self.license_number
    

class RentalStatus(models.Model):
    status_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    description = models.TextField(null=True)

    def __str__(self):
        return self.name


class Rental(models.Model):
    user = models.ForeignKey(User, related_name="rentals", on_delete=models.SET_NULL, null=True)
    car = models.ForeignKey(Car, related_name="rentals", on_delete=models.SET_NULL, null=True)
    booking_date = models.DateField()
    pickup_date = models.DateField()
    drop_date = models.DateField()
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.ForeignKey(RentalStatus, related_name="rentals", on_delete=models.SET_NULL, null=True)

    class Meta:
            unique_together = ('car', 'pickup_date')

    def __str__(self):
        return f"Car: {self.car.license_number}, Pickup Date: {self.pickup_date}"


class Payment(models.Model):
    rental = models.ForeignKey(Rental, related_name="payments", on_delete=models.CASCADE)
    payment_type = models.CharField(max_length=50)
    payment_method = models.CharField(max_length=50)
    payment_date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Rental: {self.rental.car.license_number}, Payment Date: {self.payment_date}"
    

class Review(models.Model):
    rental = models.OneToOneField(Rental, on_delete=models.CASCADE)
    # one to one relationship with rental table, so that a review can be given only once for a rental
    # it is like a foreign key, but with unique constraint
    rating = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])
    review_date = models.DateField()
    comment = models.TextField()

    def __str__(self):
        return f"Rental: {self.rental.car.license_number}, Rating: {self.rating}"