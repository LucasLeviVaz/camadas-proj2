#####################################################
# Camada Física da Computação
#Carareto
#11/08/2022
#Aplicação
####################################################

from enlace import *
import time
import numpy as np
import sys

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

        head = [1, 1, 1, 1, 1, 0]
        eop_certo = b'\xAA'*4

        imageW = './imgs/recebidaCopia.png'

        # 0 tipo da mensagem, 1 e 2 nome do arquivo, 3 tamanho do payload, 4 quantos pacotes, 5 em qual pacote estou, resto, b'\x00'

        i=0
        # Loop para cada um dos pacotes
        while head[5] < head[4]:

            head = com1.getData(10)[0]
            n_bytes_enviado = head[3]

            n_bytes_recebido = com1.rx.getBufferLen() -4
            payload = com1.getData(n_bytes_enviado)[0]
            eop = com1.getData(4)[0]

            qual_pacote = head[5]
            qual_pacote_bytes = qual_pacote.to_bytes(1, byteorder='big')

            # Tipo 6 (erros)
            if n_bytes_enviado != n_bytes_recebido or eop != eop_certo:
                head_s = b'\x06' + qual_pacote_bytes + b'\x00'*8 + eop_certo 
                com1.sendData(head_s)

                #colocar no header a partir de q pacote enviar dnv


            # Tipo 1
            elif head[0] == 1:
                head_s = b'\x02' + qual_pacote_bytes + b'\x00'*8 + eop_certo 
                com1.sendData(head_s)
                img_bytes = payload

            # Tipo 3
            elif head[0] == 3:
                head_s = b'\x04' + qual_pacote_bytes + b'\x00'*8 + eop_certo 
                com1.sendData(head_s)
               
                print(i)
                print(head[5])
                print(head[4])
                img_bytes += payload



            if head[5] == head[4]:
                i +=1
            else:
                i = head[5]

        
        print(img_bytes)
        imagem = open(imageW, 'wb')
        imagem = imagem.write(img_bytes)


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
