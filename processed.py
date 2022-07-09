'''
Processed approach

COMO EXECUTAR: python processed.py -k 4 -i 4
-k Indica o número de prcocessos
-i Indica o número de imagens a serem processadas
'''

import argparse
import time
from multiprocessing import Process, JoinableQueue
import coffee_analyzer
import pandas as pd
import time


# Define a função que sera executada por cada processo
# Recebe a fila de imagens e o array de dados
# O array de dados é utilizado para armazenar os dados de cada imagem
# A função pega uma imagem da fila, processa e armazena os dados
# Se a fila de imagens a serem processadas estiver vazia o processo é finalizada
def function(QUEUE_IMAGES, QUEUE_DATA):
    while True:
        image = QUEUE_IMAGES.get()
        QUEUE_DATA.put(coffee_analyzer.read_crop_analyze(image))
        print(QUEUE_DATA.qsize())
        QUEUE_IMAGES.task_done()
        if QUEUE_IMAGES.empty():
            break


def main():
    QUEUE_IMAGES = JoinableQueue()
    QUEUE_DATA = JoinableQueue()
    
    # Parseando os argumentos da linha de comando
    # Pode ser informado a quantidade de processos e a quantidade de imagens
    parser = argparse.ArgumentParser('PROCESS')
    parser.add_argument('-k', '--process', type=int, default=4)
    parser.add_argument('-i', '--images', type=int, default=24)
    args = parser.parse_args()

    TOTAL_PROCESS = args.process

    START_TIME = time.time()

    # Criando os processos na quantidade informada e passando por parametro a fila de imagens
    list_process = [Process(target=function, args=[QUEUE_IMAGES, QUEUE_DATA]) for _ in range(TOTAL_PROCESS)]

    df = pd.read_csv('./photos.csv', delimiter=';')

    # Verificando se quantidade de imagens informadas é maior que a quantidade disponível
    if(args.images > df.shape[0]):
        args.images = df.shape[0]

    # Carregando o caminho das imagens para a fila
    for i in range(args.images):
        QUEUE_IMAGES.put(df.iloc[i])

    # Iniciando os processos
    for process in list_process:
        process.start()

    # Esperando todos os processos terminarem
    QUEUE_IMAGES.join()
    END_TIME = time.time()
    
    print('Time for Processed:', END_TIME - START_TIME, 'secs')


if __name__ == "__main__":
    main()