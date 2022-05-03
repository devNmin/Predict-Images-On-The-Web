
import numpy as np
import cv2
import tensorflow as tf



def predict_file(image_file):
    
    model = tf.keras.applications.MobileNetV2(input_shape=(128,128,3),weights='imagenet')
    src = cv2.imread(image_file) 
    dst = cv2.resize(src, (128, 128))
    img = np.reshape(dst,[1,128,128,3])
    preprocessed_images = tf.keras.applications.mobilenet_v2.preprocess_input(img)
    preds = model.predict(preprocessed_images)
    topK = 1
    y_pred_top = tf.keras.applications.mobilenet_v2.decode_predictions(preds, top=topK)
    
    return  y_pred_top[0][0][1]
