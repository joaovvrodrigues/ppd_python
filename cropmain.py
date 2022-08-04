import time
from celery import group
import cropimage
import argparse
import time
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

    # Split the sequence (considering 16 processes)
    # A works start a process per core
    # parts = 2
    # sub_size = int(args.images) // parts
    # subseqs = [df.iloc[i * sub_size:(i + 1) * sub_size] for i in range(parts - 1)]
    # subseqs.append(df.iloc[(parts - 1) * sub_size:])

    # print(subseqs)
    for i in range(args.images):
        result = cropimage.read_crop_analyze.delay(df.iloc[i])
        print(result.get())
    
    # partials = group(sort.s(seq) for seq in subseqs)().get()

    # Merge all the individual sorted sub-lists into our final result.
    # result = partials[0]
    # for partial in partials[1:]:
    #     result = merge(result, partial)
    # # Processando as imagens
    # for i in range(args.images):
    #     itens.append(coffee_analyzer.read_crop_analyze(df.iloc[i]))

    END_TIME = time.time()

    print('Time for sequential:', END_TIME - START_TIME, 'secs')
    print('Total itens:', len(itens))


if __name__ == '__main__':
    main()

# # Create a list of 1,000,000 elements in random order.
# sequence = list(range(1000000))
# random.shuffle(sequence)
# start_time = time.time()

# # Split the sequence (considering 16 processes)
# # A works start a process per core
# parts = 16
# sub_size = len(sequence) // parts
# subseqs = [sequence[i * sub_size:(i + 1) * sub_size] for i in range(parts - 1)]
# subseqs.append(sequence[(parts - 1) * sub_size:])

# # Ask the Celery workers to sort each sub-sequence.
# # Use a group to run the individual independent tasks as a unit of work.
# partials = group(sort.s(seq) for seq in subseqs)().get()

# # Merge all the individual sorted sub-lists into our final result.
# result = partials[0]
# for partial in partials[1:]:
#     result = merge(result, partial)
# distrib_time = time.time() - start_time
# print('Distributed mergesort took %.02fs' % (distrib_time))
