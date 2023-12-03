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
        'subscription_type_id': type['subscription_type_id'],
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

def return_random_expense(num_names) -> list:
    fake = Faker()
    json_data = []
    for i in range(num_names):
        json_data.append({'expense_id': uuid.uuid4().hex[:50]  \
                         , 'transaction_id': fake.random_int(100, 10000)})
    return json_data

def return_random_expense_type(num_names) -> list:
    fake = Faker()
    json_data = []
    for i in range(num_names):
        json_data.append({'expense_type_id': uuid.uuid4().hex[:50]
                         , 'expense_type_name': fake.word()})
    return json_data

def return_random_transaction(num_names) -> list:
    fake = Faker()
    json_data = []
    for i in range(num_names):
        json_data.append({'transaction_id': i+1, 'transaction_amount': fake.random_int(100, 10000)})
    return json_data



def main():
    file = "../names.csv"
    import pandas as pd
    df = pd.read_csv(file)
    num_names = len(df)

    # SubscriptionType, Budget, ExpenseType
    pres = [
        return_random_subscription_type(num_names),
        return_random_budget(num_names),
        return_random_expense_type(num_names)
    ]

    # populate the database
    for table in pres:
        for row in table:
            print(row)


    import uuid
    for user in df['name'][0:10]:
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
        budget = pres[1].pop(0)
        user['budget_id'] = budget['budget_id']
        sub_type = pres[0].pop(0)
        subscription = return_random_subscription(num_names, sub_type, user_id)
        user['subscription_id'] = subscription['subscription_id']
        # save the user
        print(user)
        # save the subscription
        print(subscription)
        # save the budget
        print(budget)

        # Expense, Transaction generation
        # this is unstructure @kye :here:
        # generate random expenses under user id










main()
