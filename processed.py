'''
Processed approach
Time for Processed: 6.730908632278442 secs
24 imagens
'''

import time
from multiprocessing import Process, JoinableQueue
import db
import pandas as pd
import time


TOTAL_PROCESS = 4
QUEUE_IMAGES = JoinableQueue()
QUEUE_DATA = JoinableQueue()

def function(QUEUE_IMAGES, QUEUE_DATA):
    while True:
        image = QUEUE_IMAGES.get()
        QUEUE_DATA.put(db.extrair(image))
        print(QUEUE_DATA.qsize())
        QUEUE_IMAGES.task_done()
        if QUEUE_IMAGES.empty():
            break


def main():
    start_time = time.time()
    list_process = [Process(target=function, args=[QUEUE_IMAGES, QUEUE_DATA]) for _ in range(TOTAL_PROCESS)]

    dataframe = pd.read_csv('./photos.csv', delimiter=';')

    for index, row in dataframe.iterrows():
        QUEUE_IMAGES.put(row)

    for process in list_process:
        process.start()

    QUEUE_IMAGES.join()
    end_time = time.time()
    
    print('Time for Processed:', end_time - start_time, 'secs')
    print(QUEUE_DATA.qsize())


if __name__ == "__main__":
    main()