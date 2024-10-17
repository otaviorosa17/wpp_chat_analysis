import os
from PIL import Image
import hashlib
from collections import defaultdict

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

# Exemplo de uso
folder_path = 'imgs/'
duplicatas = find_duplicate_images(folder_path)

# Contar ocorrências e ordenar
counted_duplicates = {len(files): files for files in duplicatas.values()}
sorted_duplicates = sorted(counted_duplicates.items(), key=lambda x: x[0], reverse=True)

if sorted_duplicates:
    print("\nImagens duplicadas encontradas (em ordem decrescente de ocorrências):")
    for count, files in sorted_duplicates:
        print(f"{count} ocorrências de: {files[0]}")  # Printando apenas uma ocorrência
else:
    print("Nenhuma imagem duplicada encontrada.")
