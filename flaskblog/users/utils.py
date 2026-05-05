import cloudinary.uploader
import os
import secrets
from PIL import Image
from flask import url_for, current_app, flash
# from flask_mail import Message
# from flaskblog import mail


# def save_picture(form_picture):
#     random_hex = secrets.token_hex(8)
#     _, f_ext = os.path.splitext(form_picture.filename)
#     pic_name = random_hex + f_ext
#     pic_path = os.path.join(current_app.root_path, "static/profile_pics", pic_name)

#     output_size = (125, 125)
#     i = Image.open(form_picture)
#     i.thumbnail(output_size)
#     i.save(pic_path)

#     return pic_name

# def delete_picture(pic_name):
#     if pic_name and pic_name != "default.jpg":
#         pic_path = os.path.join(current_app.root_path, "static/profile_pics", pic_name)
#         if os.path.exists(pic_path):
#             os.remove(pic_path)

# def save_picture(form_picture):
#     random_hex = secrets.token_hex(8)
#     _, f_ext = os.path.splitext(form_picture.filename)
#     f_ext = (f_ext or "").lower()
#     pic_name = random_hex + f_ext
#     pic_dir = os.path.join(current_app.root_path, "static", "profile_pics")
#     os.makedirs(pic_dir, exist_ok=True)
#     pic_path = os.path.join(pic_dir, pic_name)

#     output_size = (125, 125)
#     i = Image.open(form_picture)
#     i.thumbnail(output_size)
#     if f_ext in (".jpg", ".jpeg"):
#         i.convert("RGB").save(pic_path, "JPEG", quality=85)
#     else:
#         i.save(pic_path)

#     return pic_name


# def delete_picture(pic_name):
#     if pic_name and pic_name != "default.jpg":
#         pic_path = os.path.join(current_app.root_path, "static/profile_pics", pic_name)
#         if os.path.exists(pic_path):
#             os.remove(pic_path)

def save_picture(form_picture):
    upload_result = cloudinary.uploader.upload(
        form_picture,
        folder="profile_pics", 
        transformation=[
            {"width": 125, "height": 125, "crop": "fill"}
        ]
    )

    return {
        "url": upload_result["secure_url"],
        "public_id": upload_result["public_id"]
    }


def delete_picture(public_id):
    if public_id:
        try:
            cloudinary.uploader.destroy(public_id)
        except Exception:
            pass

def send_email(user):    
    # if not current_app.config.get('MAIL_USERNAME') or not current_app.config.get('MAIL_PASSWORD'):
    #     raise RuntimeError('EMAIL_USER and EMAIL_PASS environment variables must be set to send reset emails.')

#     token = user.get_token()
#     msg = Message("Reset Password Request", sender=current_app.config['MAIL_USERNAME'], recipients=[user.email])
#     msg.body = f'''To reset your password, click the following link:
# {url_for("users.reset_token", token=token, _external=True)}
# If you did not make this request then simply ignore this email and no changes will be made.
# ''' 
    # mail.send(msg)
    flash("Password reset feature is temporarily disabled.", "info")
