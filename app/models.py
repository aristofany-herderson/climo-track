from django.db import models

class State(models.Model):
  name = models.CharField(null=False, max_length=100)
  
class City(models.Model):
  station = models.CharField(null=False, max_length=100)
  state = models.ForeignKey(State, on_delete=models.CASCADE, default=1)
  
class HydrologicalData(models.Model):
  station = models.ForeignKey(City, on_delete=models.CASCADE, default=1)
  
  temperature_average_january = models.DecimalField(max_digits=10, decimal_places=4, null=False)
  temperature_average_february = models.DecimalField(max_digits=10, decimal_places=4, null=False)
  temperature_average_march = models.DecimalField(max_digits=10, decimal_places=4, null=False)
  temperature_average_april = models.DecimalField(max_digits=10, decimal_places=4, null=False)
  temperature_average_may = models.DecimalField(max_digits=10, decimal_places=4, null=False)
  temperature_average_june = models.DecimalField(max_digits=10, decimal_places=4, null=False)
  temperature_average_july = models.DecimalField(max_digits=10, decimal_places=4, null=False)
  temperature_average_august = models.DecimalField(max_digits=10, decimal_places=4, null=False)
  temperature_average_september = models.DecimalField(max_digits=10, decimal_places=4, null=False)
  temperature_average_october = models.DecimalField(max_digits=10, decimal_places=4, null=False)
  temperature_average_november = models.DecimalField(max_digits=10, decimal_places=4, null=False)
  temperature_average_december = models.DecimalField(max_digits=10, decimal_places=4, null=False)

  precipitation_average_january = models.DecimalField(max_digits=10, decimal_places=4, null=False)
  precipitation_average_february = models.DecimalField(max_digits=10, decimal_places=4, null=False)
  precipitation_average_march = models.DecimalField(max_digits=10, decimal_places=4, null=False)
  precipitation_average_april = models.DecimalField(max_digits=10, decimal_places=4, null=False)
  precipitation_average_may = models.DecimalField(max_digits=10, decimal_places=4, null=False)
  precipitation_average_june = models.DecimalField(max_digits=10, decimal_places=4, null=False)
  precipitation_average_july = models.DecimalField(max_digits=10, decimal_places=4, null=False)
  precipitation_average_august = models.DecimalField(max_digits=10, decimal_places=4, null=False)
  precipitation_average_september = models.DecimalField(max_digits=10, decimal_places=4, null=False)
  precipitation_average_october = models.DecimalField(max_digits=10, decimal_places=4, null=False)
  precipitation_average_november = models.DecimalField(max_digits=10, decimal_places=4, null=False)
  precipitation_average_december = models.DecimalField(max_digits=10, decimal_places=4, null=False)
  