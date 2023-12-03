import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_finances.settings')
django.setup()

from faker import Faker
from datetime import datetime, timedelta
import random
import json
import uuid

def return_random_budget(num_names) -> list:
    fake = Faker()
    json_data = []
    for i in range(num_names):
        json_data.append({'budget_id': uuid.uuid4().hex[:50] \
                         , 'budget_amount': fake.random_int(100, 10000)})
    return json_data

def return_random_subscription(num_names, type, user_id) -> dict:
    fake = Faker()
    json_data = {
        'subscription_id': uuid.uuid4().hex[:50],
        'subscription_type_id': type,
        'user_id': user_id,
        'subscription_start_date': datetime.now().strftime("%Y-%m-%d"),
        'subscription_end_date': (datetime.now() + timedelta(days=365)).strftime("%Y-%m-%d")
    }
    return json_data

def return_random_subscription_type(num_names) -> list:
    fake = Faker()
    json_data = []
    for i in range(num_names):
        json_data.append({'subscription_type_id': uuid.uuid4().hex[:50] , \
                          'subscription_type_name': fake.word(), 'subscription_type_amount': fake.random_int(10, 100)})
    return json_data

def return_random_expense(num_names, user) -> list:
    fake = Faker()
    json_data = []
    for i in range(num_names):
        json_data.append({'expense_id': uuid.uuid4().hex[:50] \
                         ,'expense_type_id': uuid.uuid4().hex[:50] \
                         , 'user_id': user, 'transaction_id': uuid.uuid4().hex[:50]})
    return json_data

def return_random_expense_type(num_names) -> list:
    fake = Faker()
    json_data = []
    for i in range(num_names):
        json_data.append({'expense_type_id': uuid.uuid4().hex[:50]
                         , 'expense_type_name': fake.word()})
    return json_data




def fake_single_transaction_data(transaction_id):
    fake = Faker()
    ts = {}

    # generate random invoice
    for i in range(random.randint(1,5)):
        ts[fake.word()] = fake.random_int(100, 10000)


    return {
        "transaction_id" : transaction_id,
        "transaction_amount" : random.randint(0,1000),
        "transaction_date" : fake.date_between('-8y'),
        "financial_invoice" : ts,
    }

from django.apps import apps


def insert(table, data):
    dataMap = {
        'subscription_type': "SubscriptionType",
        'budget': "Budget",
        'expense_type': "ExpenseType",
        'expense': "Expense",
        'transaction': "Transaction",
        'subscription': "Subscription",
        'user': "User",
    }
    table = dataMap[table]
    # Get the model from the table name
    model = apps.get_model('money', table)
    # Create a new instance of the model
    instance = model(**data)
    print(instance)

    # Save the instance to the database
    instance.save()

def clear():
    from money.models import User, Budget, SubscriptionType, Subscription, ExpenseType, Expense, Transaction
    User.objects.all().delete()
    Budget.objects.all().delete()
    SubscriptionType.objects.all().delete()
    Subscription.objects.all().delete()
    ExpenseType.objects.all().delete()
    Expense.objects.all().delete()
    Transaction.objects.all().delete()
    print("Cleared all tables")

def main():
    clear()
    file = "names.csv"
    import pandas as pd
    df = pd.read_csv(file)
    num_names = len(df)

    # SubscriptionType, Budget, ExpenseType
    pres = [
        return_random_subscription_type(num_names),
    ]
    pres_copy = pres.copy()
    budgets = return_random_budget(num_names)

    # populate the database
    for table in ['subscription_type']:
        tableData = pres.pop(0)
        for row in tableData:
            insert(table, row)
    pres = pres_copy.copy()



    import uuid
    for user in df['name'][0:num_names]:
        # user id char field max 50
        user_id = uuid.uuid4().hex[:50]
        user = {
            'user_id': user_id,
            'name': user.split()[0],
            'surname': " ".join(user.split()[1:]),
            'email': Faker().free_email(),
            'phone_number': Faker().phone_number(),
            'age': random.randint(15,50) # FERPA :skull:
        }
        # pop from pres
        budget = budgets.pop(0)
        budget['user_id'] = user_id
        user['budget_id'] = budget['budget_id']
        sub_type = pres[0].pop(0)
        subscription = return_random_subscription(num_names, sub_type, user_id)
        user['subscription_id'] = subscription['subscription_id']
        # save the user
        insert('user', user)
        print(user)
        # save the subscription
        insert('subscription', subscription)
        print(subscription)
        # save the budget
        insert('budget', budget)
        print(budget)

        # Expense, Transaction generation
        # this is unstructure @kye :here:
        # generate random expenses under user id

        # generate random transactions under user id
        expenses = return_random_expense(random.randint(5,10) , user_id)
        # make sure all are unique transaction ids
        for expense in expenses:
            # generate a transaction for this
            transaction = fake_single_transaction_data(expense['transaction_id'])
            insert('expense', expense)
            insert('transaction', transaction)
            print(expense)
            print(transaction)



        # generate random expenses under user id for each











main()
