import tkinter as tk
from tkinter import messagebox
import csv
import os
import string
import unicodedata
from datetime import datetime

# Função para normalizar texto (remover acentos e caracteres especiais)
def normalize_text(text):
    normalized = unicodedata.normalize('NFD', text)
    return ''.join(
        char for char in normalized
        if not unicodedata.combining(char)
    )

# Função para aplicar a cifra de César
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
            result += char
    return result

# Função para registrar erros em um arquivo CSV
def log_error(error_message):
    file_exists = os.path.isfile("log_erros.csv")
    with open("log_erros.csv", mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["Horário", "Mensagem de Erro"])
        writer.writerow([datetime.now().isoformat(), error_message])

# Função para processar o texto inserido pelo usuário
def process_text():
    try:
        text = entry_text.get()
        shift = int(entry_shift.get())
        decrypt = decrypt_var.get()

        if not text.strip():
            raise ValueError("Por favor, insira um texto para processar.")

        normalized_text = normalize_text(text)
        result = caesar_cipher(normalized_text, shift, decrypt)
        result_text.delete("1.0", tk.END)
        result_text.insert(tk.END, result)

    except ValueError as ve:
        error_message = f"Erro de entrada: {ve}"
        messagebox.showerror("Erro", error_message)
        log_error(error_message)
    except Exception as e:
        error_message = f"Erro inesperado: {str(e)}"
        messagebox.showerror("Erro", error_message)
        log_error(error_message)

# Configuração da interface gráfica com tema de espaço
root = tk.Tk()
root.title("Cifra do Astronauta no Espaço")
root.configure(bg="#001f3f")

# Título
title_label = tk.Label(root, text="🚀 Cifra do Astronauta no Espaço 🌌", 
                       font=("Comic Sans MS", 18, "bold"), fg="white", bg="#001f3f")
title_label.grid(row=0, column=0, columnspan=2, pady=10)

# Campo para inserir o texto
tk.Label(root, text="Mensagem para criptografar:", font=("Arial", 12), fg="white", bg="#001f3f").grid(row=1, column=0, padx=10, pady=5, sticky="e")
entry_text = tk.Entry(root, width=40, font=("Courier New", 12))
entry_text.grid(row=1, column=1, padx=10, pady=5)

# Campo para inserir o deslocamento
tk.Label(root, text="Deslocamento:", font=("Arial", 12), fg="white", bg="#001f3f").grid(row=2, column=0, padx=10, pady=5, sticky="e")
entry_shift = tk.Entry(root, width=10, font=("Courier New", 12))
entry_shift.grid(row=2, column=1, padx=10, pady=5, sticky="w")

# Checkbox para descriptografar
decrypt_var = tk.BooleanVar()
decrypt_check = tk.Checkbutton(root, text="Descriptografar", variable=decrypt_var, 
                               font=("Arial", 12), fg="white", bg="#001f3f", selectcolor="#003366")
decrypt_check.grid(row=3, column=1, padx=10, pady=5, sticky="w")

# Botão para processar
process_button = tk.Button(root, text="Lançar 🚀", font=("Arial", 12, "bold"), 
                           bg="#0074D9", fg="white", command=process_text)
process_button.grid(row=4, column=1, padx=10, pady=10, sticky="w")

# Rótulo e área de texto para exibir o resultado
tk.Label(root, text="Mensagem criptografada/descriptografada:", font=("Arial", 12), fg="white", bg="#001f3f").grid(row=5, column=0, padx=10, pady=5, sticky="ne")
result_text = tk.Text(root, height=5, width=40, font=("Courier New", 12), bg="#011627", fg="#29A19C")
result_text.grid(row=5, column=1, padx=10, pady=10)

# Decoração temática
spaceship_label = tk.Label(root, text="🌌✨ Viaje pelo universo das cifras! ✨🌌",
                           font=("Comic Sans MS", 12, "italic"), fg="white", bg="#001f3f")
spaceship_label.grid(row=6, column=0, columnspan=2, pady=10)

root.mainloop()
