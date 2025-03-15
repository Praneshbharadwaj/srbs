from flask import Flask, render_template, request, send_file, redirect, url_for
from PIL import Image, ImageDraw, ImageFont
import os
import qrcode
import webbrowser

app = Flask(__name__)

from PIL import Image, ImageDraw, ImageFont
import os

def generate_receipt_image(name, phone, output_folder, logo_path=None):
    """Generates a PNG receipt image with an optional logo, centers text, and uses different font sizes."""
    width, height = 400, 300
    img = Image.new('RGB', (width, height), color='white')
    d = ImageDraw.Draw(img)

    # Load fonts
    try:
        receipt_font = ImageFont.truetype("arial.ttf", 24)
        data_font = ImageFont.truetype("arial.ttf", 14)
    except IOError:
        receipt_font = ImageFont.load_default()
        data_font = ImageFont.load_default()

    # Calculate text positions for centering
    receipt_text = "Receipt"
    name_text = f"Name: {name}"
    phone_text = f"Phone: {phone}"

    receipt_bbox = d.textbbox((0, 0), receipt_text, font=receipt_font)
    name_bbox = d.textbbox((0, 0), name_text, font=data_font)
    phone_bbox = d.textbbox((0, 0), phone_text, font=data_font)

    receipt_width = receipt_bbox[2] - receipt_bbox[0]
    receipt_height = receipt_bbox[3] - receipt_bbox[1]
    name_width = name_bbox[2] - name_bbox[0]
    name_height = name_bbox[3] - name_bbox[1]
    phone_width = phone_bbox[2] - phone_bbox[0]
    phone_height = phone_bbox[3] - phone_bbox[1]

    receipt_x = (width - receipt_width) // 2
    name_x = (width - name_width) // 2
    phone_x = (width - phone_width) // 2

    receipt_y = 30
    name_y = receipt_y + receipt_height + 20
    phone_y = name_y + name_height + 20

    d.text((receipt_x, receipt_y), receipt_text, fill='black', font=receipt_font)
    d.text((name_x, name_y), name_text, fill='black', font=data_font)
    d.text((phone_x, phone_y), phone_text, fill='black', font=data_font)

    if logo_path and os.path.exists(logo_path):
        try:
            logo = Image.open(logo_path)
            logo = logo.resize((50, 70))
            img.paste(logo, (width - 60, 10))
        except Exception as e:
            print(f"Error adding logo: {e}")

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
        phone_no_plus = "+" + phone if not phone.startswith('+') else phone
        output_folder = "D:/Prathith/SRBS_119/Receipts" # Define output folder

        try:
            os.makedirs(output_folder, exist_ok=True) # Create folder if it doesn't exist
            img_path = generate_receipt_image(name, phone, output_folder,logo_path="logo/logo.jpg")

            # whatsapp_url = f"https://web.whatsapp.com/send?phone={phone_no_plus}"
            # webbrowser.open_new_tab(whatsapp_url)

            return render_template('success.html', name=name, phone=phone, img_path=img_path)

        except Exception as e:
            print(f"Error: {e}")
            return render_template('error.html', error_message=f"An error occurred: {e}")

    return render_template('index.html')

@app.route('/download_receipt', methods=['POST'])
def download_receipt():
    name = request.form['name']
    phone = request.form['phone']
    output_folder = "generated_files" # Define output folder

    try:
        img_path = generate_receipt_image(name, phone, output_folder)
        return send_file(img_path, as_attachment=True, download_name="receipt.png")

    except Exception as e:
        print(f"Download error: {e}")
        return render_template('error.html', error_message=f"Download error: {e}")

if __name__ == '__main__':
    app.run(debug=True)