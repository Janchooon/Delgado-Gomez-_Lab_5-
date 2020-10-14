from Cryptodome.Cipher import AES
import socket


Entrada = open('mensajeentrada.txt','r') #Txt que contiene el texto plano
TextoPlano = Entrada.readlines()[0]
TextoPlano = TextoPlano.encode(encoding = "ascii", errors = "ignore") #Extrae el texto plano del archivo
Entrada.close()

#Encriptado AES
Llave = b"Sixteen byte key"
AES_Cifrado = AES.new(Llave, AES.MODE_EAX)

nonce = AES_Cifrado.nonce
Encriptado_AES, tag = AES_Cifrado.encrypt_and_digest(TextoPlano)


Valor_P = 173
Valor_Q = 50
Valor_A = int(input("Ingrese valor A secreto: "))

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
        AES_Cifrado = AES.new(Llave, AES.MODE_EAX, nonce=nonce)
        Desencriptado_AES = AES_Cifrado.decrypt(Encriptado_AES)
        Enviar = str(Desencriptado_AES)
        try:
            AES_Cifrado.verify(tag)
            print("The message is authentic:", Desencriptado_AES)
            Recibido.write("Decrypted: %r" %Desencriptado_AES)
            Recibido.close()
        except ValueError:
            print("Key incorrect or message corrupted")
            Recibido.write("Encrypted: %r" %Encriptado_AES)
            Recibido.close()
        Conexion.send(Enviar.encode(encoding = "ascii", errors = "ignore"))
    else:
        print ("Encrypted:", Encriptado_AES)
        Recibido.write("Encrypted: %r" %Encriptado_AES)
        Recibido.close()
