# -*- coding: utf-8 -*-
from keras.models import Model,load_model
import os
#os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import numpy as np
import magic
import extract_features
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {'wav', 'wave'}
ALLOWED_MIME_TYPES = {'audio/wav', 'audio/x-wav'}

app = Flask(__name__)
#app.config["DEBUG"] = True
app.config["JSON_AS_ASCII"] = False

model_file = 'trained_cnn.h5'

model = load_model(model_file)

def is_allowed_file(file):
    if '.' in file.filename:
        ext = file.filename.rsplit('.', 1)[1].lower()
        print("ext: ", ext)
    else:
        return False
        
    mime_type = magic.from_buffer(file.stream.read(), mime=True)
    print('mime_type: ', mime_type)
    if (
        mime_type in ALLOWED_MIME_TYPES and
        ext in ALLOWED_EXTENSIONS
    ):
        return True
        
    return False 

@app.route('/cough/inference', methods=['POST'])
def inference():
    response = ''
    try:
        f = request.files['file']
        f.save(os.path.join('/tmp', f.filename))
        if os.path.exists(os.path.join('/tmp/ramdisk', f.filename)) and os.path.getsize(os.path.join('/tmp/ramdisk', f.filename)) > 0:
            prediction_feature = extract_features.get_features(os.path.join('/tmp/ramdisk', f.filename))
            prediction_feature = np.expand_dims(np.array([prediction_feature]),axis=2)
            predicted_vector = model.predict_classes(prediction_feature)
            if list(predicted_vector)[0] == 1:
                response = '{"response":{"cough": True}}'
            else:
                response = '{"response":{"cough": False}}'
        else:
            response = '{"response":{"cough": False}}'
    except Exception as e:
        print('Error: ', e)
        response = '{"response":{"cough": False}}'
    finally:
        if os.path.isfile(os.path.join('/tmp', f.filename)):
            os.remove(os.path.join('/tmp', f.filename))
    return response
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=False, threaded = False)         
