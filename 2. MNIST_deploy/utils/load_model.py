import pickle


def load_model():
    '''

        Function to load svc model.
    
    '''
    with open('model/svm_mnist.pkl', 'rb') as f:
        svc = pickle.load(f)
    return svc