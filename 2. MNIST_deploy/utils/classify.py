import numpy as np


# Classification function
def classify_image(image, svc):
    '''

        Function to classify Image.

    '''
    image = image.convert('L').resize((28, 28))
    img_array = np.array(image)
    img_array = img_array.flatten()
    prediction = svc.predict([img_array])
    return prediction[0]