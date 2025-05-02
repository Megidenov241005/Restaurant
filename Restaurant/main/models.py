from django.db import models
from django.contrib.auth.models import User




class Manager(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return f"Manager: {self.user.username}"

class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return f"Client: {self.user.username}"

class Table(models.Model):
    seats = models.PositiveIntegerField()

    def __str__(self):
        return f"Table #{self.id} ({self.seats} seats)"

class Reserve(models.Model):
    table = models.ForeignKey(Table, on_delete=models.PROTECT, related_name="reserves")
    datetime = models.DateTimeField()

    def __str__(self):
        return f"Reservation for Table #{self.table.id} at {self.datetime}"