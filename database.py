from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import os
load_dotenv(".env")

uri = os.getenv("uri")

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

db = client["test-db"]

collection = db["monthly_reports"]

# incomes = {"Salary": 20000, "blog": 1000, "Other Income": 1000}
# expenses = {"Rent": 6000, "Utitlies": 1000, "Groceries": 5000, "Other": 4000}
# period = "August_2024"
# comment = "some comment"
def insert_period(period, incomes, expenses, comment):
    collection.insert_one({"key": period, "incomes": incomes, "expenses": expenses, "comment": comment})

# insert_period(period, incomes, expenses, comment)

def fetch_all_periods():
    return collection.find()

# periods = fetch_all_periods()
# for period in periods:
#     print(period)

def get_period(period):
    return collection.find_one({"key": period})
# result = get_period("August_2024")
# print(result)
