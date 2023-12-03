import faker
import uuid
import random

def fake_user_data(names):
    fake = faker.Faker()
    users = []
    for n in names:
        users.append({
            "user_id" : uuid.uuid4().hex,
            "subscription_id" : uuid.uuid4().hex,
            "name" : n.split(" ")[0],
            "surname" : n.split(" ")[1],
            "email" : fake.free_email(),
            "phone_number" : fake.basic_phone_number(),
            "age" : random.randint(15,50),
            })

    return users

def fake_user_transaction_data(id):
    transactions = []
    for i in range(random.randint(5,25)):
        transactions.append(fake_single_transaction_data(id))

    return transactions

    




fake_user_data(["bippis mippis", "ippis lippis", "joe rogan", "bim job"])