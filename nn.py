from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Conv1D, GlobalAveragePooling1D, MaxPooling1D
from keras.models import load_model
import extract_features
from sklearn.preprocessing import LabelEncoder
import numpy as np

def create_mlp(num_labels):

    model = Sequential()
    model.add(Dense(256,input_shape = (40,)))
    model.add(Activation('relu'))
    model.add(Dropout(0.5))

    model.add(Dense(256,input_shape = (40,)))
    model.add(Activation('relu'))
    model.add(Dropout(0.5))

    model.add(Dense(num_labels))
    model.add(Activation('softmax'))
    return model

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

def train(model,X_train, X_test, y_train, y_test,model_file):    
    
    # compile the model 
    model.compile(loss = 'categorical_crossentropy',metrics=['accuracy'],optimizer='adam')

    print(model.summary())

    print("training for 100 epochs with batch size 32")
   
    model.fit(X_train,y_train,batch_size= 1024, epochs = 100, validation_data=(X_test,y_test))
    
    # save model to disk
    print("Saving model to disk")
    model.save(model_file)

def compute(X_test,y_test,model_file):

    # load model from disk
    loaded_model = load_model(model_file)
    score = loaded_model.evaluate(X_test,y_test)
    return score[0],score[1]*100

def predict(filenames,le,model_file, kind):

    model = load_model(model_file)
    file_count = float(len(filenames))
    acc = 0.0
    for filename in filenames:
        print(filename)
        prediction_feature = extract_features.get_features(filename)
        #if model_file == "trained_mlp.h5":
        #    prediction_feature = np.array([prediction_feature])
        #elif model_file == "trained_cnn.h5":    
        prediction_feature = np.expand_dims(np.array([prediction_feature]),axis=2)

        predicted_vector = model.predict_classes(prediction_feature)
        print(predicted_vector)
        predicted_class = le.inverse_transform(predicted_vector)
        ##print("Predicted class",predicted_class[0])
        predicted_proba_vector = model.predict_proba([prediction_feature])

        predicted_proba = predicted_proba_vector[0]
        ##print(kind)
        if kind == 'no':
            if predicted_proba[0] > 0.5:
                acc += 1
            #else:
            #    print(filename)
        elif kind == 'yes':
            if predicted_proba[1] > 0.5:
                acc += 1
            else:
                print(filename)
                #print(predicted_proba)
        #for i in range(len(predicted_proba)): 
            
            #category = le.inverse_transform(np.array([i]))
            #print(category[0], ' == ', kind)
            #if category[0] == 'no' and predicted_proba[i] < 0.5:
            #    acc += 1
            #    print(filename)
            #print(category[0], "\t\t : ", format(predicted_proba[i], '.32f') )
    if acc == 0.0:
        print('kind: ', kind, ' file acc: 0.0', ' acc count: ', acc, ' file count: ', file_count)
    else:
        print('kind: ', kind, ' file acc: ', acc / file_count, ' acc count: ', acc, ' file count: ', file_count)

def inference(filenames, lr):
    model = load_model(model_file)
    prediction_feature = extract_features.get_features(filename)
    prediction_feature = np.expand_dims(np.array([prediction_feature]),axis=2)
    predicted_vector = model.predict_classes(prediction_feature)

