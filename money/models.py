"""
Did not use foreign keys because using filler with the Django ORM is a pain.
"""
from django.db import models
import uuid

# Create your models here.
class User(models.Model):
    user_id = models.CharField(max_length=50, primary_key=True, unique=True, default=uuid.uuid4().hex[:50]) # default
    # ... for primary key
    subscription_id = models.CharField(max_length=50)
    name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    age = models.IntegerField()
    budget_id = models.CharField(max_length=50)

class Budget(models.Model):
    budget_id = models.CharField(max_length=50, primary_key=True, unique=True, default=uuid.uuid4().hex[:50])
    budget_amount = models.FloatField()
    user_id = models.CharField(max_length=50)

class SubscriptionType(models.Model):
    subscription_type_id = models.CharField(max_length=50, primary_key=True)
    subscription_type_name = models.CharField(max_length=50)
    subscription_type_amount = models.FloatField()

class Subscription(models.Model):
    subscription_id = models.CharField(max_length=50, primary_key=True)
    subscription_type_id = models.CharField(max_length=50)
    user_id = models.CharField(max_length=50)
    subscription_start_date = models.DateField()
    subscription_end_date = models.DateField()

# ExpenseType, Expense
class ExpenseType(models.Model):
    expense_type_id = models.CharField(max_length=50, primary_key=True, unique=True, default=uuid.uuid4().hex[:50])
    expense_type_name = models.CharField(max_length=50)

class Expense(models.Model):
    expense_id = models.CharField(max_length=100, primary_key=True, unique=True, default=uuid.uuid4())
    expense_type_id = models.CharField(max_length=50)
    user_id = models.CharField(max_length=50)
    transaction_id = models.CharField(max_length=50)

# make use of mongodb for transactions
class Transaction(models.Model): # our model for mongo unstruct
    transaction_id = models.CharField(max_length=50, primary_key=True)
    transaction_amount = models.FloatField()
    transaction_date = models.DateField()
    # allow for multiple financial invoice values as unstructured fields
    financial_invoice = models.JSONField()
    class Meta:
        app_label = 'money'
        db_table = 'transaction'