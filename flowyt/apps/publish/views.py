import os
import sys
import threading
import uuid
import zipfile

from flask import request
from flask_restful import Resource, abort
from werkzeug.utils import secure_filename

from flowyt.settings import STORAGE_FOLDER_TEMP_UPLOADS, WORKSPACES_PATH

from apps.publish.serializers import PublishSerializer
from utils.middlewares import secret_key_maybe_required, secret_key_required


class Reload(Resource):
    @secret_key_maybe_required
    def get(self):
        self.reload()
        return {"msg": "Reloading..."}, 200

    def reload(self):
        os.popen("ps aux |grep gunicorn |grep orechestryzi_engine|awk '{ print $2 }' |xargs kill -HUP")
        return True


class Publish(Resource):
    ALLOWED_EXTENSIONS = {"zip"}

    @secret_key_required
    def post(self):
        # check if the post request has the file part
        if "workpace_zip_file" not in request.files:
            return {"msg": "No workpace_zip_file in multipart form"}, 400

        file = request.files["workpace_zip_file"]

        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == "":
            return {"msg": "No selected file."}, 400

        if not self.allowed_file(file.filename):
            return {"msg": "The file is not a zip"}, 400

        # Store
        filename = secure_filename(str(uuid.uuid4()) + ".zip")
        file.save(os.path.join(STORAGE_FOLDER_TEMP_UPLOADS, filename))

        # Extract
        path_to_zip_file = STORAGE_FOLDER_TEMP_UPLOADS + "/" + filename
        directory_to_extract_to = WORKSPACES_PATH

        with zipfile.ZipFile(path_to_zip_file, "r") as zip_ref:
            zip_ref.extractall("{0}/{1}".format(directory_to_extract_to, file.filename[:-4]))

        # Remove upload
        os.remove(path_to_zip_file)

        return {"msg": "The workspace {0} upload was completed successfully!".format(file.filename[:-4])}, 200

    def allowed_file(self, filename):
        return "." in filename and filename.rsplit(".", 1)[1].lower() in self.ALLOWED_EXTENSIONS
