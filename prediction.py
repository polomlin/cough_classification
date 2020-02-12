# -*- coding: utf-8 -*-

from keras.utils import to_categorical
from keras.models import load_model
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import extract_features
import nn
import glob
import numpy as np
import shutil


def create_cnn(num_labels):

    model = Sequential()
    model.add(Conv1D(64, 3, activation='relu', input_shape=(40, 1)))
    model.add(Conv1D(64, 3, activation='relu'))
    model.add(MaxPooling1D(3))
    model.add(Conv1D(128, 3, activation='relu'))
    model.add(Conv1D(128, 3, activation='relu'))
    model.add(GlobalAveragePooling1D())
    model.add(Dropout(0.5))
    model.add(Dense(num_labels))
    model.add(Activation('softmax'))
    return model

def predict(filenames,le,model_file, kind):
    model = load_model(model_file)
    for filename in filenames:
        prediction_feature = extract_features.get_features(filename)
        #if model_file == "trained_mlp.h5":
        #    prediction_feature = np.array([prediction_feature])
        #elif model_file == "trained_cnn.h5":
        prediction_feature = np.expand_dims(np.array([prediction_feature]),axis=2)

        predicted_vector = model.predict_classes(prediction_feature)
        predicted_proba_vector = model.predict_proba([prediction_feature])

        predicted_proba = predicted_proba_vector[0]
        for i in range(len(predicted_proba)):
            category = le.inverse_transform(np.array([i]))
            print(category[0], "\t\t : ", format(predicted_proba[i], '.32f') )

def predict_move(filenames, model_file):
    model = load_model(model_file)
    for filename in filenames:
        prediction_feature = extract_features.get_features(filename)
        prediction_feature = np.expand_dims(np.array([prediction_feature]),axis=2)
        predicted_vector = model.predict_classes(prediction_feature)
        if list(predicted_vector)[0] == 1:
            #base = os.path.basename(filename)
            shutil.copy2(filename, '/home/sam/Music/cough/asr/waiting_filter/')

if __name__ == "__main__":
    le = LabelEncoder()
    # one hot encoded labels
    #allpaths = glob.glob('/home/sam/Music/cough/asr/test/yes/*.wav')
    #predict(allpaths,le,"trained_cnn.h5",'yes')

    #allpaths = glob.glob('/home/sam/Music/cough/asr/test/no/*.wav')
    #predict(allpaths,le,"trained_cnn.h5", 'no')

    allpaths = glob.glob('/home/sam/Music/human_sound_effect/wav/*.wav')
    predict_move(allpaths,"trained_cnn.h5")



