import faker
import uuid
import json
import random

def fake_user_data(names):
    jsons = []
    fake = faker.Faker()
    for n in names:
        jsons.append(json.dumps({
            "user_id" : uuid.uuid4().hex,
            "subscription_id" : uuid.uuid4().hex,
            "name" : n.split(" ")[0],
            "surname" : n.split(" ")[1],
            "email" : fake.free_email(),
            "phone_number" : fake.basic_phone_number(),
            "age" : random.randint(15,50)
            }))

    for j in jsons:
        print(j, "\n")


fake_user_data(["bippis mippis", "ippis lippis", "joe rogan", "bim job"])