import unicodedata
import string

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

# Função principal para solicitar entrada e processar o texto
def main():
    print("Cifra de César - Modo de Texto")
    
    texto = input("Digite o texto a ser cifrado: ")
    deslocamento = int(input("Digite o valor do deslocamento (de 1 a 26): "))
    
    # Normaliza o texto e aplica a cifra
    texto_normalizado = normalizar_texto(texto)
    texto_cifrado = cifra_cesar(texto_normalizado, deslocamento)
    
    print("\nTexto original:", texto)
    print("Texto cifrado:", texto_cifrado)

if __name__ == "__main__":
    main()
