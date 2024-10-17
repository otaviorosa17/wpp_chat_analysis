import re
import pandas as pd

# Abrir e ler o arquivo de texto
with open('cajus.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Expressão regular para capturar as informações
pattern = r'\[(\d{2}/\d{2}/\d{2}), (\d{2}:\d{2}:\d{2})\] (.*?): (.*)'

# Criar uma lista para armazenar os dados
chat_data = []

# Variável para armazenar a mensagem atual
current_message = ""
date, time, sender = "", "", ""

# Iterar sobre as linhas do arquivo
for line in lines:
    match = re.match(pattern, line)
    
    if match:
        # Se houver uma correspondência, processe a mensagem atual
        if current_message:
            # Adiciona a mensagem anterior à lista antes de começar uma nova
            chat_data.append([date, time, sender, current_message])
        
        # Atualiza data, hora, remetente e começa uma nova mensagem
        date, time, sender, message = match.groups()
        current_message = message  # Começa uma nova mensagem
    else:
        # Se não houver correspondência, continua a mensagem atual
        if current_message:
            current_message += "\n" + line.strip()  # Adiciona a nova linha à mensagem atual

# Adicionar a última mensagem processada, se houver
if current_message:
    chat_data.append([date, time, sender, current_message])

# Criar o DataFrame com os dados extraídos
df = pd.DataFrame(chat_data, columns=['Date', 'Time', 'Sender', 'Message'])

# Exibir o DataFrame
print("\nDataFrame completo:")
print(df)

print(df.loc[32, 'Message'])