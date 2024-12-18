import numpy as np
import cv2
import base64


def resize_image(img_base64, size):
    '''

        Function to resize a image.
        Inputs: bytes image
                size
        Output: resized bytes image
    '''
    img_data = base64.b64decode(img_base64)
    nparr = np.frombuffer(img_data, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    # Resize image
    resized_image = cv2.resize(image, (size, size))
    
    # Encode resized image to base64
    _, img_encoded = cv2.imencode('.jpg', resized_image)
    resized_base64 = base64.b64encode(img_encoded).decode('utf-8')
    
    return resized_base64