import socket
from product import Product
import pickle
with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
    s.connect((socket.gethostname(),4571))
    while True:
        msg = s.recv(1024)
        if not msg:
            print('\nNOTICE: No messages from the server. Closing the connection...')
            break
        # print('Message from server:',msg.decode('utf-8'))
        # print('Type of message received',type(msg))
        
        print('\nType of message received',type(msg))
        print('Message data:',msg)
        try:
            unpickled_msg = pickle.loads(msg)
            
            print('Type of deserialized message received',type(unpickled_msg))
            print('Deserialized data',unpickled_msg)
            #product information for singular product
            try:
                print('\nProduct ID:',unpickled_msg.pid)
                print('Product Name:',unpickled_msg.pname)
                print('Product Price:',unpickled_msg.pid)
            except:
                print('\nNo product information available for object')
        except:
            print('Received incomplete or invalid message for deserialization.')