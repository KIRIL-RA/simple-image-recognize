import cv2 as cv
import numpy as np

img = cv.imread("YOUR IMAGE PATH")
template = cv.imread("YOUR TEMPLATE PATH")

# Color parametrs for processing on symbol template
lower_color = np.array([100,100, 100])
upper_color = np.array([110,255,255])

# Color parametrs for processing on image
lower_color_ = np.array([93, 139, 37])
upper_color_ = np.array([255, 255, 255])

def processing(image, lower_color, upper_color):
    
    '''
    Function to find contours
    Returns an array of contours
    '''

    # Change color space
    hsv = cv.cvtColor(image, cv.COLOR_BGR2HSV)

    # Apply color filter
    mask = cv.inRange(hsv, lower_color, upper_color)

    # Find contours
    im2, contours, hierarchy = cv.findContours(mask, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)

    # Sort countors from small to large
    contours = sorted(contours, key=cv.contourArea, reverse=True)
    return contours

def compare(img_contours, tmp_contours):

    '''
    Function to search for a pattern in the picture
    If successful, returns the contouer of the found object
    Returns None on failure
    '''

    # Parameter designation
    coef = []
    max_coef_param = 0.17

    # Minimum size of the searched object
    min_size_obj_param = 120

    # Search the template on image
    for img_contours_ in img_contours:
        if len(img_contours_) >= min_size_obj_param:
            coef_buffer = cv.matchShapes(img_contours_, tmp_contours[0], 1, 0.0)
            coef.append(coef_buffer)
            if coef_buffer == min(coef):
                result_img_contour = img_contours_
            
    if min(coef) < max_coef_param:
        return result_img_contour
    else:
        return None

contours_image = processing(img, lower_color_, upper_color_)
contours_template = processing(template, lower_color, upper_color)

result_img = compare(contours_image, contours_template)

# Draw countuors on images
cv.drawContours(img, result_img, -1, (255, 0, 255), 3)
cv.drawContours(template, contours_template[0], -1, (255, 0, 255), 3)

# Show images with contuors
cv.imshow("Contours_img", img)
cv.imshow("Contours_tmp", template)
cv.waitKey(10000000)