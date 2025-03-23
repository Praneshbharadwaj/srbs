from pymongo import MongoClient
from datetime import datetime

client = MongoClient("mongodb+srv://praneshbharadwaj631:Pranesh%40200323@cluster0.gwupm.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")  # Replace with your MongoDB URL if hosted remotely
db = client["receipt_db"]  # Database name
collection = db["receipts"]
from datetime import datetime

# Add 'counter' and 'timestamp' fields to all documents
documents = list(collection.find({}))
print(documents)  # Prints all documents as a list  


