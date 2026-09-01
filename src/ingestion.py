import re
import pdfplumber

with pdfplumber.open("bulas/ARIPIPRAZOL-bula_1788114599293.pdf") as pdf:  
    texto_completo = ""
    for pagina in pdf.pages:
        texto_completo += pagina.extract_text() + "\n"  

padrao_rodape = r'\w+\s*–\s*VP\s*\d+'  # Padrão para identificar o rodapé
texto_limpo = re.sub(padrao_rodape, '', texto_completo)  # Remove o rodapé do texto completo

padrao = r'(^\d+\.\s+[A-ZÁ-Ú].*?\?)'  # Padrão para identificar títulos de seções (ex: "1. INDICAÇÕES?")
resultados = re.split(padrao, texto_limpo, flags=re.MULTILINE | re.DOTALL)  # Divide o texto em seções com base nos títulos encontrados
titulos = resultados[1::2]  # Seleciona os títulos das seções (índices ímpares)
conteudos = resultados[2::2]  # Seleciona os conteúdos das seções (índices pares)

chunks = [
    {"titulo": titulo.strip(), "conteudo": conteudo.strip()}
    for titulo, conteudo in zip(titulos, conteudos)
]
print(chunks)
