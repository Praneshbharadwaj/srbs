from flask import Flask, jsonify, render_template, request, send_file
import os
import traceback
from datetime import datetime
from utils.store_image import *


app = Flask(__name__)
from utils.gen_rec_img import generate_receipt_image
from utils.save_csv import write_to_csv
from pymongo import MongoClient
from utils.sendsmsToPhone import send_sms


# Pranesh
# client = MongoClient("mongodb+srv://praneshbharadwaj631:Pranesh%40200323@cluster0.gwupm.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")  # Replace with your MongoDB URL if hosted remotely

# SRBS
client = MongoClient("mongodb+srv://sriramabhakthasabha:hOsEFBpavwo374Hy@srbs.grssp.mongodb.net/?retryWrites=true&w=majority&appName=srbs")
db = client["receipt_db"]  # Database name
collection = db["receipts"]  # Collection name


import io
from flask import Flask, render_template, request, send_file
from PIL import Image
from utils.num2str import *
from utils.serial_num import get_counter
from datetime import datetime

@app.route("/", methods=["GET", "POST"])
def index():
    print("Started APP")
    if request.method == "POST":
        name = request.form["name"]
        phone = request.form["phone"]
        address_line1 = request.form["address_line1"]
        address_line2 = request.form["address_line2"]
        amount = request.form["amount"]
        phone_no_plus = "+" + phone if not phone.startswith("+") else phone
        payment_type = request.form["payment_type"]
        reference_number = None #Initialize to none, in case it is not provided.

        if payment_type == "cheque" or payment_type == "UPI":
            reference_number = request.form.get("reference_number") #Use .get to prevent key errors.

        print("Submit pressed and details fetched")
        try:
            # Call the generate_receipt_image function
            img_buffer = generate_receipt_image(
                name=name,
                phone=phone_no_plus,
                address_line1=address_line1,
                address_line2=address_line2,
                amount=amount,
                payment_type=payment_type,
                reference_number=reference_number,
                output_folder="Receipts",
                logo_path="logo/logo.jpg",
                signature_path="logo/sign.png",
                template_path="logo/Template.png"
            )
            counter = get_counter()
            # Save receipt data to the database
            image_url = upload_image_to_C(img_buffer,f"{name}_{phone}.png")
            receipt_data = {
                "name": name,
                "phone": phone_no_plus,
                "address_line1": address_line1,
                "address_line2": address_line2,
                "amount": amount,
                "counter": counter,
                "timestamp" : datetime.now(),
                "payment_type":payment_type,
                "reference_number":reference_number,
                "image_url" : image_url
            }
            collection.insert_one(receipt_data)
            print("Generated IMG!")
            print(image_url)
            print("sending sms")
            # send_sms(phone,f''' 
            #     {image_url}
                     
            #          ''')
            response =  send_file(
                img_buffer,
                mimetype="image/png",
                as_attachment=True,
                download_name=f"{name}_{phone}.png"
            )
            response.headers["Refresh"] = "3; url=/"
            return response
            
        except Exception as e:
            tb = traceback.format_exc()
            print(f"Error occurred:\n{tb}")
            return render_template("error.html", error_message=f"An error occurred:\n{tb}")

    return render_template("index.html")
@app.route("/get-receipts",methods = ["GET"])
def getIdata():
    data = collection.find({},{"_id":0})
    print(data)
    return jsonify(list(data))



if __name__ == "__main__":
    app.run(debug=True)
