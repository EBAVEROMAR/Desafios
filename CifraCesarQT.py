#interface grafico em QT
import sys
import csv
import os
import string
import unicodedata
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QMessageBox, QCheckBox
)

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

# Classe principal da aplicação
class CaesarCipherApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Cifra de César")

        # Layout principal
        central_widget = QWidget()
        main_layout = QVBoxLayout()

        # Campo para o texto
        text_layout = QHBoxLayout()
        text_label = QLabel("Texto:")
        self.text_input = QLineEdit()
        text_layout.addWidget(text_label)
        text_layout.addWidget(self.text_input)
        main_layout.addLayout(text_layout)

        # Campo para o deslocamento
        shift_layout = QHBoxLayout()
        shift_label = QLabel("Deslocamento:")
        self.shift_input = QLineEdit()
        shift_layout.addWidget(shift_label)
        shift_layout.addWidget(self.shift_input)
        main_layout.addLayout(shift_layout)

        # Checkbox para desencriptar
        self.decrypt_checkbox = QCheckBox("Desencriptar")
        main_layout.addWidget(self.decrypt_checkbox)

        # Botão para processar
        self.process_button = QPushButton("Processar")
        self.process_button.clicked.connect(self.process_text)
        main_layout.addWidget(self.process_button)

        # Label para o resultado
        self.result_label = QLabel("Resultado: ")
        main_layout.addWidget(self.result_label)

        # Configuração final
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def process_text(self):
        try:
            text = self.text_input.text()
            shift = int(self.shift_input.text())
            decrypt = self.decrypt_checkbox.isChecked()

            if not text:
                raise ValueError("O texto não pode estar vazio.")

            normalized_text = normalize_text(text)
            result = caesar_cipher(normalized_text, shift, decrypt)
            self.result_label.setText(f"Resultado: {result}")

        except ValueError as ve:
            error_message = f"Erro de entrada: {ve}"
            QMessageBox.critical(self, "Erro", error_message)
            log_error(error_message)
        except Exception as e:
            error_message = f"Erro inesperado: {str(e)}"
            QMessageBox.critical(self, "Erro", error_message)
            log_error(error_message)

# Inicialização da aplicação
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CaesarCipherApp()
    window.show()
    sys.exit(app.exec_())
