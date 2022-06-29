import logging
import threading
import time
import random

import db
import pandas as pd



LOG_FORMAT = '%(asctime)s - %(threadName)s - %(message)s'
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)

last = None
items = []
lista_imagens = []
lista_dados = []
produzido = False
consumido = False
condition = threading.Condition()


class Consumer(threading.Thread):
    def consume(self):
        global last
        global produzido
        global consumido
        global lista_imagens
        global lista_dados


        with condition:
            if len(lista_imagens) == 0:
                logging.info('no items to consume')
                consumido = True
                if(not produzido):
                    condition.wait()
                logging.info('Consumer continues..')
            if len(lista_imagens) != 0:
                consumido = False
                item = lista_imagens.pop(0)
                lista_dados.append(db.extrair_m(item))
                last = time.time()
                logging.info('consumed item {} at {}'.format(len(item), last))
            condition.notify()

    def run(self):
        while True:
            print('consumido: {} | produzido: {}'.format(consumido, produzido))
            if(consumido and produzido):
                break
            self.consume()


class Producer(threading.Thread):
    def produce(self):
        with condition:
            if len(lista_imagens) == 100:
                logging.info('items produced {}. Stopped'.format(len(items)))
                condition.wait()
                logging.info('Producer continues..')

            item = items.pop(0)
            lista_imagens.append(db.montar(item))
            
            logging.info('Added item {}'.format(len(item)))
            logging.info('total items {}'.format(len(items)))
            condition.notify()

    def run(self):
        global last
        global produzido
        global consumido
        global lista_imagens
        global lista_dados
        
        num_items = len(items)
        for i in range(num_items):
            self.produce()
        produzido = True
        logging.info('Producer all items produced..')


def main():
    producer = Producer(name='Producer')
    consumer = Consumer(name='Consumer')

    dataframe = pd.read_csv('./dev/photos.csv', delimiter=';')
    for index, row in dataframe.iterrows():
        items.append(row)

    producer.start()
    consumer.start()
    producer.join()
    consumer.join()

    print(len(lista_dados))


if __name__ == "__main__":
    main()