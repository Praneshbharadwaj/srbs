from flask import Flask, jsonify, render_template, request, send_file
import threading
import traceback
import io
from datetime import datetime
from pymongo import MongoClient
from utils.gen_rec_img import generate_receipt_image
from utils.store_image import upload_image_to_C
from utils.serial_num import get_counter

app = Flask(__name__)

# SRBS MongoDB Connection (Commented for reference)
client = MongoClient("mongodb+srv://sriramabhakthasabha:hOsEFBpavwo374Hy@srbs.grssp.mongodb.net/?retryWrites=true&w=majority&appName=srbs")
# Pranesh's MongoDB Connection
# client = MongoClient("mongodb+srv://praneshbharadwaj631:Pranesh%40200323@cluster0.gwupm.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client["receipt_db"]  # Database name
collection = db["receipts"]  # Collection name

def async_store_data(name, phone, address_line1, address_line2, amount, payment_type, reference_number,img_buffer, image_url, counter):
    """Asynchronously store receipt details in MongoDB and upload image."""
    image_url = upload_image_to_C(img_buffer,f"{name}_{phone}.png")
    try:
        receipt_data = {
            "name": name,
            "phone": phone,
            "address_line1": address_line1,
            "address_line2": address_line2,
            "amount": amount,
            "counter": counter,
            "timestamp": datetime.now(),
            "payment_type": payment_type,
            "reference_number": reference_number,
            "image_url": image_url
        }
        collection.insert_one(receipt_data)
        print("Data stored asynchronously in MongoDB")
    except Exception as e:
        print(f"Error storing receipt data: {e}")

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        try:
            name = request.form["name"]
            phone = request.form["phone"]
            address_line1 = request.form["address_line1"]
            address_line2 = request.form["address_line2"]
            amount = request.form["amount"]
            payment_type = request.form["payment_type"]
            reference_number = request.form.get("reference_number", None)  

            phone_no_plus = "+" + phone if not phone.startswith("+") else phone

            # Generate the receipt image in memory
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

            # Get counter for serial numbering
            counter = get_counter()

            # **Run MongoDB Storage & Image Upload in Background**
            upload_thread = threading.Thread(
                target=async_store_data,
                args=(name, phone_no_plus, address_line1, address_line2, amount, payment_type, reference_number,img_buffer, None, counter)
            )
            upload_thread.start()

            # Send the image to the user instantly
            img_buffer.seek(0)
            return send_file(
                img_buffer,
                mimetype="image/png",
                as_attachment=True,
                download_name=f"{name}_{phone}.png"
            )

        except Exception as e:
            tb = traceback.format_exc()
            print(f"Error occurred:\n{tb}")
            return render_template("error.html", error_message="An error occurred while processing your request.")

    return render_template("index.html")

@app.route("/get-receipts", methods=["GET"])
def get_data():
    data = collection.find({}, {"_id": 0})
    return jsonify(list(data))

if __name__ == "__main__":
    app.run(debug=True)
