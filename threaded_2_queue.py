'''
threaded approach
Time for Threaded 2 Queue: 8.606582641601562 secs
24 imagens
'''

import time
from queue import Queue
from threading import Thread
import db
import pandas as pd
import time

TOTAL_THREADS = 4
QUEUE_LINKS = Queue()
QUEUE_IMAGENS = Queue()
DATA = []
PRODUZIDO = False


def montador():
    while True:
        global PRODUZIDO

        image = QUEUE_LINKS.get()
        a = db.montar(image)
        QUEUE_IMAGENS.put(a)
        QUEUE_LINKS.task_done()
        if QUEUE_LINKS.empty():
            print('QUEUE_LINKS.empty()')
            PRODUZIDO = True
            break


def extrator():
    while True:
        global PRODUZIDO

        images = QUEUE_IMAGENS.get()
        DATA.append(db.extrair_m(images))
        QUEUE_IMAGENS.task_done()
        if QUEUE_IMAGENS.empty() and PRODUZIDO:
            print('QUEUE_IMAGENS.empty()')
            break


def main():
    start_time = time.time()
    threads_montadoras = [Thread(target=montador)
                          for _ in range(TOTAL_THREADS//2)]
    threads_extratoras = [Thread(target=extrator)
                          for _ in range(TOTAL_THREADS//2)]

    dataframe = pd.read_csv('./photos.csv', delimiter=';')

    for index, row in dataframe.iterrows():
        QUEUE_LINKS.put(row)

    # Start all the workers
    for index in range(len(threads_montadoras)):
        threads_montadoras[index].start()
        threads_extratoras[index].start()

    # Usando sommente o join() da queue ele finaliza antes de terminar os threads
    # for index in range(len(threads_montadoras)):
    #     threads_montadoras[index].join()
    #     threads_extratoras[index].join()

    QUEUE_LINKS.join()
    QUEUE_IMAGENS.join()

    end_time = time.time()
    print('Time for Threaded 2 queue:', end_time - start_time, 'secs')
    print('Foram extraidos ', len(DATA), ' dados mas deveriam ser ', dataframe.shape[0] )


if __name__ == "__main__":
    main()
