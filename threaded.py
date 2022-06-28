'''
threaded approach
'''

import time
from queue import Queue
from threading import Thread
import db
import cv2
import numpy as np
import pandas as pd
import csv
import datetime
import time

# Time for Threaded: 114.82532739639282 secs
NUM_WORKERS = 4
QUEUE_LINKS = Queue()
QUEUE_IMAGENS = Queue()
DATA = []


def montador():
    '''
    Thread function
    '''
    # Constantly check the queue for addresses
    while True:
        image = QUEUE_LINKS.get()
        # DATA.append(db.extrair(image))
        QUEUE_IMAGENS.put(db.montar(image))
        # Mark the processed task as done
        QUEUE_LINKS.task_done()
        if QUEUE_LINKS.empty():
            break

def extrator():
    '''
    Thread function
    '''
    # Constantly check the queue for addresses
    while True:
        images = QUEUE_IMAGENS.get()
        DATA.append(db.extrair(images))
        # Mark the processed task as done
        QUEUE_IMAGENS.task_done()
        if QUEUE_IMAGENS.empty():
            break

def main():
    '''
    Main function
    '''
    start_time = time.time()
    # Create the worker threads
    threads_montadoras = [Thread(target=montador) for _ in range(NUM_WORKERS)]
    threads_extratoras = [Thread(target=extrator) for _ in range(NUM_WORKERS)]

    # Add the websites to the task queue
    dataframe = pd.read_csv('./photos.csv', delimiter=';')

    for index, row in dataframe.iterrows():
        QUEUE_LINKS.put(row)

    # Start all the workers
    for index in range(len(threads_montadoras)):
        threads_montadoras[index].start()
        threads_extratoras[index].start()

    # Wait for all the tasks in the queue to be processed
    QUEUE_LINKS.join()
    QUEUE_IMAGENS.join()

    end_time = time.time()
    print('Time for Threaded:', end_time - start_time, 'secs')
    print(len(DATA))


if __name__ == "__main__":
    main()
