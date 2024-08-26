import os
import secrets

from PIL import Image
from tasks.configs import celery_app


@celery_app.task
def upload_picture(file_content: bytes, filename: str, dir: str):
    extension = filename.split(".")[-1].lower()
    if extension not in ["jpg", "png"]:
        return "File extension must be .jpg or .png"

    token_name = secrets.token_hex(10) + "." + extension
    generated_name = os.path.join(dir, token_name)

    # Save the file
    try:
        with open(generated_name, "wb") as out_file:
            out_file.write(file_content)
    except Exception as e:
        return f"Error saving file: {str(e)}"

    # Process the image
    try:
        with Image.open(generated_name) as img:
            img = img.resize((512, 512))
            img.save(generated_name)
    except Exception as e:
        return f"Error processing image: {str(e)}"

    # Assume all paths involve 'static/' for simplicity
    file_url = generated_name
    return file_url
