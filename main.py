from flask import Flask, render_template, request, send_file
import os
import traceback


app = Flask(__name__)
from utils.gen_rec_img import generate_receipt_image
from utils.save_csv import write_to_csv
from pymongo import MongoClient

client = MongoClient("mongodb+srv://praneshbharadwaj631:Pranesh%40200323@cluster0.gwupm.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")  # Replace with your MongoDB URL if hosted remotely
db = client["receipt_db"]  # Database name
collection = db["receipts"]  # Collection name


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
        output_folder = "Receipts"
        print("Submit pressed and details fetched")
        try:
            os.makedirs(output_folder, exist_ok=True)
            img_path = generate_receipt_image(
                name,
                phone,
                address_line1,
                address_line2,
                amount,
                output_folder,
                logo_path="logo/logo.jpg",
                signature_path="logo/sign.png",
            )

            # write data to csv
            receipt_data = {
                "name": name,
                "phone": phone_no_plus,
                "address_line1": address_line1,
                "address_line2": address_line2,
                "amount": amount
            }
            collection.insert_one(receipt_data)


            # save_details_to_csv()

            print("Generated IMG!")

            return send_file(img_path, as_attachment=True)

        except Exception as e:
            tb = traceback.format_exc()
            print(f"Error occurred:\n{tb}")
        return render_template(
            "error.html", error_message=f"An error occurred:\n{tb}"
        )

    return render_template("index.html")





if __name__ == "__main__":
    app.run(debug=True)
