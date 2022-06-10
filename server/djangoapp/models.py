from django.db import models
from django.utils.timezone import now


# Car Make model `class CarMake(models.Model)`:
class CarMake(models.Model):
    name = models.CharField(null=False, max_length=30, default='Honda')
    description = models.CharField(max_length=280, default='Honda cars are awesome')

    def __str__(self):
        return self.name

# Car Model model `class CarModel(models.Model):`:
class CarModel(models.Model):
    # Type (CharField with a choices argument to provide limited choices)    
    TYPES = (
            ("SEDAN", "Sedan"), ("SUV", "SUV"), ("TRUCK", "Truck"), ("SPORTS CAR", "Sports Car")
            )
    
    # Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
    make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    name = models.CharField(null=False, max_length=30)
    #constant for c_type choices
    c_type = models.CharField(max_length=30, choices=TYPES)
    # Dealer id, used to refer a dealer created in cloudant database
    dealer_id = models.IntegerField()
    year = models.DateField()
    # __str__ method to print a car make object
    def __str__(self):
        return "Name: " + self.name + \
                " Make Name: "+ self.make.name + \
                " Type: " + self.c_type + \
                " Dealer ID: " + str(self.dealer_id)+ \
                " Year: " + str(self.year)
                


# Python class `CarDealer` to hold dealer data
class CarDealer:

    def __init__(self, address, city, full_name, id, lat, long, short_name, st, zip):
        # Dealer address
        self.address = address
        # Dealer city
        self.city = city
        # Dealer Full Name
        self.full_name = full_name
        # Dealer id
        self.id = id
        # Location lat
        self.lat = lat
        # Location long
        self.long = long
        # Dealer short name
        self.short_name = short_name
        # Dealer state
        self.st = st
        # Dealer zip
        self.zip = zip

    def __str__(self):
        return "Dealer name: " + self.full_name

# Python class `DealerReview` to hold review data
class DealerReview:
    def __init__(self, dealership, name, purchase, review, purchase_date, car_make, car_model, car_year,sentiment, id):
        self.dealership=dealership
        self.name=name
        self.purchase=purchase
        self.review=review
        self.purchase_date=purchase_date
        self.car_make=car_make
        self.car_model=car_model
        self.car_year=car_year
        self.sentiment=sentiment #Watson NLU service
        self.id=id

    def __str__(self):
        return "Review: " + self.review +\
                " Sentiment: " + self.sentiment

