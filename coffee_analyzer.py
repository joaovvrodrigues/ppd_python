import cv2
import numpy as np


# Recebe a imagem e retorna os dados da imagem (H, S, V, L, A, B, Grey)
def read_crop_analyze(row):
    row_data = []

    # Carregando a imagem e aplica a função de corte, que irá cortar a imagem nos pontos informados
    img_coffee = crop_image(cv2.imread(
        './RAW/{}'.format(row['name_coffee'])), row['X1'], row['Y1'], row['H'])
    img_paper = crop_image(cv2.imread(
        './RAW/{}'.format(row['name_paper'])), row['X1'], row['Y1'], row['H'])

    agtron_value = row['agtron']
    flash_value = row['flash']

    print('device: {}, flash: {}, agtron: {}'.format(
        row['device_id'], flash_value, agtron_value))

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
