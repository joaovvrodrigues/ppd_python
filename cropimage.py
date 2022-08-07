from PIL import Image
import numpy as np
import io
import cv2
import celery
import base64

# SUBIR O SERVIDOR RABBIT sudo rabbitmq-server
# VERIFICA SE O SERVIDOR ESTA RODANDO sudo rabbitmqctl status
# RODAR O CELERY celery -A cropimage worker --loglevel=info
# EXECUTAR O ARQUIVO python3 cropmain.py

# Nome da função que será chamada pelo worker
# Broker envia e recebe mensagens relacionadas a tarefas distribuídas (RabbitMQ)
# Backend armazena os resultados calculados quando houver algum delay na rede (Redis)

app = celery.Celery('cropimage', broker='amqp://172.21.45.18:5672', backend='redis://172.21.45.18')

# Recebe a imagem e retorna os dados da imagem (H, S, V, L, A, B, Grey)
@app.task
def read_crop_analyze(coffee, paper, agtron,flash, x, y, h):

    coffee_img = bytes_to_image(coffee)
    paper_img = bytes_to_image(paper)

    row_data = []

    # Carregando a imagem e aplica a função de corte, que irá cortar a imagem nos pontos informados
    img_coffee = crop_image(coffee_img, x, y, h)
    img_paper = crop_image(paper_img, x, y, h)

    agtron_value = agtron
    flash_value = flash

    print('flash: {}, agtron: {}'.format(flash_value, agtron_value))

    # Cria um dicionário com os dados da imagem de café (Componentes referentes a cor)
    row_data.extend(mean_std(extract_hsv(img_coffee)))
    row_data.extend(mean_std(extract_lab(img_coffee)))
    row_data.extend([np.mean(extract_grey(img_coffee)),
                    np.std(extract_grey(img_coffee))])

    # Cria um dicionário com os dados da imagem de papel (Componentes referentes a iluminação)
    row_data.extend(mean_std([extract_hsv(img_paper)[2]]))
    row_data.extend(mean_std([extract_lab(img_paper)[0]]))
    row_data.extend([np.mean(extract_grey(img_paper)),
                    np.std(extract_grey(img_paper))])

    # Arrendonda as casas decimais
    row_data = [round(num, 3) for num in row_data]
    row_data.extend([flash_value, 'Agtron {}'.format(agtron_value)])

    # Retorna o dicionário com os dados da imagem
    return row_data

# Converte os bytes para uma imagem em cv2
def bytes_to_image(bytes):
    byte = bytes.encode('utf-8')
    decoded = base64.b64decode(byte)
    pil = Image.open(io.BytesIO(decoded))
    img = cv2.cvtColor(np.array(pil), cv2.COLOR_RGB2BGR)
    return img

# Corta a imagem nos pontos informados
def crop_image(img, x, y, h):
    return img[y:y+h, x:x+h]

# Converte a imagem para HSV
# Retorna o H, S, V separados
def extract_hsv(img):
    hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    H, S, V = cv2.split(hsv_img)
    return (H, S, V)

# Converte a imagem para LAB
# Retorna o L, A, B separados
def extract_lab(img):
    lab_img = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    L, A, B = cv2.split(lab_img)
    return (L, A, B)

# Converte a imagem para cinza
# Retorna o Grey
def extract_grey(img):
    grey_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return grey_img

# Calcula o média e o desvio padrão de cada componente da imagem
def mean_std(data):
    list_data = []
    for index, component in enumerate(data):
        list_data.append(np.mean(component))
        list_data.append(np.std(component))

    return list_data
