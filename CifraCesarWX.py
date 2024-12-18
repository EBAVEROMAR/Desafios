#interface grafico em wx

import wx
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

# Classe principal da aplicação
class CaesarCipherApp(wx.Frame):
    def __init__(self):
        super().__init__(None, title="Cifra de César", size=(400, 300))
        self.init_ui()

    def init_ui(self):
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        # Campo para o texto
        hbox_text = wx.BoxSizer(wx.HORIZONTAL)
        lbl_text = wx.StaticText(panel, label="Texto:")
        self.text_input = wx.TextCtrl(panel)
        hbox_text.Add(lbl_text, flag=wx.RIGHT, border=8)
        hbox_text.Add(self.text_input, proportion=1)
        vbox.Add(hbox_text, flag=wx.EXPAND | wx.ALL, border=10)

        # Campo para o deslocamento
        hbox_shift = wx.BoxSizer(wx.HORIZONTAL)
        lbl_shift = wx.StaticText(panel, label="Deslocamento:")
        self.shift_input = wx.TextCtrl(panel)
        hbox_shift.Add(lbl_shift, flag=wx.RIGHT, border=8)
        hbox_shift.Add(self.shift_input, proportion=1)
        vbox.Add(hbox_shift, flag=wx.EXPAND | wx.ALL, border=10)

        # Checkbox para desencriptar
        self.decrypt_checkbox = wx.CheckBox(panel, label="Desencriptar")
        vbox.Add(self.decrypt_checkbox, flag=wx.ALL, border=10)

        # Botão para processar
        self.process_button = wx.Button(panel, label="Processar")
        self.process_button.Bind(wx.EVT_BUTTON, self.process_text)
        vbox.Add(self.process_button, flag=wx.ALIGN_CENTER | wx.ALL, border=10)

        # Label para o resultado
        self.result_label = wx.StaticText(panel, label="Resultado: ")
        vbox.Add(self.result_label, flag=wx.ALIGN_CENTER | wx.ALL, border=10)

        panel.SetSizer(vbox)

    def process_text(self, event):
        try:
            text = self.text_input.GetValue()
            shift = int(self.shift_input.GetValue())
            decrypt = self.decrypt_checkbox.GetValue()

            if not text:
                raise ValueError("O texto não pode estar vazio.")

            normalized_text = normalize_text(text)
            result = caesar_cipher(normalized_text, shift, decrypt)
            self.result_label.SetLabel(f"Resultado: {result}")

        except ValueError as ve:
            error_message = f"Erro de entrada: {ve}"
            wx.MessageBox(error_message, "Erro", wx.OK | wx.ICON_ERROR)
            log_error(error_message)
        except Exception as e:
            error_message = f"Erro inesperado: {str(e)}"
            wx.MessageBox(error_message, "Erro", wx.OK | wx.ICON_ERROR)
            log_error(error_message)

# Inicialização da aplicação
if __name__ == '__main__':
    app = wx.App()
    frame = CaesarCipherApp()
    frame.Show()
    app.MainLoop()
