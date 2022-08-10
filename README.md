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
| Celery |
| Redis |

# PPD - Trabalho 2

O objetivo deste trabalho é demonstrar como a programação distribuída pode ser usada para reduzir o tempo de processamento de diversos tipos de programas, bem como apresentar os resultados obtidos através de sua aplicação em um algoritmo de extração de características e cores de imagens.

## Como executar

É necessário instalar 3 softwares nas máquinas disponíveis para executar este programa:

- Celery
- Redis
- RabbitMQ

Na máquina que servirá como worker, é necessário instalar o Celery. Na máquina que servirá como broker, é necessário instalar o RabbitMQ e o Redis. Também é necessário instalar
as bibliotecas do python para o celery e o redis. As bibliotecas devem ser instaladas em todas as máquinas, através dos comandos:

```pip install celery```
```pip install redis```

Para executar o programa, primeiro é necessário inicializar o RabbitMQ e o Redis na máquina que servirá como broker. Também é necessário inicializar o Celery na(s) máquina(s) que servirá(ão) como worker(s) através do comando:

```celery -A cropimage worker --loglevel=info```

Após a inicialização do RabbitMQ e do Redis no broker, o programa pode ser executado através do comando:

```python cropmain.py```

