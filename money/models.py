from django.db import models

# Create your models here.
class User(models.Model):
    user_id = models.CharField(max_length=50, primary_key=True)
    subscription_id = models.CharField(max_length=50)
    name = models.CharField(max_length=255)  # Example for Name
    surname = models.CharField(max_length=255)  # Example for Surname
    email = models.EmailField()  # Example for Email
    phone_number = models.CharField(max_length=20)  # Example for PhoneNumber
    age = models.IntegerField()  # Example for Age
    budget_id = models.CharField(max_length=50)

class Budget(models.Model):
    budget_id = models.CharField(max_length=50, primary_key=True)
    budget_amount = models.FloatField()
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

class SubscriptionType(models.Model):
    subscription_type_id = models.CharField(max_length=50, primary_key=True)
    subscription_type_name = models.CharField(max_length=50)
    subscription_type_amount = models.FloatField()

class Subscription(models.Model):
    subscription_id = models.CharField(max_length=50, primary_key=True)
    subscription_type_id = models.ForeignKey(SubscriptionType, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    subscription_start_date = models.DateField()
    subscription_end_date = models.DateField()

class ExpenseType(models.Model):
    expense_type_id = models.CharField(max_length=50, primary_key=True)
    expense_type_name = models.CharField(max_length=50)

class Expense(models.Model):
    expense_type_id = models.ForeignKey(ExpenseType, on_delete=models.CASCADE)
    transaction_id = models.CharField(max_length=50)
