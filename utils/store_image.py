import requests
import uuid

import cloudinary
import cloudinary.uploader
import cloudinary.api

# Configure Cloudinary
cloudinary.config(
    cloud_name="di30awmhx",
    api_key="618963697678824",
    api_secret="Qwf1GzcxD6c_QGtOWgOX9I9Sr_8"
)  

def upload_image_to_C(img_buffer, file_name):
    
    try:
        
        img_buffer.seek(0)
        response = cloudinary.uploader.upload(img_buffer,resource_type = "image")
        image_url = response["secure_url"]
        return image_url
    except Exception as e :
        print("error occurec",e)

