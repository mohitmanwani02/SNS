import socket
import threading
import sys
import ast
import numpy as np
class Peer:
    def __init__(self,socket,ip,port):
        self.socket=socket
        self.ip=ip
        self.port=port
        self.isloggedin=False
        self.user_name=''
        self.password=''
        self.rollno=None
        

connected_peers={}

class Server:
    key='100111001001'
    IP = socket.gethostbyname(socket.gethostname())
    def __init__(self):
        self.server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        self.conn_list = []

    def xor(self,a, b): 
   
        result = [] 

        for i in range(1, len(b)): 
            if a[i] == b[i]: 
                result.append('0') 
            else: 
                result.append('1') 
    
        return ''.join(result) 
    
   
    def mod2div(self,divident, divisor): 
    
        pick = len(divisor) 
    
        tmp = divident[0 : pick] 
    
        while pick < len(divident): 
    
            if tmp[0] == '1': 
    
                tmp = self.xor(divisor, tmp) + divident[pick] 
    
            else:  

                tmp = self.xor('0'*pick, tmp) + divident[pick] 

            pick += 1
    
        if tmp[0] == '1': 
            tmp = self.xor(divisor, tmp) 
        else: 
            tmp = self.xor('0'*pick, tmp) 
    
        checkword = tmp 
        return checkword 


    def decodeData(self,data, key): 
   
        l_key = len(key) 
    
        # Appends n-1 zeroes at end of data 
        appended_data = data + '0'*(l_key-1) 
        remainder = self.mod2div(appended_data, key) 
    
        return int(remainder)

    def handle_connection(self,client_socket,client_address,peer_details):
        
        while True:
            
            data=client_socket.recv(4096)
            if not data:
                break
            data=data.decode()
            if data.lower()=='disconnect':
                print("\n[+]############    USER ",connected_peers[client_address[1]])
                print("{}:{} disconnected.....".format(client_address[0],client_address[1]))
                connected_peers.pop(client_address[1])
                client_socket.close()
                
                break
            print("\n[+]############      USER ",connected_peers[client_address[1]])
            tokens=data.split("`")
            data=tokens[0]
            print("\n[+]The Recieved Transformed Matrix is\n",data)
            data1=str((data))
            #print("string",data1)
            
            
            lis=ast.literal_eval(data1)
            #print("As litera",lis)
            rem=self.decodeData(tokens[1],self.key)
            print("\n[+]The Attached CRC code is\n",tokens[1])
            print("\n[+]The remainder of CRC check is ",rem)
            if(rem==0):
                print("CRC check successful!!")
            else:
                print("CRC check unsuccessful!!\nResend the message")
                continue
                


            self.dec(lis)

            



    def dec(self,matrix):
        S=[[-3,-3,-4],[0,1,1],[4,3,4]]
        s1=np.linalg.inv(S)
        print("\nInversely Transformed Matrix is\n", (np.matmul(s1,matrix)).astype(int))
        d=(np.matmul(s1,matrix)).astype(int)
        text=""
        col=len(matrix[0])
        for i in range(col):
            for j in range(3):
                if d[j][i]==27:
                    text=text+" "
                else:
                    text=text+chr(d[j][i]+ord('A')-1)

        print("\nMessage Recieved\n",text)

    def run(self,PORT=18000):
        self.server_socket.bind((self.IP,PORT))
        self.server_socket.listen(20)
        print("Listening at {}".format(self.server_socket.getsockname()))
        i=1
        while True:
            client_socket,client_address = self.server_socket.accept()
            print(client_address[0],client_address[1],' connected')
            connected_peers[client_address[1]]=i
            i+=1
            serveratpeerip, seerveratpeerport=client_socket.recv(4096).decode().split(':')
            print(serveratpeerip,seerveratpeerport)
            # self.conn_list.append(client_socket)
            client_details=Peer(client_socket,serveratpeerip,seerveratpeerport)
            # peers.append(client_details)
            th=threading.Thread(target=self.handle_connection,args=(client_socket,client_address,client_details))
            th.daemon = True
            th.start()

if __name__ == "__main__":
    server = Server()
    server.run()
        