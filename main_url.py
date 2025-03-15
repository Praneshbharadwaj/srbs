from flask import Flask, render_template, request, send_file, redirect, url_for
from PIL import Image, ImageDraw, ImageFont
import os
import webbrowser

app = Flask(__name__)

from PIL import Image, ImageDraw, ImageFont
import os

from utils.num2str import *

ramothsava_year = 119

def generate_receipt_image(name, phone, address_line1, address_line2, amount, output_folder, logo_path=None, signature_path=None):
    """Generates a PNG receipt image with address lines, amount, logo, border, signature, and different font sizes."""
    width, height = 400, 300
    img = Image.new('RGB', (width, height), color='white')
    d = ImageDraw.Draw(img)

    try:
        receipt_font = ImageFont.truetype("arial.ttf", 24)
        data_font = ImageFont.truetype("arial.ttf", 14)
        address_font = ImageFont.truetype("arial.ttf", 10)
    except IOError:
        receipt_font = ImageFont.load_default()
        data_font = ImageFont.load_default()
        address_font = ImageFont.load_default()

    # Convert amount ruppes to words
    amount_str = number_to_words_rupees(int(amount))

    receipt_text = f"Sri Rama Bhaktha Sabha (R) \nReceipt"
    name_text = f"Received with thanks from Sri/Smt: {name}"
    phone_text = f"Phone: {phone}"
    address_line1_text = f"Address Line 1: {address_line1}"
    address_line2_text = f"Address Line 2: {address_line2}"
    towards_text = f"Towards {ramothsava_year}th year ramothsava celebrations "
    amount_text = f"Amount: ₹{amount}"
    amount_words_text = f"Amountg in words: {amount_str}"
    sign_text = "Sign"

    receipt_bbox = d.textbbox((0, 0), receipt_text, font=receipt_font)
    name_bbox = d.textbbox((0, 0), name_text, font=data_font)
    phone_bbox = d.textbbox((0, 0), phone_text, font=data_font)
    address_line1_bbox = d.textbbox((0, 0), address_line1_text, font=address_font)
    address_line2_bbox = d.textbbox((0, 0), address_line2_text, font=address_font)
    amount_bbox = d.textbbox((0, 0), amount_text, font=data_font)
    amount_words_bbox = d.textbbox((0, 0), amount_words_text, font=data_font)
    sign_bbox = d.textbbox((0, 0), sign_text, font=data_font)

    receipt_width = receipt_bbox[2] - receipt_bbox[0]
    receipt_height = receipt_bbox[3] - receipt_bbox[1]
    name_width = name_bbox[2] - name_bbox[0]
    name_height = name_bbox[3] - name_bbox[1]
    phone_width = phone_bbox[2] - phone_bbox[0]
    phone_height = phone_bbox[3] - phone_bbox[1]
    address_line1_width = address_line1_bbox[2] - address_line1_bbox[0]
    address_line1_height = address_line1_bbox[3] - address_line1_bbox[1]
    address_line2_width = address_line2_bbox[2] - address_line2_bbox[0]
    address_line2_height = address_line2_bbox[3] - address_line2_bbox[1]
    amount_width = amount_bbox[2] - amount_bbox[0]
    amount_height = amount_bbox[3] - amount_bbox[1]
    sign_width = sign_bbox[2] - sign_bbox[0]
    sign_height = sign_bbox[3] - sign_bbox[1]

    receipt_x = (width - receipt_width) // 2
    name_x = 20
    phone_x = 20
    address_line1_x = 20
    address_line2_x = 20
    amount_x = 20
    amount_words_x = 20
    sign_x = width - sign_width - 10

    receipt_y = 30
    name_y = receipt_y + receipt_height + 20
    phone_y = name_y + name_height + 15
    address_line1_y = phone_y + phone_height + 15
    address_line2_y = address_line1_y + address_line1_height + 10
    amount_y = address_line2_y + address_line2_height + 15
    amount_words_y = amount_y + amount_height + 15
    sign_y = height - sign_height - 10

    d.text((receipt_x, receipt_y), receipt_text, fill='black', font=receipt_font)
    d.text((name_x, name_y), name_text, fill='black', font=data_font)
    d.text((phone_x, phone_y), phone_text, fill='black', font=data_font)
    d.text((address_line1_x, address_line1_y), address_line1_text, fill='black', font=address_font)
    d.text((address_line2_x, address_line2_y), address_line2_text, fill='black', font=address_font)
    d.text((amount_x, amount_y), amount_text, fill='black', font=data_font)
    d.text((amount_words_x, amount_words_y), amount_words_text, fill='black', font=data_font)
    d.text((sign_x - 20, sign_y - 10), sign_text, fill='black', font=data_font)

    if logo_path and os.path.exists(logo_path):
        try:
            logo = Image.open(logo_path)
            logo = logo.resize((50, 70))
            img.paste(logo, (width - 70, 20))
        except Exception as e:
            print(f"Error adding logo: {e}")

    if signature_path and os.path.exists(signature_path):
        try:
            signature = Image.open(signature_path)
            signature = signature.resize((100, 50))
            img.paste(signature, (width - 110, height - 90))
        except Exception as e:
            print(f"Error adding signature: {e}")

    border_color = 'black'
    border_width = 5
    d.rectangle([(10, 10), (width - 10, height - 10)], outline=border_color, width=border_width)

    image_filename = f"{name.replace(' ', '_')}_{phone}.png"
    image_path = os.path.join(output_folder, image_filename)
    img.save(image_path, 'PNG')
    print(f"PNG generated successfully and saved to: {image_path}")
    return image_path

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        address_line1 = request.form['address_line1']
        address_line2 = request.form['address_line2']
        amount = request.form['amount']
        phone_no_plus = "+" + phone if not phone.startswith('+') else phone
        output_folder = "D:/Prathith/SRBS_119/Receipts"

        try:
            os.makedirs(output_folder, exist_ok=True)
            img_path = generate_receipt_image(name, phone, address_line1, address_line2, amount, output_folder, logo_path="logo/logo.jpg", signature_path="logo/sign.png")

            return render_template('success.html', name=name, phone=phone, img_path=img_path, address="address", amount=amount)

        except Exception as e:
            print(f"Error: {e}")
            return render_template('error.html', error_message=f"An error occurred: {e}")

    return render_template('index.html')

@app.route('/download_receipt', methods=['POST'])
def download_receipt():
    name = request.form['name']
    phone = request.form['phone']
    address = request.form['address']
    amount = request.form['amount']
    output_folder = "generated_files"

    try:
        img_path = generate_receipt_image(name, phone, address, amount, output_folder)
        return send_file(img_path, as_attachment=True, download_name="receipt.png")

    except Exception as e:
        print(f"Download error: {e}")
        return render_template('error.html', error_message=f"Download error: {e}")

if __name__ == '__main__':
    app.run(debug=True)