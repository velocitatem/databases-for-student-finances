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

    


def fake_single_transaction_data(id):
    fake = faker.Faker()
    t = [fake.company(), f"${random.randint(0,80)}.{random.randint(0,100)}", str(fake.date_between('-8y'))]
    if random.randint(0,100) <= 30:
        t.append(fake.ean())

    random.shuffle(t)
    ts = f"{t[0]}, {t[1]}, {t[2]}"
    if len(t) > 3:
        ts += f", {t[3]}"

    return {
        "user_id" : id,
        "transaction" : ts
    }


fake_user_data(["bippis mippis", "ippis lippis", "joe rogan", "bim job"])