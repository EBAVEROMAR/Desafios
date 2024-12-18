#interface grafico em Tkinter

import tkinter as tk
from tkinter import messagebox
import csv
import os
import string
import unicodedata

# Função para normalizar texto (substituir acentos e caracteres especiais)
def normalize_text(text):
    normalized = unicodedata.normalize('NFD', text)
    return ''.join(
        char if char.isalnum() else '.' if char not in string.ascii_letters else ''
        for char in normalized
        if not unicodedata.combining(char)
    )

# Função para encriptar ou desencriptar usando a cifra de César
def caesar_cipher(text, shift, decrypt=False):
    if decrypt:
        shift = -shift

    result = ""
    for char in text:
        if char.isalpha():
            alpha_set = string.ascii_lowercase if char.islower() else string.ascii_uppercase
            new_pos = (alpha_set.index(char) + shift) % 26
            result += alpha_set[new_pos]
        else:
            result += '.'  # Converte caracteres especiais em ponto
    return result

# Função para registar erros em CSV
def log_error(error_message):
    file_exists = os.path.isfile("error_log.csv")
    with open("error_log.csv", mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["Error Message"])
        writer.writerow([error_message])

# Função para processar texto com base na ação do utilizador
def process_text():
    try:
        text = entry_text.get()
        shift = int(entry_shift.get())
        decrypt = decrypt_var.get()

        if not text:
            raise ValueError("O texto não pode estar vazio.")

        normalized_text = normalize_text(text)
        result = caesar_cipher(normalized_text, shift, decrypt)
        result_label.config(text=f"Resultado: {result}")

    except ValueError as ve:
        error_message = f"Erro de entrada: {ve}"
        messagebox.showerror("Erro", error_message)
        log_error(error_message)
    except Exception as e:
        error_message = f"Erro inesperado: {str(e)}"
        messagebox.showerror("Erro", error_message)
        log_error(error_message)

# Configuração da interface gráfica
root = tk.Tk()
root.title("Cifra de César")

# Campo para o texto
label_text = tk.Label(root, text="Texto:")
label_text.grid(row=0, column=0, padx=10, pady=5, sticky="e")
entry_text = tk.Entry(root, width=40)
entry_text.grid(row=0, column=1, padx=10, pady=5)

# Campo para o deslocamento
label_shift = tk.Label(root, text="Deslocamento:")
label_shift.grid(row=1, column=0, padx=10, pady=5, sticky="e")
entry_shift = tk.Entry(root, width=10)
entry_shift.grid(row=1, column=1, padx=10, pady=5, sticky="w")

# Checkbox para desencriptar
decrypt_var = tk.BooleanVar()
decrypt_check = tk.Checkbutton(root, text="Desencriptar", variable=decrypt_var)
decrypt_check.grid(row=2, column=1, padx=10, pady=5, sticky="w")

# Botão para processar
process_button = tk.Button(root, text="Processar", command=process_text)
process_button.grid(row=3, column=1, padx=10, pady=10, sticky="w")

# Label para o resultado
result_label = tk.Label(root, text="Resultado: ")
result_label.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

root.mainloop()
