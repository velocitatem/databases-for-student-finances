from django.shortcuts import render
from django.db.models import Avg, Max, Min
from .models import User, Budget, SubscriptionType, Subscription, ExpenseType, Expense, Transaction


# Create your views here.
# get the average budget for age category

def get_average_budget(request):
    # for now just overall average age of all users where budget over 1000
    # get overall average budget
    # have to join budget and budget_type

    age_categories = []

    # get all budgets
    budgets = Budget.objects.all()
    # get all users
    users = User.objects.all()
    joined = budgets.filter(user_id__in=users.values('user_id'))
    # get min age and max age
    min_age = users.aggregate(min_age=Min('age'))
    max_age = users.aggregate(max_age=Max('age'))
    # go by 10 years into categories
    age = min_age['min_age']
    while age < max_age['max_age']:
        age_categories.append((age, age+5))
        age += 5
    average_budgets = {}
    for category in age_categories:
        # get all users in category
        users_in_category = users.filter(age__gte=category[0], age__lte=category[1])
        # get all budgets for users in category
        budgets_in_category = joined.filter(user_id__in=users_in_category.values('user_id'))
        # get average budget for category
        average_budget = budgets_in_category.aggregate(average_budget=Avg('budget_amount'))
        budget_amt = average_budget['average_budget']
        average_budgets[category] = budget_amt
    print(average_budgets)


    return render(request, 'money/average_budget.html', {'average_budgets': average_budgets, 'min_age': min_age['min_age'], 'max_age': max_age['max_age']})
