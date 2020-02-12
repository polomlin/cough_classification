import numpy as np
from sklearn.preprocessing import LabelEncoder
from keras.utils import to_categorical
from sklearn.model_selection import train_test_split
import extract_features
import nn
import sys
import glob

def get_numpy_array(features_df):

    X = np.array(features_df.feature.tolist())
    y = np.array(features_df.class_label.tolist())
    # encode classification labels
    le = LabelEncoder()
    # one hot encoded labels
    yy = to_categorical(le.fit_transform(y))
    return X,yy,le

def get_train_test(X,y):
    
    X_train, X_test, y_train, y_test = train_test_split(X,y,test_size = 0.2, random_state = 42)
    return  X_train, X_test, y_train, y_test

if __name__ == "__main__":
    
    # extract features
    print("Extracting features..")
    features_df = extract_features.extract_features()

    if sys.argv[1] == "cnn":

        #convert into numpy array
        X, y, le = get_numpy_array(features_df)

        # split into training and testing data
        X_train, X_test, y_train, y_test = get_train_test(X,y)
        num_labels = y.shape[1]
        
        X_train = np.expand_dims(X_train, axis=2)
        X_test = np.expand_dims(X_test, axis=2)
        
        # create model architecture
        model = nn.create_cnn(num_labels)

        # train model
        print("Training..")
        nn.train(model,X_train, X_test, y_train, y_test,"trained_cnn.h5")

        # compute test loss and accuracy
        test_loss, test_accuracy = nn.compute(X_test,y_test,"trained_cnn.h5")

        print('num_labels: ', num_labels)
        print('le: ', le)
        print("Test loss",test_loss)
        print("Test accuracy",test_accuracy)

        # predicting using trained model with any test file in dataset
        allpaths = glob.glob('/home/sam/Music/cough/asr/test/yes/*.wav')
        nn.predict(allpaths,le,"trained_cnn.h5",'yes')

        allpaths = glob.glob('/home/sam/Music/cough/asr/test/no/*.wav')
        nn.predict(allpaths,le,"trained_cnn.h5", 'no')
    elif sys.argv[1] == "predict":
        X, y, le = get_numpy_array(features_df)

        #allpaths = glob.glob('/home/sam/Music/cough/asr/test/yes/*filter_*.wav')
        #nn.predict(allpaths,le,"trained_cnn.h5",'yes')

        #allpaths = glob.glob('/home/sam/Music/cough/asr/test/no/*.wav')
        #nn.predict(allpaths,le,"trained_cnn.h5", 'no')

