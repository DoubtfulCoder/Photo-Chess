import cv2
import numpy as np
import requests

url = 'http://localhost:5000/api'
r = requests.post(url,json={'image_path':'images/IMG_20220118_210009652.jpg',})
# retrieve data and convert to numpy array
new_img = np.array(r.json())
# change type for opencv to use
new_img = new_img.astype(np.uint8)

print(type(new_img))

cv2.imshow('new_img', new_img)
cv2.imwrite('new_img.png', new_img)
cv2.waitKey(0)
