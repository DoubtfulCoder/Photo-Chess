import math

import cv2
import numpy as np

from sort_rows import sort_coords_into_rows

path1 = './images/bishop-lines.png'
path2 = './images/download (2).png'
path3 = './images/download (3).png'
path4 = './images/king with canny edges.png'
path5 = 'images/IMG_20220118_205107650.jpg'
path6 = 'images/IMG_20220118_220359732.jpg'
path7 = 'images/IMG_20220118_210009652.jpg'

# img = cv2.imread(path7)

def get_squares(img):
    # resize image
    resized_image = cv2.resize(img, (276, 368))
    # resized_image = cv2.resize(img, (512, 512))
    # convert to grayscale
    gray = cv2.cvtColor(resized_image, cv2.COLOR_RGBA2GRAY)
    # canny edge detect for making edges more clear
    edges = cv2.Canny(gray, 58, 255, apertureSize=3)
    gray = edges.copy()
    img = resized_image

    # cv2.imshow('img', img)
    # cv2.imshow('gray', gray)

    # img = cv2.imread(path4)
    # gray = cv2.cvtColor(img, cv2.COLOR_RGBA2GRAY)
    # cv2.imshow('img', img)
    # cv2.imshow('gray', gray)
    # cv2.waitKey(0)

    # needed later for checking a square's percent of total area
    height, width = img.shape[:2]
    total_image_area = height * width

    contours, _ = cv2.findContours(
        gray, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)

    # coordinates of board
    boardMinX = 0
    boardMaxX = 0
    boardMinY = 0
    boardMaxY = 0

    # coordinates of all detected squares
    centerXs = []
    centerYs = []
    widths = []
    heights = []

    # adds square's coordinates to lists

    def add_to_squares(x_center, y_center, width, height):
        centerXs.append(x_center)
        centerYs.append(y_center)
        widths.append(width)
        heights.append(height)

    image_number = 0

    for cnt in contours:
        # approximates the shape of the contour
        approx = cv2.approxPolyDP(cnt, 0.05*cv2.arcLength(cnt, True), True)
        # get rectangle approximation of shape
        x, y, w, h = cv2.boundingRect(cnt)

        # check for entire board detection and extract coordinates
        # board will probably at least 40% of area of image
        if cv2.contourArea(cnt) > 0.3*total_image_area:
            # print('board area', cv2.contourArea(cnt))
            minX = math.inf
            maxX = -math.inf
            minY = math.inf
            maxY = -math.inf
            # find minimum and maximum x and y coordinates of board
            for coord in approx:
                for x_coord, y_coord in coord:
                    minX = x_coord if x_coord < minX else minX
                    maxX = x_coord if x_coord > maxX else maxX
                    minY = y_coord if y_coord < minY else minY
                    maxY = y_coord if y_coord > maxY else maxY
            boardMinX += minX
            boardMaxX += maxX
            boardMinY += minY
            boardMaxY += maxY
            # print(boardMinX, boardMaxX, boardMinY, boardMaxY)
            # print(approx)
            cv2.rectangle(img, (boardMinX, boardMinY),
                          (boardMaxX, boardMaxY), (255, 0, 0), 2)

        # check for individual squares on board and extract coordinates
        elif len(approx) == 4 and cv2.contourArea(cnt) > 500.0:
            # elif True:
            # check if shape is square (width and height rougly equal)
            if w/h > 0.75 and w/h < 1.25:
                if image_number == 7:
                    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                else:
                    cv2.rectangle(img, (x, y), (x + w, y + h),
                                  (36, 255, 12), 2)
                # append center of square, width, height to lists
                centerXs.append(int(x + 0.5 * w))
                centerYs.append(int(y + 0.5 * h))
                widths.append(int(w))
                heights.append(int(h))
                # cv2.rectangle(img, (x+w, y), (x + 2*w, y + h), (36,255,12), 2)
                # cv2.rectangle(img, (x-w, y), (x, y + h), (36,255,12), 2)
                # ROI = img[y:y+h, x:x+w]
                # cv2.imwrite('ROI_{}.png'.format(image_number), ROI)
                image_number += 1

    # do 4 passes of all squares to estimate missing neighboring squares
    for i in range(4):
        # loop through every square
        for i in range(len(centerXs)):

            centerX = centerXs[i]
            centerY = centerYs[i]
            width = widths[i]
            height = heights[i]

            # estimate coordinates of neighboring squares
            rightX = centerX + width
            leftX = centerX - width
            upY = centerY - height
            downY = centerY + height

            # check if neighboring squares are missing
            is_square_to_right = False
            is_square_to_left = False
            is_square_to_up = False
            is_square_to_down = False

            # check if neighboring squares are missing
            for j in range(len(centerXs)):
                other_centerX = centerXs[j]
                other_centerY = centerYs[j]

                # check if other square is a neighboring square (rougly same x or same y)
                approxSameX = abs(other_centerX - centerX) < 20
                approxSameY = abs(other_centerY - centerY) < 20

                # check if there is a square to right/left/up/down
                # if not, then we fill approximate it
                if (abs(other_centerX - rightX) < 20 and approxSameY):
                    is_square_to_right = True
                elif (abs(other_centerX - leftX) < 20 and approxSameY):
                    is_square_to_left = True
                elif (abs(other_centerY - upY) < 20 and approxSameX):
                    is_square_to_up = True
                elif (abs(other_centerY - downY) < 20 and approxSameX):
                    is_square_to_down = True

            # draw missing squares (must be within bounds of board)
            # e.g. if the center of the new square is (90, 70) but
            # the max x-coordinate of the board is only 80, then we don't draw it
            if (rightX < boardMaxX and not is_square_to_right):
                cv2.rectangle(
                    img,
                    # rightX is the the CENTER x coordinate but we need
                    # the top left corner x so we subtract half the width
                    (int(rightX - width/2), int(centerY - height/2)),
                    (int(rightX + width/2), int(centerY + height/2)),
                    (0, 0, 255), 2
                )
                add_to_squares(rightX, centerY, width, height)

            if (leftX > boardMinX and not is_square_to_left):
                cv2.rectangle(
                    img,
                    # leftX is the the CENTER x coordinate but we need
                    # the top left corner x so we subtract half the width
                    (int(leftX - width/2), int(centerY - height/2)),
                    (int(leftX + width/2), int(centerY + height/2)),
                    (0, 0, 255), 2
                )
                add_to_squares(leftX, centerY, width, height)

            if (upY > boardMinY and not is_square_to_up):
                cv2.rectangle(
                    img,
                    # upY is the the CENTER y coordinate but we need
                    # the top left corner y so we subtract half the height
                    (int(centerX - width/2), int(upY - height/2)),
                    (int(centerX + width/2), int(upY + height/2)),
                    (0, 0, 255), 2
                )
                add_to_squares(centerX, upY, width, height)

            # if (downY < boardMinY and not is_square_to_down):
            if (downY < boardMaxY and not is_square_to_down):
                cv2.rectangle(
                    img,
                    # downY is the the CENTER y coordinate but we need
                    # the top left corner y so we subtract half the height
                    (int(centerX - width/2), int(downY - height/2)),
                    (int(centerX + width/2), int(downY + height/2)),
                    (0, 0, 255), 2
                )
                add_to_squares(centerX, downY, width, height)

    # print(centerXs)
    # print(centerYs)
    print('len centerXs', len(centerXs))
    print('len centerYs', len(centerYs))
    # print(is_square_to_right, is_square_to_left,
    #       is_square_to_up, is_square_to_down)

    # print(centerXs)
    # centerXs.sort()
    # print(centerXs)
    # bothCenters = [centerXs, centerYs]
    # bothCenters = sorted(bothCenters, key=itemgetter(1))
    # bothCenters = zip(*bothCenters)
    # print(bothCenters)
    # bothCenters.sort(key=lambda x: x[1])
    # bothCenters = zip(*bothCenters)
    # print(bothCenters[0])
    # print(bothCenters[1])

    # test = np.array([[150, 170, 130, 190, 110], [10, 8, 7, 9, 11]])
    # correct_indices = test[1].argsort()
    # test = test[:, correct_indices]
    # print(test)

    both_centers = np.array([centerXs, centerYs])
    correct_indices = both_centers[1].argsort()
    both_centers = both_centers[:, correct_indices]
    # sort first 8 values of first row in both_centers
    # print(both_centers[0, :8].argsort())

    both_centers = sort_coords_into_rows(np.array(both_centers[1]), np.array(both_centers[0]))
    print('both centers:', both_centers)

    cv2.imwrite('./frontend/assets/result.png', img)

    # cv2.imshow('img', img)
    # cv2.waitKey(0)
    return both_centers
