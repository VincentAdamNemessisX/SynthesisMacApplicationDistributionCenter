import os
from datetime import datetime


def handle_uploaded_image(file, upload_to):
    path = str(upload_to + datetime.now().strftime('%Y')
               + "/" + datetime.now().strftime('%m'))
    if not os.path.exists(path):
        os.makedirs(path)
    if file is None:
        return None
    path = (path + "/" +
            str(datetime.now().strftime('%Y-%m-%d-%H-%M-%S-'))
            + file.name)
    with open(path, "wb") as destination:
        for chunk in file.chunks():
            destination.write(chunk)
    return path
