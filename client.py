import socket
import sys
import threading
import numpy as np




class Client:
    def __init__(self,server_ip,server_port, sip,sport):
        self.client_socket =socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.client_socket.connect((server_ip,server_port))
        self.sip=sip
        self.sport=sport
        self.server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.text=''
        self.user_name=''
        self.filepath=''
        self.rollnumber=""


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
    
    def encodeData(self,data, key): 
    
        l_key = len(key) 
    
        appended_data = data + '0'*(l_key-1) 
        remainder = self.mod2div(appended_data, key) 
    
        codeword = data + remainder 
        return codeword 

    def transform(self,message):
        m_message=[]
        S_matrix=[[-3,-3,-4],[0,1,1],[4,3,4]]
        for i in range(len(message)):
            if message[i]==" ":
                m_message.append(27)
            else:
                m_message.append(ord(message[i].upper())-ord('A')+1)


        row=3
        #print(len(message))
        if len(message)%3==0:
            col=int(len(message)/3)

            s=[]
            for i in range(row):
                l=[]
                for j in range(col):
                    l.append(m_message[j*3+i])
                s.append(l)
                #print(s)
            print("Initial Matrix is :\n",s)
            #m_message=zip(*[iter(m_message)]*3)

        else :
            col=int(len(message)/3)+1

            for i in range((3*col)-len(message)%3):
                m_message.append(27) 
            s=[]
            for i in range(row):
                l=[]
                for j in range(col):
                    l.append(m_message[j*3+i])
                s.append(l)
            print("\nInitial Matrix is :\n",s)
            #m_message=[m_message[col*i : col*(i+1)] for i in range(row)]

        #print(m_message)


        print("\nThe Transformed Matrix is\n",np.matmul(S_matrix,s))

        r=np.matmul(S_matrix,s)
        return (r)


        #m_message=""
        #for i in range(len(message)):
           # m_message[i]=ord(message[i])-ord('A')+1



    def senddata(self):
        self.client_socket.send((self.sip+':'+str(self.sport)).encode())
        while True:
            print("\nEnter Command\n")
            inp=input()
            #tokens=inp.split()
            if inp[0:4]=='send':
                s_string=inp[5:]
                t_string=self.transform(s_string)
                #t_string=np.asarray(t_string)
                f_string=t_string.tolist()
                #print("fstring",f_string)
                f_string=str(f_string)
                #print("new2",f_string)
                binar = (''.join(format(ord(x), 'b') for x in s_string)) 
                
                codeword=self.encodeData(binar,'100111001001')

                print("\n[+]The CRC code is\n",codeword)
                print("\n[+]Appending CRC code\n")
                self.client_socket.send((f_string+"`"+codeword).encode())
                print("[+]Message Delivered!!")
                #self.filepath=tokens[2]
            elif inp[0:10].lower()=='disconnect':
                self.client_socket.send((inp[0:10].encode()))
                self.client_socket.close()
                break
         


    def print_cmds(self):
            cmds = ["[+] WELCOME!!\n[+]To Send Message type  ------>  send < message >\n[+]To Disconnect type  -------->  disconnect"]

            print("************** *******")
            for cmd in cmds:
                print(cmd)

            print("***********************\n")

if __name__ == "__main__":
    client = Client(sys.argv[1],int(sys.argv[2]),sys.argv[3],int(sys.argv[4]))
    client.print_cmds()
    client.senddata()
   # client.run()
