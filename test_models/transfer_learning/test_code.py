from keras.models import load_model
import cv2
import numpy as np

def model_pred(model_h5, test_file):
    
    image_size = 160
    model = load_model(model_h5)
    # model.summary()
    model.compile(loss='binary_crossentropy',
                optimizer='rmsprop',
                metrics=['accuracy'])

    img = cv2.imread(test_file)
    img = cv2.resize(img,(image_size,image_size))
    img = np.reshape(img,[1,image_size,image_size,3])

    classes = model.predict_classes(img)
    class_all = ['Cat','Dog']
    result = class_all[np.squeeze(classes)]

    return result