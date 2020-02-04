import asyncio
import os
import uuid
import zipfile
import sys

from flask import request
from flask_restful import Resource, abort
from orchestrator.settings import STORAGE_FOLDER_TEMP_UPLOADS, WORKSPACES_PATH
from werkzeug.utils import secure_filename

from apps.build.serializers import BuildSerializer

ALLOWED_EXTENSIONS = {"zip"}

class Reload(Resource):
    def get(self):
        os.execl(sys.executable, os.path.abspath(__file__), *sys.argv) 

class BuildWorkspace(Resource):
    def post(self):
        # check if the post request has the file part
        if 'workpace_zip_file' not in request.files:
            return {"msg": "No workpace_zip_file in multipart form"}, 400

        file = request.files['workpace_zip_file']

        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            return {"msg": "No selected file."}, 400

        if not self.allowed_file(file.filename):
            return {"msg": "The file is not a zip"}, 400

        # Store
        filename = secure_filename(str(uuid.uuid4()) + ".zip")
        file.save(os.path.join(STORAGE_FOLDER_TEMP_UPLOADS, filename))

        # Extract
        path_to_zip_file = STORAGE_FOLDER_TEMP_UPLOADS + "/" + filename
        directory_to_extract_to = WORKSPACES_PATH

        with zipfile.ZipFile(path_to_zip_file, 'r') as zip_ref:
            zip_ref.extractall(directory_to_extract_to)

        # Remove upload
        os.remove(path_to_zip_file)

        return {"msg": "The workspace upload was completed successfully!"}, 200
                                    
    def allowed_file(self, filename):
        return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
