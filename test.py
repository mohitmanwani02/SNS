import itertools
import numpy as np
S_matrix=[[-3,-3,-4],[0,1,1],[4,3,4]]
message ="PENGUINS ARE ONE TO ONE"
m_message=[]


for i in range(len(message)):
    if message[i]==" ":
        m_message.append(27)
    else:
        m_message.append(ord(message[i].upper())-ord('A')+1)


row=3
if len(message)%3==0:
    col=int(len(message)/3)

    s=[]
    for i in range(row):
        l=[]
        for j in range(col):
            l.append(m_message[j*3+i])
        s.append(l)
        print(s)
    #m_message=zip(*[iter(m_message)]*3)

else :
    col=int(len(message)/3)+1

    for i in range(len(message)%3):
        m_message.append(27) 
    s=[]
    for i in range(row):
        l=[]
        for j in range(col):
            l.append(m_message[j*3+i])
        s.append(l)
        print(s)
    #m_message=[m_message[col*i : col*(i+1)] for i in range(row)]

#print(m_message)


print("The Transformed Matrix is\n",np.matmul(S_matrix,s))

r=np.matmul(S_matrix,s)



def dec(matrix):
    S=[[-3,-3,-4],[0,1,1],[4,3,4]]
    s1=np.linalg.inv(S)
    print("Decrypted message is", (np.matmul(s1,matrix)).astype(int))
    d=(np.matmul(s1,matrix)).astype(int)
    text=""
    for i in range(col):
        for j in range(3):
            if d[j][i]==27:
                text=text+" "
            else:
                text=text+chr(d[j][i]+ord('A')-1)

    print(text)



dec(r)

