import os
from PIL import Image
import hashlib
from collections import defaultdict
import re
import pandas as pd

def hash_image(image_path):
    """Gera um hash para a imagem usando o algoritmo SHA256."""
    with Image.open(image_path) as img:
        img = img.convert('RGB')  # Converte para RGB
        img_bytes = img.tobytes()  # Converte a imagem em bytes
        return hashlib.sha256(img_bytes).hexdigest()  # Retorna o hash

def find_duplicate_images(folder_path):
    """Encontra e conta imagens duplicadas em uma pasta."""
    images_hashes = defaultdict(list)

    # Listar todos os arquivos na pasta
    files = [f for f in os.listdir(folder_path) if f.lower().endswith('.webp')]
    total_files = len(files)

    for index, filename in enumerate(files):
        file_path = os.path.join(folder_path, filename)
        img_hash = hash_image(file_path)
        images_hashes[img_hash].append(filename)

        # Mensagem de progresso a cada 500 arquivos processados
        if (index + 1) % 500 == 0 or index + 1 == total_files:
            print(f"Processados {index + 1} de {total_files} arquivos.")

    # Filtrar apenas as imagens com mais de uma ocorrência
    duplicates = {hash_value: files for hash_value, files in images_hashes.items() if len(files) > 1}

    return duplicates

# Caminho para o diretório com os stickers
folder_path = 'imgs/'

# Encontrar imagens duplicadas
duplicates = find_duplicate_images(folder_path)

# Abrir e ler o arquivo de texto com mensagens
with open('cajus.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Expressão regular para capturar as informações
pattern = r'\[(\d{2}/\d{2}/\d{2}), (\d{2}:\d{2}:\d{2})\] (.*?): (.*)'

# Criar uma lista para armazenar os dados dos stickers
sticker_data = []

# Variável para armazenar a mensagem atual
current_message = ""
date, time, sender = "", "", ""

# Iterar sobre as linhas do arquivo
for line in lines:
    match = re.match(pattern, line)
    
    if match:
        # Atualiza data, hora, remetente e começa uma nova mensagem
        date, time, sender, message = match.groups()
        current_message = message  # Começa uma nova mensagem
        
        # Verifica se a mensagem indica um sticker
        if "sticker omitted" in message:
            sticker_filename = f"{sender}-STICKER-{date.replace('/', '-')}-{time}.webp"
            sticker_data.append([date, time, sender, sticker_filename])  # Adiciona dados do sticker
            
    else:
        # Se não houver correspondência, continua a mensagem atual
        if current_message:
            current_message += "\n" + line.strip()  # Adiciona a nova linha à mensagem atual

# Criar um DataFrame para stickers
df_stickers = pd.DataFrame(sticker_data, columns=['Date', 'Time', 'Sender', 'Sticker_File'])

# Contar ocorrências de stickers
sticker_counts = df_stickers['Sticker_File'].value_counts().reset_index()
sticker_counts.columns = ['Sticker_File', 'Count']

# Obter os top 3 stickers
top_stickers = sticker_counts.head(3)['Sticker_File'].tolist()

# Criar um dicionário para armazenar os top senders para cada sticker
top_senders = {}

for sticker in top_stickers:
    top_sender_for_sticker = df_stickers[df_stickers['Sticker_File'] == sticker]['Sender'].value_counts().head(3).index.tolist()
    top_senders[sticker] = top_sender_for_sticker

# Relacionar stickers duplicados com os top senders
for sticker_hash, sticker_files in duplicates.items():
    for sticker_file in sticker_files:
        for top_sticker in top_stickers:
            if top_sticker == sticker_file:
                print(f"\nSticker duplicado: {sticker_file}")
                print(f"Ocorrências: {len(sticker_files)}")
                print("Top Senders:", top_senders.get(top_sticker, []))

# Exibir resultados
if not duplicates:
    print("Nenhuma imagem duplicada encontrada.")
