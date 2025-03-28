from pymongo import MongoClient


client = MongoClient("mongodb+srv://sriramabhakthasabha:hOsEFBpavwo374Hy@srbs.grssp.mongodb.net/?retryWrites=true&w=majority&appName=srbs")
db = client["receipt_db"]  # Database name
collection = db["receipts"] 

collection.update_many({}, { "$set": { "image_url": "" } })
