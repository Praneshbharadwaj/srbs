from flask import Flask, render_template, request, send_file, redirect, url_for
from PIL import Image, ImageDraw, ImageFont  # Using PIL for image generation
import os
import qrcode
import pywhatkit  # For WhatsApp integration (requires installation)
import tempfile

app = Flask(__name__)

def generate_receipt_image(name, phone, temp_file_path):
    """Generates a PNG receipt image."""
    width, height = 400, 300
    img = Image.new('RGB', (width, height), color='white')
    d = ImageDraw.Draw(img)

    font = ImageFont.load_default()  # You can specify a custom font here

    d.text((20, 20), "Receipt", fill='black', font=font)
    d.text((20, 50), f"Name: {name}", fill='black', font=font)
    d.text((20, 80), f"Phone: {phone}", fill='black', font=font)
    # Add more receipt details here...

    img.save(temp_file_path, 'PNG')
    print("PNG generated successfully!!!")

def generate_qr_code(phone, temp_qr_path):
    """Generates a QR code for the WhatsApp number."""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(f"whatsapp://send?phone={phone}")
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img.save(temp_qr_path)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        phone_no_plus = "+" + phone if not phone.startswith('+') else phone

        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_img:
                img_path = temp_img.name
                print(f"Image Path: {img_path}")
                generate_receipt_image(name, phone, img_path)
            with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_qr:
                qr_path = temp_qr.name
                generate_qr_code(phone_no_plus, qr_path)

            try:
                # Attempt to send via WhatsApp, handling potential errors
                # pywhatkit.sendwhats_image(phone_no_plus, qr_path, "Scan this QR code to chat with the provided number", wait_time=10, tab_close=True)
                pywhatkit.sendwhats_image(phone_no_plus, img_path, "Receipt", wait_time=50, tab_close=True)
                return render_template('success.html', name=name, phone=phone)

            except Exception as e:
                print(f"WhatsApp sending error: {e}")
                return render_template('error.html', error_message=f"Error sending WhatsApp message: {e}")

        except Exception as e:
            print(f"Error generating Image: {e}")
            return render_template('error.html', error_message=f"Error generating Image: {e}")

        # finally:
        #     if 'img_path' in locals() and os.path.exists(img_path):
        #         os.unlink(img_path)
        #     if 'qr_path' in locals() and os.path.exists(qr_path):
        #         os.unlink(qr_path)

    return render_template('index.html')

@app.route('/download_receipt', methods=['POST'])
def download_receipt():
    name = request.form['name']
    phone = request.form['phone']

    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_img:
            img_path = temp_img.name
            generate_receipt_image(name, phone, img_path)

        return send_file(img_path, as_attachment=True, download_name="receipt.png")

    except Exception as e:
        print(f"Download error: {e}")
        return render_template('error.html', error_message=f"Download error: {e}")

    finally:
        if 'img_path' in locals() and os.path.exists(img_path):
            os.unlink(img_path)

if __name__ == '__main__':
    app.run(debug=True)