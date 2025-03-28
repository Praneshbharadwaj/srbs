from pymongo import MongoClient


input_name_x = 320

client = MongoClient("mongodb+srv://praneshbharadwaj631:Pranesh%40200323@cluster0.gwupm.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
# client = MongoClient("mongodb+srv://sriramabhakthasabha:hOsEFBpavwo374Hy@srbs.grssp.mongodb.net/?retryWrites=true&w=majority&appName=srbs")  # Replace with your MongoDB URL if hosted remotely
db = client["receipt_db"]  # Database name
collection = db["serial_number_counter"]
def increment_counter():
    try:
        result = collection.find_one_and_update(
            {},
            {"$inc":{"counter":1}},
            upsert=True,
            return_document=True
        )
        return result["counter"]

    except Exception as e:
        # Handle other potential errors
        print(f"An error occurred: {e}")
        return None


def get_counter():
    try:
        result = collection.find_one({})
        return result["counter"]

    except Exception as e:
        # Handle other potential errors
        print(f"An error occurred: {e}")
        return None

# if __name__ == "__main__":
#     # Example usage:
#     counter_value = increment_counter()

#     if counter_value is not None:
#         print(f"Counter value: {counter_value}")

#     #Example of multiple calls:
#     for i in range(5):
#     new_count = increment_counter()
#     if new_count is not None:
#         print(f"Counter is now: {new_count}")