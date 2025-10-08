nome = input("Digite o sue nome:")
print(nome.upper())
!pip install docling "pysentimiento[pt]" matplotlib wordcloud nltk
#IMPORTANDO BIBLIOTECAS IMPORTANTES
import re
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
from docling.document_converter import DocumentConverter
from pysentimiento import create_analyzer
from wordcloud import WordCloud
import nltk
from nltk.corpus import stopwords


try:
    stopwords.words('portuguese')
except LookupError:
    nltk.download('stopwords')
    nltk.download('punkt')

#COLOQUE O NOME DO ARQUIVO
caminho_pdf_str = input("digite o nome do arquivo:")

caminho_pdf = Path(caminho_pdf_str)

print(f"Processando o arquivo: {caminho_pdf.name}")

converter = DocumentConverter()
result = converter.convert(caminho_pdf)
texto_bruto = result.document.export_to_text()

nome_presidente = caminho_pdf.stem.replace("posse ", "").title()

#CRIANDO GRÁFICO
emotion_analyzer = create_analyzer(task="emotion", lang="pt")
resultado_analise = emotion_analyzer.predict(texto_bruto)
probabilidades_emocoes = resultado_analise.probas

print("Probabilidades das Emoções")
for emocao, prob in sorted(
    probabilidades_emocoes.items(), key=lambda item: item[1], reverse=True
):
    print(f"{emocao.capitalize():<10}: {prob:.4f}")
#FORMATANDO O GRÁFICO
top_7_emocoes = dict(
    sorted(
        probabilidades_emocoes.items(),
        key=lambda item: item[1],
        reverse=True,
    )[:7]
)

cores = cm.viridis(np.linspace(0, 1, len(top_7_emocoes)))

plt.figure(figsize=(12, 7))

bars = plt.bar(
    top_7_emocoes.keys(),
    top_7_emocoes.values(),
    color=cores,  # APLICA A PALETA DE CORES
)
plt.title(
    f"Análise de Emoções - {nome_presidente}",
    fontsize=16,
    fontweight='bold',
)
plt.ylabel("Probabilidade (Score 0-1)", fontsize=12)
plt.xticks(rotation=45, ha="right", fontsize=11)
plt.yticks(fontsize=10)
plt.ylim(0, max(top_7_emocoes.values()) * 1.15)

plt.bar_label(bars, fmt='%.3f', padding=3, fontsize=10)

plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()

#CRIANDO NUVEM DE PALAVRAS
print("Gerando nuvem de palavras")
stop_words_pt = set(stopwords.words('portuguese'))
texto_processado = texto_bruto.lower()
texto_processado = re.sub(
    r'[^a-záàâãéèêíïóôõöúçñ\s]', '', texto_processado
)
palavras = [
    p
    for p in texto_processado.split()
    if p not in stop_words_pt and len(p) > 2
]
texto_limpo = ' '.join(palavras)

#FORMATANDO A NUVEM DE PALAVRAS
if texto_limpo:
    wordcloud = WordCloud(
        width=1200,
        height=600,
        background_color='white',
        colormap='viridis',
        max_words=50,
    ).generate(texto_limpo)
    plt.figure(figsize=(15, 8))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title(
        f'Nuvem de Palavras - Discurso de {nome_presidente}', fontsize=16
    )
    plt.show()

print("\nAnálise concluída.")
