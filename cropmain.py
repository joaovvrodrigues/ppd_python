import time
import cropimage
import argparse
import time
import pandas as pd
import base64


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

    for i in range(args.images):
        with open('./RAW/{}'.format(df.iloc[i][1]), "rb") as f:
            bytes_coffee = f.read()        
        b64_coffee = base64.b64encode(bytes_coffee).decode("utf8")
        
        with open('./RAW/{}'.format(df.iloc[i][2]), "rb") as f:
            bytes_paper = f.read()        
        b64_paper = base64.b64encode(bytes_paper).decode("utf8")

        result = cropimage.read_crop_analyze.delay(b64_coffee, b64_paper, int(df.iloc[i][3]), int(df.iloc[i][4]),  int(df.iloc[i][5]),  int(df.iloc[i][6]), int(df.iloc[i][9]),  )
        print(result.get())

    END_TIME = time.time()

    print('Time for sequential:', END_TIME - START_TIME, 'secs')
    print('Total itens:', len(itens))    

if __name__ == '__main__':
    main()