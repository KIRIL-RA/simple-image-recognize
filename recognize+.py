# Modified version

import cv2 as cv
import numpy as np

img = cv.imread("/home/kirill/Desktop/pythonproj/gowoard_.png")
template = [cv.imread("/home/kirill/Desktop/pythonproj/pedestrain.png"), cv.imread("/home/kirill/Desktop/pythonproj/template_sample.png")]
template_names = ['right', 'forward']

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
    return contours, mask

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
        return min(coef), result_img_contour
    else:
        return None, None

def compare_patterns(image, template_arr, template_name_arr):

    '''
    Function to find the most suitable pattern
    If succes, returns the name of pattern
    Returns None on failure
    '''

    # Color parametrs for processing on symbol template
    lower_color = np.array([100,100, 100])
    upper_color = np.array([110,255,255])
    
    # Color parametrs for processing on image
    lower_color_ = np.array([93, 139, 37])
    upper_color_ = np.array([255, 255, 255])

    contours_image, mask_img = processing(img, lower_color_, upper_color_)
    contours_template = []
    mask_template = []
    for template_arr_ in template_arr:
        contours_template_, mask_tmp = processing(template_arr_, lower_color, upper_color)
        mask_template.append(mask_tmp)
        contours_template.append(contours_template_)

    for contour_ in range(len(contours_template)):
        cv.drawContours(template_arr[contour_], contours_template[contour_], -1, (255, 0, 255), 3)
        temp_buf = cv.resize(template_arr[contour_], (300, 300))
        cv.imshow(str(contour_), temp_buf)

        mask_template[contour_] = cv.resize(mask_template[contour_], (300, 300))
        cv.imshow(str(contour_ + 100), mask_template[contour_])
    
    coef_arr = []
    for contours_template_ in contours_template:
        coef, result = compare(contours_image, contours_template_)
        if coef != None:
            coef_arr.append(coef)
        else:
            coef_arr.append(1000)

        cv.drawContours(image, result, -1, (255, 0, 255), 3)

    cv.imshow("Contours_img", image)
    cv.imshow("Mask_img", mask_img)

    for number in range(len(coef_arr)):
        if coef_arr[number] == min(coef_arr):
            return template_name_arr[number]
    return None

print(compare_patterns(img, template, template_names))
cv.waitKey(10000000)