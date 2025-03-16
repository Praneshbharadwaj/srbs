from flask import Flask, render_template, request, send_file
from PIL import Image, ImageDraw, ImageFont
import os

app = Flask(__name__)

from PIL import Image, ImageDraw, ImageFont
import os

from utils.num2str import *
from datetime import datetime
from utils.serial_num import increment_counter

ramothsava_year = 119
input_stroke_width = 0.5

input_name_x = 320

def generate_receipt_image(
    name,
    phone,
    address_line1,
    address_line2,
    amount,
    output_folder,
    logo_path=None,
    signature_path=None,
):
    """Generates a PNG receipt image with address lines, amount, logo, border, signature, and different font sizes."""

    print("Inside generate function")
    width, height = 800, 600
    img = Image.new("RGB", (width, height), color="white")
    d = ImageDraw.Draw(img)

    print("Image created")

    try:
        receipt_font = ImageFont.truetype("arial.ttf", 32)
        data_font = ImageFont.truetype("arial.ttf", 18)
        address_font = ImageFont.truetype("arial.ttf", 18)
    except IOError:
        receipt_font = ImageFont.load_default()
        data_font = ImageFont.load_default()
        address_font = ImageFont.load_default()

    print("Fonts generated")

    serial_num = increment_counter("D:/Prathith/SRBS_119/Receipts/serial_num.txt")
    # Convert amount ruppes to words
    now = datetime.now()
    formatted_date = now.strftime("%d-%m-%Y")
    amount_str = number_to_words_rupees(int(amount))
    srbs_text = f"Sri Rama Bhaktha Sabha (R)"
    receipt_text = f"E-Receipt"
    name_text = f"{name}"
    phone_text = f"{phone}"
    address_line1_text = f"{address_line1}"
    address_line2_text = f"{address_line2}"
    towards_text = f"Towards {ramothsava_year}th year ramothsava celebrations "
    amount_text = f"₹{amount}"
    amount_words_text = f"{amount_str} Only"
    sign_text = "Signature"
    serial_num_txt = str(serial_num)

    template_name = "Received with thanks from Sri/Smt:"
    template_amount = "Amount: "
    template_amount_words = "Amount in words: "
    template_date = "Date: "
    template_sl_no = "No.: "

    print("Yet to generate textbox")

    receipt_bbox = d.textbbox((0, 0), receipt_text, font=receipt_font)
    srbs_bbox = d.textbbox((0, 0), srbs_text, font=receipt_font)
    name_bbox = d.textbbox((0, 0), name_text, font=data_font)
    phone_bbox = d.textbbox((0, 0), phone_text, font=data_font)
    address_line1_bbox = d.textbbox((0, 0), address_line1_text, font=address_font)
    address_line2_bbox = d.textbbox((0, 0), address_line2_text, font=address_font)
    amount_bbox = d.textbbox((0, 0), amount_text, font=data_font)
    amount_words_bbox = d.textbbox((0, 0), amount_words_text, font=data_font)
    towards_bbox = d.textbbox((0, 0), amount_words_text, font=data_font)
    sign_bbox = d.textbbox((0, 0), sign_text, font=data_font)
    formatted_date_bbox = d.textbbox((0, 0), formatted_date, font=data_font)

    print("Generated bboxes!")

    receipt_width = receipt_bbox[2] - receipt_bbox[0]
    receipt_height = receipt_bbox[3] - receipt_bbox[1]
    srbs_width = srbs_bbox[2] - srbs_bbox[0]
    srbs_height = srbs_bbox[3] - srbs_bbox[1]
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
    amount_words_height = amount_words_bbox[3] - amount_words_bbox[1]
    sign_width = sign_bbox[2] - sign_bbox[0]
    sign_height = sign_bbox[3] - sign_bbox[1]
    formatted_date_width = formatted_date_bbox[2] - formatted_date_bbox[0]
    formatted_date_height = formatted_date_bbox[3] - formatted_date_bbox[1]

    print("Got bbox details")

    receipt_x = (width - receipt_width) // 2
    srbs_x = (width - srbs_width) // 2
    template_name_x = 20
    name_x = input_name_x
    phone_x = input_name_x
    address_line1_x = input_name_x
    address_line2_x = input_name_x
    template_amount_x = 20
    template_amount_words_x = 20
    amount_x = 200
    amount_words_x = 200
    towards_x = 20
    sign_x = width - sign_width - 30
    formatted_date_x = 560
    template_date_x = 500
    template_sl_no_x = 20
    serial_num_x = 80

    srbs_y = 30
    receipt_y = srbs_y + srbs_height + 15
    formatted_date_y = receipt_y + receipt_height + 20
    template_date_y = formatted_date_y
    template_name_y = formatted_date_y + formatted_date_height + 30
    name_y = formatted_date_y + formatted_date_height + 30
    phone_y = name_y + name_height + 15
    address_line1_y = phone_y + phone_height + 15
    address_line2_y = address_line1_y + address_line1_height + 10
    template_amount_y = address_line2_y + address_line2_height + 15
    amount_y = address_line2_y + address_line2_height + 15
    template_amount_words_y = amount_y + amount_height + 15
    amount_words_y = amount_y + amount_height + 15
    towards_y = amount_words_y + amount_words_height + 15
    sign_y = height - sign_height - 10
    template_sl_no_y = formatted_date_y
    serial_num_y = formatted_date_y

    d.text((srbs_x, srbs_y), srbs_text, fill="blue", font=receipt_font)
    d.text((receipt_x, receipt_y), receipt_text, fill="blue", font=receipt_font)
    d.text((name_x, name_y), name_text, fill="black", font=data_font, stroke_width=input_stroke_width, stroke_fill='black')
    d.text((template_name_x, template_name_y), template_name, fill="black", font=data_font)
    d.text((phone_x, phone_y), phone_text, fill="black", font=data_font, stroke_width=input_stroke_width, stroke_fill='black')
    d.text(
        (address_line1_x, address_line1_y),
        address_line1_text,
        fill="black",
        font=address_font, stroke_width=input_stroke_width, stroke_fill='black'
    )
    d.text(
        (address_line2_x, address_line2_y),
        address_line2_text,
        fill="black",
        font=address_font, stroke_width=input_stroke_width, stroke_fill='black'
    )
    d.text((template_amount_x, template_amount_y), template_amount, fill="black", font=data_font)
    d.text((template_amount_words_x, template_amount_words_y), template_amount_words, fill="black", font=data_font)
    d.text((amount_x, amount_y), amount_text, fill="black", font=data_font, stroke_width=input_stroke_width, stroke_fill='black')
    d.text(
        (amount_words_x, amount_words_y),
        amount_words_text,
        fill="black",
        font=data_font, stroke_width=input_stroke_width, stroke_fill='black'
    )
    d.text((towards_x, towards_y), towards_text, fill="black", font=data_font)
    d.text((sign_x - 20, sign_y - 10), sign_text, fill="black", font=data_font)
    d.text(
        (formatted_date_x, formatted_date_y),
        formatted_date,
        fill="black",
        font=data_font, stroke_width=input_stroke_width, stroke_fill='black'
    )
    d.text((template_date_x, template_date_y), template_date, fill="black", font=data_font)
    d.text((template_sl_no_x, template_sl_no_y), template_sl_no, fill="black", font=data_font)
    d.text((serial_num_x, serial_num_y), serial_num_txt, fill="red", font=data_font)

    print("Added details to image")

    if logo_path and os.path.exists(logo_path):
        try:
            logo = Image.open(logo_path)
            logo = logo.resize((100, 140))
            img.paste(logo, (width - 140, 20))
        except Exception as e:
            print(f"Error adding logo: {e}")

    if signature_path and os.path.exists(signature_path):
        try:
            signature = Image.open(signature_path)
            signature = signature.resize((100, 50))
            img.paste(signature, (width - 110, height - 90))
        except Exception as e:
            print(f"Error adding signature: {e}")

    border_color = "black"
    border_width = 5
    d.rectangle(
        [(10, 10), (width - 10, height - 10)], outline=border_color, width=border_width
    )

    image_filename = f"{name.replace(' ', '_')}_{phone}.png"
    image_path = os.path.join(output_folder, image_filename)
    img.save(image_path, "PNG")
    print(f"PNG generated successfully and saved to: {image_path}")
    return image_path