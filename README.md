# PPD - Trabalho 1
O objetivo deste trabalho é demonstrar como a programação paralela pode ser usada para reduzir o tempo de processamento de diversos tipos de programas, bem como apresentar os resultados obtidos através de sua aplicação em um algoritmo de extração de características e cores de imagens.

## Implementações

- Implementação sequencial
- Implementeação utilizando threads
- Implementeação utilizando processos

## Como executar

Existem dois parametros que podem ser alterados para a execução do programa.
 - -k : Indica o número de threads ou processos (Padrão: 4)
 - -i  : Indica o número de imagens a serem processadas (Padrão: 24)

##### Implementação sequencial

```sh
python sequential.py -i 4
```

##### Implementação com Threads

```sh
python threaded.py -k 4 -i 4
```

##### Implementação com Processos

```sh
python processed.py -k 4 -i 4
```

## Bibliotecas

Bibliotecas necessárias para a execução do programa.

| Plugin | 
| ------ |
| Multiprocessing | 
| Threading | 
| Queue |
| Pandas | 
| Numpy |
| Cv2 | 

