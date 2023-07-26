import os
import re


def to_int(price: str) -> float:
    '''
        Из строки берет только числа и конвертирует в int
    '''
    return int(''.join(re.findall(r'\d+', price)))


def save_file(file_name: str, extention: str, content: str, folder: str='errors') -> str:
    i = 0
    if not os.path.exists(folder):
        os.mkdir(folder)
        
    while os.path.exists(f'{folder}/{file_name}({i}).{extention}'):
        i += 1

    full_file_name = f'{folder}/{file_name}({i}).{extention}'

    with open(full_file_name, 'w', encoding="utf-8") as f:
        f.write(content)

    return full_file_name
