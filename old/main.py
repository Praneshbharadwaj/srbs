from flask import Flask, render_template, request, send_file, redirect, url_for
from fpdf import FPDF
import os
import qrcode
import pywhatkit  # For WhatsApp integration (requires installation)
import tempfile

app = Flask(__name__)

def generate_receipt_pdf(name, phone, temp_file_path):
    """Generates a PDF receipt."""
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt="Receipt", ln=1, align='C')
    pdf.cell(200, 10, txt=f"Name: {name}", ln=1)
    pdf.cell(200, 10, txt=f"Phone: {phone}", ln=1)
    # Add more receipt details here...

    pdf.output(temp_file_path)
    print("PDF generated successfully!!!")

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
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
                pdf_path = temp_pdf.name
                print(f"PDF Path: {pdf_path}")
                generate_receipt_pdf(name, phone, pdf_path)
            with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_qr:
                qr_path = temp_qr.name
                generate_qr_code(phone_no_plus, qr_path)

            try:
                # Attempt to send via WhatsApp, handling potential errors
                pywhatkit.sendwhats_image(phone_no_plus, qr_path, "Scan this QR code to chat with the provided number", wait_time=10, tab_close=True)
                pywhatkit.sendwhats_pdf(phone_no_plus, pdf_path, "Receipt", wait_time=10, tab_close=True)
                return render_template('success.html', name=name, phone=phone)

            except Exception as e:
                print(f"WhatsApp sending error: {e}")
                return render_template('error.html', error_message=f"Error sending WhatsApp message: {e}")

        except Exception as e:
            print(f"Error generating PDF: {e}")
            return render_template('error.html', error_message=f"Error generating PDF: {e}")

        finally:
            if 'pdf_path' in locals() and os.path.exists(pdf_path):
                os.unlink(pdf_path)
            if 'qr_path' in locals() and os.path.exists(qr_path):
                os.unlink(qr_path)


    return render_template('index.html')

@app.route('/download_receipt', methods=['POST'])
def download_receipt():
    name = request.form['name']
    phone = request.form['phone']

    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
            pdf_path = temp_pdf.name
            generate_receipt_pdf(name, phone, pdf_path)

        return send_file(pdf_path, as_attachment=True, download_name="receipt.pdf")

    except Exception as e:
        print(f"Download error: {e}")
        return render_template('error.html', error_message=f"Download error: {e}")

    finally:
        if 'pdf_path' in locals() and os.path.exists(pdf_path):
            os.unlink(pdf_path)

if __name__ == '__main__':
    app.run(debug=True)