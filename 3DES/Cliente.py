# -*- coding: utf-8 -*-
"""
Created on Mon Oct 12 17:10:48 2020

@author: janso
"""

import socket
import pyDes

DES = pyDes.des("DESCRYPT", pyDes.CBC, "\0\0\0\0\0\0\0\0", pad=None, padmode=pyDes.PAD_PKCS5)

Valor_P = 173
Valor_Q = 50
Valor_B = int(input("Ingrese valor B secreto: "))
B = Valor_B

Valor_Bx = str((Valor_Q^Valor_B)%Valor_P)

Host = "LocalHost"
Puerto = 8000

Mi_Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
Mi_Socket.connect((Host, Puerto))

for i in range(1):
    Mi_Socket.send(Valor_Bx.encode(encoding="ascii", errors="ignore"))
    Ax = Mi_Socket.recv(1024)
    Ax = int(Ax.decode(encoding = "ascii", errors = "ignore"))
    LlaveCalculadaB = str((Ax^(Valor_B)) % Valor_P)
    Mi_Socket.send(LlaveCalculadaB.encode(encoding="ascii", errors="ignore"))

    Recibir = Mi_Socket.recv(1024)
    Recibir = Recibir.decode(encoding = "ascii", errors = "ignore")
    
    print(Recibir)