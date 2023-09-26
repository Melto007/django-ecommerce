"""Image file upload"""

import cloudinary
import datetime


def upload_image(file):
    url = cloudinary.uploader.upload(
        file,
        public_id=f'image/{datetime.datetime.utcnow()}',
        use_filename=True,
        unique_filename=True
    )
    return url
