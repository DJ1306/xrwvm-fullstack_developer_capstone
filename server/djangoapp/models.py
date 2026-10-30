from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

class CarMake(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    def __str__(self):
        return self.name

class CarModel(models.Model):
    car_make = models.ForeignKey(CarMake,on_delete=models.CASCADE,related_name="models")
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=12,choices=[(kind,kind) for kind in ["Sedan","SUV","Wagon","Truck","Convertible","Coupe","Hatchback","Minivan","Pickup"]])
    year = models.PositiveIntegerField(validators=[MinValueValidator(2015),MaxValueValidator(2023)])
    class Meta:
        constraints = [models.UniqueConstraint(fields=["car_make","name","year"],name="unique_car_model")]
    def __str__(self):
        return f"{self.car_make.name} {self.name} ({self.year})"
