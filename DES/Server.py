# -*- coding: utf-8 -*-
"""
Created on Mon Oct 12 17:06:03 2020

@author: janso
"""

import socket
import pyDes

Entrada = open('mensajeentrada.txt','r') #Txt que contiene el texto plano
TextoPlano = Entrada.readlines()[0] #Extrae el texto plano del archivo
Entrada.close()

#Encriptado DES
DES = pyDes.des("DESCRYPT", pyDes.CBC, "\0\0\0\0\0\0\0\0", pad=None, padmode=pyDes.PAD_PKCS5)
Encriptado_DES = DES.encrypt(TextoPlano)

Valor_P = 173
Valor_Q = 50
Valor_A = 13

Valor_Ax = str((Valor_Q^Valor_A)%Valor_P) 

Host = "LocalHost"
Puerto = 8000

Server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
Server.bind((Host, Puerto))
Server.listen(1)
print("Servidor en espera")

Conexion, Addr = Server.accept()

for i in range(1):
    Conexion.send(Valor_Ax.encode(encoding="ascii", errors="ignore"))
    Bx = Conexion.recv(1024)
    Bx = int(Bx.decode(encoding = "ascii", errors = "ignore"))
    LlaveCalculadaA = (Bx^(Valor_A)) % Valor_P
    LlaveCalculadaB = Conexion.recv(1024)
    LlaveCalculadaB = int(LlaveCalculadaB.decode(encoding = "ascii", errors = "ignore"))
    
    Recibido = open('mensajerecibido.txt','w')
    
    if LlaveCalculadaA == LlaveCalculadaB:
        Desencriptado_DES = DES.decrypt(Encriptado_DES)
        Enviar = str(Desencriptado_DES)
        Conexion.send(Enviar.encode(encoding = "ascii", errors = "ignore"))
        print ("Decrypted ", Desencriptado_DES)
        Recibido.write("Decrypted: %r" %Desencriptado_DES)
    else:
        print ("Encrypted:", Encriptado_DES)
        Recibido.write("Encrypted: %r" %Encriptado_DES)
