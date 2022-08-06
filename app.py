# Import libraries
import base64
from io import BytesIO

import cv2
import imutils
import numpy as np
import requests
from flask import Flask, jsonify, request
from flask_cors import CORS

from piece_detect import get_pieces
from square_detect import get_squares

app = Flask(__name__)
# CORS(app)
CORS(app, resources={r'/*': {'origins': '*'}})

def convertBase64ToFile(base64str):
    file_bytes = base64.b64decode(base64str)
    file = BytesIO(file_bytes)
    return file



# Load the model

@app.route('/api',methods=['POST'])
def predict():
    # Get the data from the POST request.
    data = request.get_json(force=True)
    image_path = data['image_path']
    base64_img = data['base_64_image']
    print('image path:', image_path)
    # print('base64 image:', base64_img)

    fileData = convertBase64ToFile(base64_img)
    with open("./file.jpeg", 'wb') as out:
        out.write(fileData.read())

    image_path = './file.jpeg'

    image = imutils.url_to_image(image_path) if image_path.startswith('http') else cv2.imread(image_path)
    # print('length', len(image))
    # Get squares from the image
    squares = get_squares(image)
    pieces = get_pieces(image_path)
    # convert Detection objects to strings for parsing
    pieces = [str(piece) for piece in pieces]
    # squares_and_pieces = {'squares': squares, 'pieces': pieces}
    squares_and_pieces = {'squares': squares, 'pieces': pieces}
    # print('squares and pieces:', squares_and_pieces)
    return jsonify(squares_and_pieces)
    # return jsonify(squares.tolist())

@app.route('/api', methods=['GET'])
def yo():
    return jsonify([1,2,3])

# if __name__ == '__main__':
#     from waitress import serve
#     serve(app, host="0.0.0.0", port=5000)
#     # app.run(port=5000, debug=True)
