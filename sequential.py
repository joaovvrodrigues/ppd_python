'''
Sequential approach
Time for sequential: 18.905866146087646 secs
24 imagens
'''

import time
import db
import pandas as pd


def main():
    itens = []
    
    start_time = time.time()
    
    dataframe = pd.read_csv('./photos.csv', delimiter=';')
    for index, row in dataframe.iterrows():
        itens.append(db.extrair(row))
    
    end_time = time.time()

    print('Time for sequential:', end_time - start_time, 'secs')
    print('Total itens:', len(itens))

if __name__ == '__main__':
    main()
