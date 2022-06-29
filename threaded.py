'''
Sequential approach
Time for Threaded: 5.90933632850647 secs
24 imagens
'''

import time
from queue import Queue
from threading import Thread
import db
import pandas as pd
import time

NUM_WORKERS = 4
QUEUE_IMAGES = Queue()
DATA = []

def worker():
    while True:
        image = QUEUE_IMAGES.get()
        DATA.append(db.extrair(image))
        QUEUE_IMAGES.task_done()
        if QUEUE_IMAGES.empty():
            break


def main():
    start_time = time.time()
    threads = [Thread(target=worker) for _ in range(NUM_WORKERS)]

    dataframe = pd.read_csv('./photos.csv', delimiter=';')

    for index, row in dataframe.iterrows():
        QUEUE_IMAGES.put(row)

    for thread in threads:
        thread.start()

    QUEUE_IMAGES.join()
    end_time = time.time()
    
    print('Time for Threaded:', end_time - start_time, 'secs')
    print(len(DATA))


if __name__ == "__main__":
    main()
