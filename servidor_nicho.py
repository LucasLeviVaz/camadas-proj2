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
      
        print("Abriu a comunicação")

        com1.enable()
        print("esperando 1 byte de sacrifício")
        rxBuffer, nRx = com1.getData(1)
        com1.rx.clearBuffer()

        time.sleep(2)

        eop_certo = b'\xAA'*4
        n_bytes_total = 0
        ult_payload = 0
        j=1

        imageW = './imgs/recebidaCopia.png'

        # 0 tipo da mensagem, 1 e 2 nome do arquivo, 3 tamanho do payload, 4 quantos pacotes, 5 em qual pacote estou, resto, b'\x00'
        while j <= 2:
            head = [1, 1, 1, 1, 1, 0]

            # Loop para cada um dos pacotes
            while head[5] < (head[4]):


                inicio = time.time() 
                inicio_r = time.time()

                # Timout
                while (time.time() - inicio) < 10.5:

                    if (time.time() - inicio) > 10:
                        head_s = b'\x05' + b'\x00' * 9 + eop_certo
                        com1.sendData(head_s)
                        print("Tempo esgotado...")
                        com1.disable()
                        sys.exit()

                    elif (time.time() - inicio_r) > 2:
                        com1.sendData(head_s)
                        inicio_r = time.time()
                        print(time.time()-inicio)


                    # Ping-pong
                    elif com1.rx.getBufferLen() > 1:
                        head = com1.getData(10)[0]
                        n_bytes_enviado = head[3]

                        n_bytes_recebido = com1.rx.getBufferLen() -4
                        payload = com1.getData(n_bytes_enviado)[0]
                        eop = com1.getData(4)[0]

                        inicio = -100


                        if head[0] == 5:
                            print("Tempo esgotado...")
                            com1.disable()
                            sys.exit()


                        # Tipo 1
                        if head[0] == 1:
                            qual_pacote = head[5]
                            qual_pacote_bytes = qual_pacote.to_bytes(1, byteorder='big')
                            head_s = b'\x02' + qual_pacote_bytes + b'\x00'*8 + eop_certo 
                            com1.sendData(head_s)
                            img_bytes = b''
                            imageW = './imgs/' + str(head[1]) + str(head[2]) + '.png'


                        # Tipo 6 (erros)
                        elif n_bytes_enviado != n_bytes_recebido or eop != eop_certo:
                            qual_pacote = head[5]
                            qual_pacote_bytes = qual_pacote.to_bytes(1, byteorder='big')
                            head_s = b'\x06' + qual_pacote_bytes + b'\x00'*8 + eop_certo 
                            com1.sendData(head_s)
                            com1.rx.clearBuffer()

                            if j == 1:
                                mensagem_erro = f"Erro detectado no pacote {qual_pacote}.\n"
                                with open('log_erros_arq1.txt', 'a') as arquivo_log:
                                    arquivo_log.write(mensagem_erro)
                            
                            else:
                                mensagem_erro = f"Erro detectado no pacote {qual_pacote}.\n"
                                with open('log_erros_arq2.txt', 'a') as arquivo_log:
                                    arquivo_log.write(mensagem_erro)


                        # Tipo 3
                        elif head[0] == 3:
                            qual_pacote = head[5]+1
                            qual_pacote_bytes = qual_pacote.to_bytes(1, byteorder='big')
                            head_s = b'\x04' + qual_pacote_bytes + b'\x00'*8 + eop_certo 
                            com1.sendData(head_s)

                            if ult_payload != payload:
                                img_bytes += payload   
                                n_bytes_total += n_bytes_recebido
                            else: 
                                qual_pacote = head[5]-1
                        
                            ult_payload = payload
                    



                print(f'recebi {n_bytes_total}')
                print(qual_pacote)

            
            imagem = open(imageW, 'wb')
            imagem = imagem.write(img_bytes)
            print('----------------------')
            print('I m a g e m  s a l v a')
            print('----------------------')
            img_bytes = b''
            n_bytes_total = 0
            j+=1
            time.sleep(1)


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
