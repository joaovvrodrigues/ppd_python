'''
Sequential approach

COMO EXECUTAR: python sequential.py -i 4
-i Indica o número de imagens a serem processadas
'''
import argparse
import time
import coffee_analyzer
import pandas as pd


def main():
    itens = []

    # Parseando os argumentos da linha de comando
    parser = argparse.ArgumentParser('PROCESS')
    parser.add_argument('-i', '--images', type=int, default=24)
    args = parser.parse_args()
    
    # Iniciando o processamento
    START_TIME = time.time()
    
    # Carregando as imagens
    df = pd.read_csv('./photos.csv', delimiter=';')
    
    # Verificando se quantidade de imagens informadas é maior que a quantidade disponível
    if(args.images > df.shape[0]):
        args.images = df.shape[0]

    # Processando as imagens
    for i in range(args.images):
        itens.append(coffee_analyzer.read_crop_analyze(df.iloc[i]))

    END_TIME = time.time()

    print('Time for sequential:', END_TIME - START_TIME, 'secs')
    print('Total itens:', len(itens))


if __name__ == '__main__':
    main()
