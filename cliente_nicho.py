#####################################################
# Camada Física da Computação
#Carareto
#11/08/2022
#Aplicação
####################################################


#esta é a camada superior, de aplicação do seu software de comunicação serial UART.
#para acompanhar a execução e identificar erros, construa prints ao longo do código! 
from PIL import Image
import io
from enlace import *
import time
import numpy as np
import sys


# voce deverá descomentar e configurar a porta com através da qual ira fazer comunicaçao
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports
# se estiver usando windows, o gerenciador de dispositivos informa a porta

#use uma das 3 opcoes para atribuir à variável a porta usada
#serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
serialName = "/dev/cu.usbmodem101" # Mac    (variacao de)
#serialName = "COM11"                  # Windows(variacao de)




def main():
    try:
        
        print("Iniciou o main")
        com1 = enlace(serialName)
        com1.enable()
        time.sleep(.2)
        com1.sendData(b'00')
        time.sleep(1)
        com1.rx.clearBuffer()

        
        with Image.open("imgs/imagem.png") as img:
            img_byte_arr = io.BytesIO()
            img.save(img_byte_arr, format=img.format)     
            img_byte_arr = img_byte_arr.getvalue()

        payload = [img_byte_arr[i:i+140] for i in range(0, len(img_byte_arr), 140)]
       
 

        #### --------------- Bytes de head: 0, tipo da mensagem. 1 e 2, nome do arquivo. 3 tamanho do payload. 4. Quantos pacotes. 5 Em qual pacote estou. resto, b'\x00'
        head_r = [0,0,0,0,0]
        eop = b'\xAA' * 4
        nome_arquivo = "imagem1"
        pacotes_bytes = len(payload).to_bytes(1, byteorder='big')
        maximo = len(payload)
        primeiro = True
        n_erros = 0
        r = 1
        nome = b'\xBB' + b'\xAA'
        while r <= 2:
            if r == 2:
                nome_arquivo = "imagem2"
                com1.rx.clearBuffer()
                primeiro = True
                with Image.open("imgs/martelo.png") as img:
                    img_byte_arr = io.BytesIO()
                    img.save(img_byte_arr, format=img.format)     
                    img_byte_arr = img_byte_arr.getvalue()
                    
                payload = [img_byte_arr[i:i+140] for i in range(0, len(img_byte_arr), 140)]
                head_r = [0,0,0,0,0]
                pacotes_bytes = len(payload).to_bytes(1, byteorder='big')
                maximo = len(payload)
                primeiro = True
                n_erros = 0
                nome = b'\xCC' + b'\xDD'
                



            while head_r[1] < maximo:
                #print(maximo)
                
                print(f"recebendo head_r:   {head_r[1]}")
                tamanho_payload = len(payload[head_r[1]]).to_bytes(1, byteorder='big')
                if primeiro == True:
                    head = b'\x01'+ nome + tamanho_payload + pacotes_bytes + b'\x01' +b'\x00' * 4
                    pacote = head+payload[head_r[1]]+eop
                    txBuffer = pacote
                    print("enviando primeiro pacote")
                    print(txBuffer)
                    com1.sendData(np.asarray(txBuffer))
                    primeiro = False
                
                #print("Dados enviados. Aguardando resposta...")
                print(f"recebendo head:   {head[5]}")
                inicio = time.time() 
                inicio_r = time.time()
                tempo_limite = 10
                rxBuffer, nRx = b'', 0
                tempo_r = 2 
                
                while (time.time() - inicio) < 10.5:
                    #print(time.time()-inicio)
                    if (time.time() - inicio) > 10: 
                        print("BBBBBBB")
                        head = b'\x05' + b'\x00' * 9
                        payload = b'\x00' * 140
                        pacote = head+payload+eop
                        txBuffer = pacote
                        print("Tempo esgotado...")
                        com1.disable()
                        sys.exit()
                    elif (time.time() - inicio_r) > tempo_r:
                        print("AAAAAA")
                        com1.sendData(np.asarray(txBuffer))
                        inicio_r = time.time()
                    elif com1.rx.getBufferLen() > 13:
                        print("CCCCCCCC")
                        inicio = -100
                        head_r= com1.getData(10)[0]
                        eop_r = com1.getData(4)[0]
                        print(head_r)
                        print("AAAAAAAAA")
                        if head_r[0] == 2:#ERRO NESSA LINHA
                            print("CCCCCCCCCC")
                            em_qual_estou = head_r[1]
                            em_qual_estou1 = em_qual_estou.to_bytes(1, byteorder='big')
                            head = b'\x03'+ nome + tamanho_payload + pacotes_bytes + em_qual_estou1 + b'\x00' * 4
                            pacote = head+payload[head_r[1]-1]+eop
                            txBuffer = pacote
                            com1.sendData(np.asarray(txBuffer))

                            print("2222222222222")
                        
                        elif head_r[0] == 4:
                            em_qual_estou = head_r[1]
                            em_qual_estou1 = em_qual_estou.to_bytes(1, byteorder='big')
                            head = b'\x03'+ nome + tamanho_payload + pacotes_bytes + em_qual_estou1 + b'\x00' * 4
                            pacote = head+payload[head_r[1]-1]+eop
                            txBuffer = pacote
                            com1.sendData(np.asarray(txBuffer))
                            

                            print("4444444444")

                        
                        elif head_r[0] == 5:
                            print("Tempo esgotado...")
                            com1.disable()
                            sys.exit()

                        elif head_r[0] == 6:
                            nome_arquivo_final = nome_arquivo+".txt"
                            mensagem_erro = f"Erro detectado no pacote {head_r[1]}.\n"
                            with open(nome_arquivo_final, 'a') as arquivo_log:
                                arquivo_log.write(mensagem_erro)

                            em_qual_estou = head_r[1]
                            em_qual_estou1 = em_qual_estou.to_bytes(1, byteorder='big')
                            head = b'\x03'+ b'\xBB' + b'\xAA' + tamanho_payload + pacotes_bytes + em_qual_estou1 +b'\x00' * 4
                            pacote = head+payload[head_r[1]-1]+eop
                            txBuffer = pacote
                            com1.sendData(np.asarray(txBuffer))

                            print("66666666666")

                            n_erros+=1

                        else:
                            print("DDDDDDDDDD")

                


            print("Esperando a proxima imagem")
            time.sleep(1)
            r += 1
            print(r)
        print(img_byte_arr)
        print(len(img_byte_arr))
        print(f'{n_erros} erros')
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