from flask import Flask, render_template, request, send_file
import os


app = Flask(__name__)
from utils.gen_rec_img import generate_receipt_image
from utils.save_csv import write_to_csv

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
        output_folder = "D:/Prathith/SRBS_119/Receipts"
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
            write_to_csv(filename="D:/Prathith/SRBS_119/Receipts/Receipts.csv",
                         name=name,
                         phone=phone_no_plus,
                         address_line1=address_line1,
                         address_line2=address_line2,
                         amount=int(amount))

            # save_details_to_csv()

            print("Generated IMG!")

            return render_template(
                "success.html",
                name=name,
                phone=phone,
                img_path=img_path,
                address="address",
                amount=amount,
            )

        except Exception as e:
            print(f"Error: {e}")
            return render_template(
                "error.html", error_message=f"An error occurred: {e}"
            )

    return render_template("index.html")





if __name__ == "__main__":
    app.run(debug=True)
