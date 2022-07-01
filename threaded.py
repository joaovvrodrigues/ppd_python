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
    
    parser = argparse.ArgumentParser('THREADED')
    parser.add_argument('-k', '--threads', type=int, default=4)
    parser.add_argument('-i', '--images', type=int, default=24)
    args = parser.parse_args()

    TOTAL_THREADS = args.threads

    START_TIME = time.time()
    threads = [Thread(target=function, args=[QUEUE_IMAGES, DATA]) for _ in range(TOTAL_THREADS)]

    df = pd.read_csv('./photos.csv', delimiter=';')

    if(args.images > df.shape[0]):
        args.images = df.shape[0]

    for i in range(args.images):
        QUEUE_IMAGES.put(df.iloc[i])

    for thread in threads:
        thread.start()

    QUEUE_IMAGES.join()
    END_TIME = time.time()

    print('Time for Threaded:', END_TIME - START_TIME, 'secs')
    print(len(DATA))

if __name__ == "__main__":
    main()
