import cv2
import numpy as np


def extrair(row):
    row_data = []

    img_coffee = row[0]
    img_paper = row[1]
    agtron_value = row[2]
    flash_value = row[3]

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

    row_data = [round(num, 3) for num in row_data]
    row_data.extend([flash_value, 'Agtron {}'.format(agtron_value)])
    return row_data


def montar(row):
    img_coffee = crop_image(cv2.imread(
        './RAW/{}'.format(row['name_coffee'])), row['X1'], row['Y1'], row['H'])
    img_paper = crop_image(cv2.imread(
        './RAW/{}'.format(row['name_paper'])), row['X1'], row['Y1'], row['H'])

    agtron_value = row['agtron']
    flash_value = row['flash']

    return [img_coffee, img_paper, agtron_value, flash_value]


def crop_image(img, x, y, h):
    return img[y:y+h, x:x+h]


def extract_rgb(img):
    R, G, B = cv2.split(img)
    return (R, G, B)


def extract_hsv(img):
    hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    H, S, V = cv2.split(hsv_img)
    return (H, S, V)


def extract_lab(img):
    lab_img = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    L, A, B = cv2.split(lab_img)
    return (L, A, B)


def extract_grey(img):
    grey_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return grey_img


def mean_std(data):
    list_data = []
    for index, component in enumerate(data):
        list_data.append(np.mean(component))
        list_data.append(np.std(component))

    return list_data
