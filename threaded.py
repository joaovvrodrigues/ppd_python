'''
Threaded approach

COMO EXECUTAR: python threaded.py -k 4 -i 4
-k Indica o número de threads
-i Indica o número de imagens a serem processadas
'''
import argparse
import time
from queue import Queue
from threading import Thread
import coffee_analyzer
import pandas as pd
import time

# Define a função que sera executada por cada thread
# Recebe a fila de imagens e o array de dados
# O array de dados é utilizado para armazenar os dados de cada imagem
# A função pega uma imagem da fila, processa e armazena os dados
# Se a fila de imagens a serem processadas estiver vazia a thread é finalizada
def function(QUEUE_IMAGES, DATA):
    while True:
        image = QUEUE_IMAGES.get()
        DATA.append(coffee_analyzer.read_crop_analyze(image))
        QUEUE_IMAGES.task_done()
        if QUEUE_IMAGES.empty():
            break


def main():
    QUEUE_IMAGES = Queue()
    DATA = []

    # Parseando os argumentos da linha de comando
    # Pode ser informado a quantidade de threads e a quantidade de imagens
    parser = argparse.ArgumentParser('THREADED')
    parser.add_argument('-k', '--threads', type=int, default=4)
    parser.add_argument('-i', '--images', type=int, default=24)
    args = parser.parse_args()

    TOTAL_THREADS = args.threads

    START_TIME = time.time()

    # Criando as threads na quantidade informada e passando por parametro a fila de imagens
    threads = [Thread(target=function, args=[QUEUE_IMAGES, DATA]) for _ in range(TOTAL_THREADS)]

    df = pd.read_csv('./photos.csv', delimiter=';')

    # Verificando se quantidade de imagens informadas é maior que a quantidade disponível
    if(args.images > df.shape[0]):
        args.images = df.shape[0]

    # Carregando o caminho das imagens para a fila
    for i in range(args.images):
        QUEUE_IMAGES.put(df.iloc[i])

    # Iniciando as threads
    for thread in threads:
        thread.start()

    # Esperando as threads finalizarem
    QUEUE_IMAGES.join()
    END_TIME = time.time()

    print('Time for Threaded:', END_TIME - START_TIME, 'secs')
    print('Total itens:', len(DATA))

if __name__ == "__main__":
    main()
