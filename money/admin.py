from django.contrib import admin
from .models import User, Budget, SubscriptionType, Subscription, ExpenseType, Expense, Transaction

# Register your models here.
admin.site.register(User)
admin.site.register(Budget)
admin.site.register(SubscriptionType)
admin.site.register(Subscription)
admin.site.register(ExpenseType)
admin.site.register(Expense)
admin.site.register(Transaction)
