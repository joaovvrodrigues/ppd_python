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

    # Executando o processamento para cada imagem
    for i in range(args.images):
        # Carregando as imagens
        with open('./RAW/{}'.format(df.iloc[i][1]), "rb") as f:
            bytes_coffee = f.read() # Coletando os bytes da imagem de café   
        b64_coffee = base64.b64encode(bytes_coffee).decode("utf8") # Converte os bytes para base64
        
        with open('./RAW/{}'.format(df.iloc[i][2]), "rb") as f:
            bytes_paper = f.read()  # Coletando os bytes da imagem de papel
        b64_paper = base64.b64encode(bytes_paper).decode("utf8")

        # Executando o processamento
        result = cropimage.read_crop_analyze.delay(b64_coffee, b64_paper, int(df.iloc[i][3]), int(df.iloc[i][4]),  int(df.iloc[i][5]),  int(df.iloc[i][6]), int(df.iloc[i][9]),  ) 
        print(result.get()) 

    END_TIME = time.time() # Finalizando o processamento

    print('Execution time:', END_TIME - START_TIME, 'secs')
    print('Total itens:', len(itens))    

if __name__ == '__main__':
    main()