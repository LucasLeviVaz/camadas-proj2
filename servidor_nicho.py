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

        print("Iniciou o main")

        com1 = enlace(serialName)
        
        com1.enable()
      
        print("Abriu a comunicação")

        print("esperando 1 byte de sacrifício")         
        rxBuffer, nRx = com1.getData(1) 
        com1.rx.clearBuffer() 
        time.sleep(.1)

        time.sleep(2)

        head = [1, 1, 1, 1]
        eop_certo = b'\xAA'*4

        # 0 tipo da mensagem, 1 e 2 nome do arquivo, 3 tamanho do payload, 4 quantos pacotes, 5 em qual pacote estou, resto, b'\x00'

        i=0
        # Loop para cada um dos pacotes
        while i < head[4]:
            head = com1.getData(10)[0]
            n_bytes_enviado = head[3]

            n_bytes_recebido = com1.rx.getBufferLen()
            payload = com1.getData(n_bytes_enviado)[0]
            eop = com1.getData(4)[0]

            # Tipo 6 (erros)
            if n_bytes_enviado != n_bytes_recebido or eop != eop_certo:
                tipo6 = b'\x06' + b'\x00'*9
                head_s = tipo6 + eop_certo
                com1.sendData(head_s)

                #colocar no header a partir de q pacote enviar dnv


            # Tipo 1
            elif head[0] == 1:
                tipo2 = b'\x02' + b'\x00'*9
                head_s = tipo2 + eop_certo
                com1.sendData(head_s)




            i = head[5]


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
