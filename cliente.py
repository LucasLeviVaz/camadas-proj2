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

        #bit de sacrificio
        com1.enable()
        time.sleep(.2)
        com1.sendData(b'00')
        time.sleep(1)

        #Se chegamos até aqui, a comunicação foi aberta com sucesso. Faça um print para informar.
        print("Abriu a comunicação")
        
        lista_comandos = [b'\x00\x00\x00\x00', b'\x00\x00\xFF\x00', b'\xFF\x00\x00', b'\x00\xFF\x00', b'\x00\x00\xFF', b'\x00\xFF', b'\xFF\x00', b'\x00', b'\xFF']
        lista_envio = []
        
        sorteio = random.randint(10, 30)
        print(sorteio)

        i=0
        while i < sorteio:
            j = random.randint(0, len(lista_comandos)-1)
            lista_envio.append(lista_comandos[j])
            i+=1
        
                  
        #aqui você deverá gerar os dados a serem transmitidos. 
        #seus dados a serem transmitidos são um array bytes a serem transmitidos. Gere esta lista com o 
        #nome de txBuffer. Esla sempre irá armazenar os dados a serem enviados.
        
        #txBuffer = imagem em bytes!
        txBuffer = lista_envio
        print("meu array de bytes tem tamanho {}" .format(len(txBuffer)))
        #faça aqui uma conferência do tamanho do seu txBuffer, ou seja, quantos bytes serão enviados.
       

        #finalmente vamos transmitir os todos. Para isso usamos a funçao sendData que é um método da camada enlace.
        #faça um print para avisar que a transmissão vai começar.
        print('a transmissão vai começar')
        #tente entender como o método send funciona!
        #Cuidado! Apenas trasmita arrays de bytes!
               
        for comando in txBuffer:
            com1.sendData(np.asarray(comando))  #as array apenas como boa pratica para casos de ter uma outra forma de dados
            time.sleep(0.5)
            txSize = com1.tx.getStatus()
            print('enviou = {}' .format(txSize))

        com1.sendData(np.asarray(b'\xCC'))  #as array apenas como boa pratica para casos de ter uma outra forma de dados
          
        # A camada enlace possui uma camada inferior, TX possui um método para conhecermos o status da transmissão
        # O método não deve estar funcionando quando usado como abaixo. deve estar retornando zero. Tente entender como esse método funciona e faça-o funcionar.
        
        #Agora vamos iniciar a recepção dos dados. Se algo chegou ao RX, deve estar automaticamente guardado
        #Observe o que faz a rotina dentro do thread RX
        #print um aviso de que a recepção vai começar.
        
        #Será que todos os bytes enviados estão realmente guardadas? Será que conseguimos verificar?
        #Veja o que faz a funcao do enlaceRX  getBufferLen
      
        #acesso aos bytes recebidos

        print('antes')
        txLen = len(txBuffer)
        if rxBuffer not in locals:
            rxBuffer, nRx = com1.getData(1)
        print('depois')
        print("recebeu {} bytes" .format(len(rxBuffer)))
        
        for i in range(len(rxBuffer)):
            print("recebeu {}" .format(rxBuffer[i]))
            
        time.sleep(5)
        print(rxBuffer)
        print(sorteio)
        if int.from_bytes(rxBuffer, "big") == sorteio:
            print('RECEBA')
        else:
            print('time out')

        com1.disable()
        
        

        '''# Carega imagem
        print ("Carregando imagem para transmissão :")
        print (" - {}".format(ImageR))
        print("---------------------------------------------")
        txBuffer = open(ImageR, 'rb').read()

        #Escreve arquivo cópia
        print ("Salvando dados no arquivo :")
        print (" - {}".format (ImageW))
        f = open (ImageW, 'wb')
        f.write(rxBuffer)
        # Fecha arquivo de imagem
        f.close()
            
    
        # Encerra comunicação
        print("-------------------------")
        print("Comunicação encerrada")
        print("-------------------------")
        com1.disable()'''
        
    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com1.disable()
        

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()
