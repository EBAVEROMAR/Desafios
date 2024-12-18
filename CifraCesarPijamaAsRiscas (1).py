# Cifra Cesar com onde o texto passa por 4 deslocamentos sucessivos, semelhantes ao funcionamento da máquina Enigma. 
# Cada deslocamento é realizado em uma direção diferente e com diferentes valores, criando um processo de cifra complexo!

import tkinter as tk
from tkinter import messagebox
import unicodedata
import string
import csv

# Função para cifra de César
def cifra_cesar(texto, deslocamento):
    resultado = ""
    for char in texto:
        if char.isalpha():  # Se for letra
            base = ord('A') if char.isupper() else ord('a')
            resultado += chr((ord(char) - base + deslocamento) % 26 + base)
        else:
            # Para caracteres não alfabéticos, substitui por ponto
            resultado += '.'
    return resultado

# Função para normalizar texto (remover acentos e tratar caracteres especiais)
def normalizar_texto(texto):
    texto_normalizado = unicodedata.normalize('NFKD', texto).encode('ASCII', 'ignore').decode('ASCII')
    texto_normalizado = ''.join(c if c in string.ascii_letters + string.digits + string.punctuation + ' ' else '.' for c in texto_normalizado)
    return texto_normalizado

# Função para log de erros em CSV
def registrar_erro(erro):
    with open('erros.csv', mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([erro])

# Função para cifrar o texto com 4 deslocamentos sucessivos (como a Enigma)
def cifrar_enigma(texto):
    deslocamentos = [3, 5, 7, 11]  # Valores de deslocamento diferentes para cada etapa
    for deslocamento in deslocamentos:
        texto = cifra_cesar(texto, deslocamento)
    return texto

# Função para manipular o botão de cifragem
def cifrar():
    try:
        texto = entrada_texto.get("1.0", "end-1c")  # Obtém o texto de entrada
        texto_normalizado = normalizar_texto(texto)  # Normaliza o texto
        texto_cifrado = cifrar_enigma(texto_normalizado)  # Cifra o texto com 4 deslocamentos

        resultado_label.config(text=f"Texto Cifrado: {texto_cifrado}")

    except Exception as e:
        resultado_label.config(text="Erro: Ocorreu um problema")
        registrar_erro(f"Erro desconhecido: {e}")

# Criação da interface com Tkinter
root = tk.Tk()
root.title("Cifra Enigma")

# Layout
frame = tk.Frame(root, padx=10, pady=10)
frame.pack(padx=10, pady=10)

# Texto de entrada
entrada_label = tk.Label(frame, text="Digite o texto:")
entrada_label.pack()

entrada_texto = tk.Text(frame, height=10, width=40)
entrada_texto.pack()

# Botão para cifrar
botao_cifrar = tk.Button(frame, text="Cifrar Texto", command=cifrar)
botao_cifrar.pack(pady=10)

# Resultado da cifra
resultado_label = tk.Label(frame, text="Resultado", wraplength=400)
resultado_label.pack()

# Iniciar a interface
root.mainloop()
