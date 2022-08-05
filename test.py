import cv2
import imutils

image = imutils.url_to_image('https://www.fnordware.com/superpng/pnggrad8rgb.png')
cv2.imshow('img', image)
cv2.waitKey(0)
