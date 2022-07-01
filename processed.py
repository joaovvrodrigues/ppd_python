'''
Processed approach

COMO EXECUTAR: python processed.py -k 4 -i 4
-k Indica o número de prcocessos
-i Indica o número de imagens a serem processadas
'''

import argparse
import time
from multiprocessing import Process, JoinableQueue
import db
import pandas as pd
import time


def function(QUEUE_IMAGES, QUEUE_DATA):
    while True:
        image = QUEUE_IMAGES.get()
        QUEUE_DATA.put(db.read_crop_analyze(image))
        print(QUEUE_DATA.qsize())
        QUEUE_IMAGES.task_done()
        if QUEUE_IMAGES.empty():
            break


def main():
    QUEUE_IMAGES = JoinableQueue()
    QUEUE_DATA = JoinableQueue()

    parser = argparse.ArgumentParser('PROCESS')
    parser.add_argument('-k', '--process', type=int, default=4)
    parser.add_argument('-i', '--images', type=int, default=24)
    args = parser.parse_args()

    TOTAL_PROCESS = args.process

    START_TIME = time.time()
    list_process = [Process(target=function, args=[QUEUE_IMAGES, QUEUE_DATA]) for _ in range(TOTAL_PROCESS)]

    df = pd.read_csv('./photos.csv', delimiter=';')

    if(args.images > df.shape[0]):
        args.images = df.shape[0]

    for i in range(args.images):
        QUEUE_IMAGES.put(df.iloc[i])

    for process in list_process:
        process.start()

    QUEUE_IMAGES.join()
    END_TIME = time.time()
    
    print('Time for Processed:', END_TIME - START_TIME, 'secs')


if __name__ == "__main__":
    main()