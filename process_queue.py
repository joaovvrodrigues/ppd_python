import multiprocessing
import random
import time

import db
import pandas as pd

infos = []

class producer(multiprocessing.Process):
    def __init__(self, queue):
        super().__init__()
        self.queue = queue

    def run(self):
        dataframe = pd.read_csv('./photos.csv', delimiter=';')
        for index, row in dataframe.iterrows():
            image_cropped = db.montar(row)
            self.queue.put(image_cropped)
            print('Process Producer: item index {} appended to queue {}'.format(index, self.queue.qsize()))
            print('The size of queue is {}'.format(self.queue.qsize()))
            # time.sleep(0.5)
        print('Process Producer: all items appended to queue {}'.format(self.queue.qsize()))

class consumer(multiprocessing.Process):
    def __init__(self, queue):
        super().__init__()
        self.queue = queue

    def run(self):
        dataframe = pd.read_csv('./photos.csv', delimiter=';')
        while True:
            global infos
            time.sleep(.1)
            if (dataframe.shape[0] == len(infos)):
                print('the queue is empty')
                break
            else:
                if(self.queue.qsize() > 0):
                    image_cropped = self.queue.get()
                    infos.append(db.extrair_m(image_cropped))
                    print('Process Consumer: item {} popped from by {}'.format(image_cropped[2], self.name))

if __name__ == '__main__':
    dataframe = pd.read_csv('./photos.csv', delimiter=';')
    queue = multiprocessing.Queue(dataframe.shape[0])
    start_time = time.time()
    process_producer = producer(queue)
    process_consumer = consumer(queue)
    process_producer.start()
    process_consumer.start()
    process_producer.join()
    process_consumer.join()
    end_time = time.time()
    
    print('Time for Processed:', end_time - start_time, 'secs')

    print(len(infos))