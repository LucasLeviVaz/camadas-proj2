#####################################################
# Camada Física da Computação
#Carareto
#11/08/2022
#Aplicação
####################################################

from enlace import *
import time
import numpy as np

# voce deverá descomentar e configurar a porta com através da qual ira fazer comunicaçao
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports
# se estiver usando windows, o gerenciador de dispositivos informa a porta

serialName = "COM5"                  

def main():
    try:
        protocol = b'\x14'

        print("Iniciou o main")

        com1 = enlace(serialName)
        
        com1.enable()
      
        print("Abriu a comunicação")

        print("esperando 1 byte de sacrifício")         
        rxBuffer, nRx = com1.getData(1) 
        com1.rx.clearBuffer() 
        time.sleep(.1)

        time.sleep(3)

        Buffer = com1.rx.getAllBuffer(0)
        print(f'Esse é o nosso buffer: {Buffer}')

        lista_comandos = Buffer.split(protocol)
        print(f'Essa é a lista de comandos recebida: {lista_comandos}')

        num_comandos = len(lista_comandos) - 1
        #num_comandos = 1
        print(f'Esse é a quantidade de comandos recebidas: {num_comandos}')

        bytes = num_comandos.to_bytes(1, 'big') 
        print(f'Esse é o dado que será enviado para o client: {bytes}')

        com1.sendData(bytes)

        # Encerra comunicação
        print("-------------------------")
        print("Comunicação encerrada")
        print("-------------------------")
        com1.disable()
        
    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com1.disable()
        

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()
