def get_cloudinary_image_object(instance, 
                          field_name="image",
                          as_html=False,
                          width=400,
                          height=400
                          ):
    if not hasattr(instance, field_name):
        return ""
    image_object = getattr(instance, field_name)
    if not image_object:
        return ""
    image_options = {	
        "width": width,
        "height": height,
        "crop": "fill"
    }
    if as_html:
        return instance.image.image(**image_options)
            
    url = instance.image.build_url(**image_options)
    return url
    
   
def get_cloudinary_video_object(instance, 
                        field_name="video",
                        as_html=False,
                        width=None,
                        height=None,
                        sign_url=False,  #para videos privados
                        fetch_format="auto",
                        quality="auto"
                        ):
    if not hasattr(instance, field_name):
        return ""
    video_object = getattr(instance, field_name)
    if not video_object:
        return ""
    video_options = {	
        "width": width,
        "height": height,
        "crop": "fill",
        "fetch_format": fetch_format,
        "quality": quality
    }
    if width:
        video_options["width"] = width
    if height:
        video_options["height"] = height
    if width and height:
        video_options["crop"] = "limit"
        

    if as_html:
        return video_object.video(**video_options)
            
    url = video_object.video.build_url(**video_options)
    return url