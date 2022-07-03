from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
import numpy as np
import cv2
import pickle
import os



out_classes = ['QR','empty','horizontal','lef3','left2','lef1','center','right1','right2','right3']
def preprocessing (img, dest_size = (20,20), dest_rang: int = 16):
    '''
    this function resize the image then makes pixels in a certain range
    it takes about 0.00035 s
    the input image should be in gray scale
    '''
    out = (cv2.resize(img, dest_size) * (dest_rang/255)).astype('uint8')
    return out.reshape( out.shape[0] * out.shape[1] )

def Train_test_split(X, y, test_size = 0.2, random_state = 0):
    return train_test_split(X, y, test_size, random_state)


def genrat_model (X_data,y_data , dest = "./line_classifier"):
    if not os.path.exists(dest):
        os.mkdir(os.path.join(dest))
        
    model = MLPClassifier(hidden_layer_sizes=(200,200,200,200),activation="relu" ,random_state=1, max_iter=2000)
    model.fit(X_data,y_data)
    pickle.dump(model, open(f'{dest}/model', 'wb'))
    return model.score(X_data, y_data)
    
def load_model(source):
    return pickle.load(open(source, 'rb'))

def conv_str2list(string):
    global out_classes
    out= [0,0,0,0,0,0,0,0,0,0]
    out[out_classes.index(string)] = 1
    return out

def conv_list2str(Input : np.ndarray):
    global out_classes
    indexs = np.where(Input == np.amax(Input))
    return out_classes[indexs[0][0]]

def indexing(source,perfx ="", sufx=""):
    data_names = [ f'{source}/{i}' for i in os.listdir(source)]
    for index in range(len(data_names)):
        os.rename(data_names[index], f"{source}/{perfx}{index}{sufx}.jpg")
    return True


current_x = -1 # global var to be used in mani functions
def click_event(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        cv2.destroyAllWindows()
        global current_x
        
        current_x = x
        

def data_generator(source, dest):
    '''
    this func generat data for line detector neural network
    '''
    X_data = []
    y_data = []
    source_data = []
    
    if not os.path.exists(dest):
        os.mkdir(os.path.join(dest))
    
    source_data = [ f'{source}/{i}' for i in os.listdir(source)]
    
    # shuffel data
    np.random.shuffle(source_data)
    source_data  = np.asarray(source_data)
    
    # get data and Target
    i = 0
    while (i < len(source_data)):
        global current_x
        current_x = -1
        current_target = None
        
        img = cv2.imread(source_data[i],0)
        cv2.imshow("source image", img)
        cv2.setMouseCallback("source image" , click_event)
        k = cv2.waitKey(0)
        cv2.destroyAllWindows()
        
        if k == ord('q'):
            current_target = "QR"
        elif k == ord('e'):
            current_target = "empty"
        elif k == ord('h'):
            current_target = "horizontal"
        elif k == -1 and current_x != -1:
            line_classes = ['lef3','left2','lef1','center','right1','right2','right3']
            index = round((current_x*6)/ img.shape[1])
            current_target = line_classes[index]
        else :
            continue
        
        img = preprocessing(img)
        X_data.append(img)
        y_data.append(current_target)
        print(current_target)
        i += 1
        
    # saving data
    np.save(f'{dest}/source_data.npy', source_data)
    np.save(f'{dest}/X_data.npy', X_data)
    np.save(f'{dest}/y_data.npy', y_data)
        
    return True

def data_generator_labled(source, dest , lable):
    '''
    this func generat data for line detector neural network with specifc lable
    '''
    X_data = []
    y_data = []
    source_data = []
    
    if not os.path.exists(dest):
        os.mkdir(os.path.join(dest))
    
    source_data = [ f'{source}/{i}' for i in os.listdir(source)]
    
    # shuffel data
    randomize = np.arange(len(source_data))
    np.random.shuffle(source_data)
    source_data  = np.asarray(source_data)
    
    for img_path in source_data:
        img = cv2.imread(img_path,0)
        img = preprocessing(img)
        X_data.append(img)
        y_data.append(lable)
        print(img_path)
    
    # saving data
    np.save(f'{dest}/source_data.npy', source_data)
    np.save(f'{dest}/X_data.npy', X_data)
    np.save(f'{dest}/y_data.npy', y_data)

def data_resize_and_indexing(source,dest, FX ,FY):
    if not os.path.exists(dest):
        os.mkdir(os.path.join(dest))
    
    data_names = [ f'{source}/{i}' for i in os.listdir(source)]
    
    for i in range(len(data_names)):
        img = cv2.imread(data_names[i])
        prev = img.shape
        img = cv2.resize(img, None ,fx = FX ,fy = FY)
        aft = img.shape
        new = f"{dest}/{i}.jpg"
        cv2.imwrite(new, img)
        
        print(data_names[i] ," - ",prev,">>>",new," - ",aft,"\n")
        
    return True

def fipping (source ,dest , horizontal = True, vertical = True , Indexing = True):
    if not os.path.exists(dest):
        os.mkdir(os.path.join(dest))
    
    data_names = [ f'{source}/{i}' for i in os.listdir(source)]
    for i in range(len(data_names)):
        img = cv2.imread(data_names[i])
        cv2.imwrite(f"{dest}/{i}.jpg", img)
        if horizontal:
            img_horiz = cv2.flip(img, 1)
            cv2.imwrite(f"{dest}/H{i}.jpg", img)
        if vertical:
            img_horiz = cv2.flip(img, 0)
            cv2.imwrite(f"{dest}/V{i}.jpg", img)
        
        print(data_names[i])
        
    if Indexing:
        indexing(dest,"f") # to avoid riblications in names
        indexing(dest)
    
    return True