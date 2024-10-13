import socket
import pickle
from product import Product
import time
with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
    s.bind((socket.gethostname(),4571))
    py_dict = {'a':1,'b':2}
    pickled_dict = pickle.dumps(py_dict)
    custom_obj = Product('P024','Torch',13)
    pickled_obj = pickle.dumps(custom_obj)

    #a list of objects example
    custom_list = [Product('P025','Waterbottle',5),
                   Product('P026','Keyboard',20),
                   Product('P027','Mouse',15),
                   Product('P028','USBCable',2),]


    print('Serialized dictionary type:',type(pickled_dict))    
    print('Serialized object type:',type(pickled_obj))    
    s.listen(5)
    print('Server is up. Listening for connections...\n')
    client,address = s.accept()
    print('Connection to',address,'established\n')
    print('Client object:',client,'\n')
    
    # client.send(bytes(str(py_dict),'utf-8'))
    # client.send(bytes(str(custom_obj),'utf-8'))
    
    client.send(pickled_dict)
    client.send(pickled_obj)
  
  #extracting all products from custom_list
    for product in custom_list:
        time.sleep(2)
        pickled_product = pickle.dumps(product)
        client.send(pickled_product)
        print('Sent the product:',product.pid)
        