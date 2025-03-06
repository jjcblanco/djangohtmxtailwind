import cloudinary
import cloudinary.uploader
from cloudinary.utils import cloudinary_url
from decouple import config

CLOUDINARY_CLOUD_NAME = config("CLOUDINARY_CLOUD_NAME",default="")
CLOUDINARY_PUBLIC_API_KEY = config("CLOUDINARY_API_KEY",default="693784592546469")
CLOUDINARY_SECRET_API_KEY = config("CLOUDINARY_SECRET_API_KEY",default="")

def cloudinary_init():

    # Configuration       
    cloudinary.config( 
        cloud_name = CLOUDINARY_CLOUD_NAME, 
        api_key = CLOUDINARY_PUBLIC_API_KEY, 
        api_secret = CLOUDINARY_SECRET_API_KEY, # Click 'View API Keys' above to copy your API secret
        secure=True
    )