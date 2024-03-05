#####################################################
# Camada Física da Computação
#Carareto
#11/08/2022
#Aplicação
####################################################


#esta é a camada superior, de aplicação do seu software de comunicação serial UART.
#para acompanhar a execução e identificar erros, construa prints ao longo do código! 


from enlace import *
import time
import numpy as np
import random

# voce deverá descomentar e configurar a porta com através da qual ira fazer comunicaçao
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports
# se estiver usando windows, o gerenciador de dispositivos informa a porta

#use uma das 3 opcoes para atribuir à variável a porta usada
#serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
#serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)
serialName = "COM5"                  # Windows(variacao de)


def main():
    try:
        print("Iniciou o main")
        #declaramos um objeto do tipo enlace com o nome "com". Essa é a camada inferior à aplicação. Observe que um parametro
        #para declarar esse objeto é o nome da porta.
        com1 = enlace(serialName)

        print("Abriu a comunicação")
        
        com1.enable()
        print("esperando 1 byte de sacrifício")
        rxBuffer, nRx = com1.getData(1)
        com1.rx.clearBuffer()
        time.sleep(3)
        # Ativa comunicacao. Inicia os threads e a comunicação seiral 
        #Se chegamos até aqui, a comunicação foi aberta com sucesso. Faça um print para informar.
          
        # A camada enlace possui uma camada inferior, TX possui um método para conhecermos o status da transmissão
        # O método não deve estar funcionando quando usado como abaixo. deve estar retornando zero. Tente entender como esse método funciona e faça-o funcionar.
        #txSize = com1.tx.getStatus()
        
        #Agora vamos iniciar a recepção dos dados. Se algo chegou ao RX, deve estar automaticamente guardado
        #Observe o que faz a rotina dentro do thread RX
        #print um aviso de que a recepção vai começar.
        
        #Será que todos os bytes enviados estão realmente guardadas? Será que conseguimos verificar?
        #Veja o que faz a funcao do enlaceRX  getBufferLen
        # recebeu = False
        # #acesso aos bytes recebidos

        #recebe 1 por 1

        recebido = com1.rx.getAllBuffer(1)
        recebido = recebido.decode('utf-8')
        recebido.split("\x14")
        print(recebido)
        j = 0
        condicao = True
        while condicao:
            if com1.rx.getBufferLen() > 0:
                rxBuffer = com1.rx.getAllBuffer(1)
                j += 1
                if rxBuffer == b'\xCC':
                    condicao = False
                else:
                    print("recebeu {}" .format(rxBuffer))
        
        j-=1
        print("recebeu {} bytes" .format(j))
        j2 = (j).to_bytes(1, byteorder='big')
        com1.sendData(np.asarray(j2))
        time.sleep(0.5)
        txsize = com1.tx.getStatus()
        print("enviou {}" .format(txsize))
        
    
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
