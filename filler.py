import os
import django
from faker import Faker
import pandas as pd
from datetime import datetime, timedelta
from django.apps import apps
import random
import json
import uuid

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_finances.settings')
django.setup()


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
    # gotta clear the tables first before a load
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
    df = pd.read_csv(file)
    num_names = len(df)

    # SubscriptionType, Budget, ExpenseType
    pres = [
        return_random_subscription_type(num_names),
    ]
    # since we deplate in some of the method we copy here
    pres_copy = pres.copy()
    budgets = return_random_budget(num_names)

    # populate the database
    # should have been for multiple types, but now I removed a lot
    for table in ['subscription_type']:
        tableData = pres.pop(0)
        for row in tableData:
            insert(table, row)
    pres = pres_copy.copy()



    for user in df['name'][0:num_names]:
        # user id char field max 50
        user_id = uuid.uuid4().hex[:50]
        user = {
            # create a new user object
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
        # budget lining
        sub_type = pres[0].pop(0)
        subscription = return_random_subscription(num_names, sub_type, user_id)
        user['subscription_id'] = subscription['subscription_id']
        # save the user
        try:
            insert('user', user)
        except Exception as e:
            print(f"Failed to insert user {user['user_id']}")
        print(user)
        # save the subscription
        try:
            insert('subscription', subscription)
        except Exception as e:
            print(f"Failed to insert subscription {subscription['subscription_id']}")
        print(subscription)
        # save the budget
        try:
            insert('budget', budget)
        except Exception as e:
            print(f"Failed to insert budget {budget['budget_id']}")
        print(budget)

        # Expense, Transaction generation
        # this is unstructure @kye :here:
        # generate random expenses under user id

        p = random.randint(5,10)
        # generate random transactions under user id
        expenses = return_random_expense(p , user_id)
        expense_types = return_random_expense_type(p)
        # make sure all are unique transaction ids
        for expense in expenses:
            # generate a transaction for this
            transaction = fake_single_transaction_data(expense['transaction_id'])
            expense_type = expense_types.pop(0)
            expense['expense_type_id'] = expense_type['expense_type_id']
            # save the expense type
            try:
                insert('expense_type', expense_type)
                insert('expense', expense)
                insert('transaction', transaction)
            except Exception as e:
                print(f"Failed to insert expense {expense['expense_id']}, cannot insert transaction {transaction['transaction_id']} and expense type {expense_type['expense_type_id']}")

            print(expense)
            print(transaction)


main()
