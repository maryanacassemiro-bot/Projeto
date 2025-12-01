import pandas as pd
import numpy as np
import streamlit as st
import random
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Carrega o DataFrame com os artigos do Código Penal
df_artigos = pd.read_csv('artigos_codigo_penal.csv')

# Configuração da página
st.set_page_config(page_icon='⚖️', page_title="Adivinhe o Artigo")

st.title("⚖️ Adivinhe o Artigo do Código Penal!")
st.subheader("Teste seus conhecimentos sobre legislação penal brasileira")

# Sidebar com informações
with st.sidebar:
    st.subheader('Sobre o Jogo')
    st.write('Este jogo foi desenvolvido para testar conhecimentos sobre o Código Penal Brasileiro.')
    st.write('Observe a nuvem de palavras gerada a partir do caput de um artigo e tente adivinhar qual é o número do artigo!')
    st.write(f'Base de dados: {len(df_artigos)} artigos do Código Penal')
    st.caption('Projeto desenvolvido para a disciplina Programação para Advogados')
    st.caption('FGV Direito Rio')

# Define stopwords jurídicas e comuns
def stopwords():
    return set([
        'a', 'o', 'e', 'de', 'da', 'do', 'em', 'um', 'uma', 'os', 'as', 'dos', 'das',
        'na', 'no', 'nas', 'nos', 'por', 'para', 'com', 'sem', 'sob', 'ao', 'aos',
        'à', 'às', 'pelo', 'pela', 'pelos', 'pelas', 'que', 'ou', 'se', 'sua', 'seu',
        'suas', 'seus', 'quem', 'qual', 'quando', 'onde', 'como', 'ser', 'foi', 'é',
        'são', 'estar', 'ter', 'ter', 'pode', 'podem', 'deve', 'devem', 'art', 'artigo',
        'pena', 'código', 'penal', 'lei', 'decreto'
    ])

# Paletas de cores para nuvem de palavras
def cores_diferentes():
    color_palettes = [
        'viridis', 'winter', 'summer', 'prism', 'Blues', 'Oranges',
        'GnBu', 'Purples', 'coolwarm', 'cool', 'hsv', 'magma'
    ]
    return random.choice(color_palettes)

# Gera nuvem de palavras e opções de resposta
def gerar_nuvem_e_opcoes(df):
    artigo = df.sample(1).iloc[0]
    caput = artigo['caput']
    numero_correto = str(artigo['numero_artigo'])
    
    # Gera nuvem de palavras
    wordcloud = WordCloud(
        width=800, 
        height=400, 
        background_color='white', 
        colormap=cores_diferentes(), 
        stopwords=stopwords(),
        max_words=50
    ).generate(caput)
    
    # Seleciona 4 números de artigos diferentes como opções incorretas
    artigos_disponiveis = df[df['numero_artigo'] != artigo['numero_artigo']]['numero_artigo'].unique()
    
    if len(artigos_disponiveis) < 4:
        outros_numeros = artigos_disponiveis.tolist()
    else:
        outros_numeros = np.random.choice(artigos_disponiveis, 4, replace=False).tolist()
    
    # Converte para string e cria lista de opções
    outros_numeros = [str(n) for n in outros_numeros]
    opcoes = outros_numeros + [numero_correto]
    random.shuffle(opcoes)
    
    return wordcloud, numero_correto, opcoes, caput

# Inicializa estados da sessão
if 'wordcloud' not in st.session_state:
    st.session_state.wordcloud = None

if 'rodada' not in st.session_state:
    st.session_state.rodada = 1

if 'pontuacao' not in st.session_state:
    st.session_state.pontuacao = 0

if 'numero_correto' not in st.session_state:
    st.session_state.numero_correto = None

if 'opcoes' not in st.session_state:
    st.session_state.opcoes = None

if 'caput_completo' not in st.session_state:
    st.session_state.caput_completo = None

if 'mostrar_caput' not in st.session_state:
    st.session_state.mostrar_caput = False

# Gera primeira nuvem se necessário
if st.session_state.wordcloud is None:
    st.session_state.wordcloud, st.session_state.numero_correto, st.session_state.opcoes, st.session_state.caput_completo = gerar_nuvem_e_opcoes(df_artigos)

# Jogo principal
if st.session_state.rodada <= 10:
    st.title(f"🎯 Rodada {st.session_state.rodada} de 10")
    st.subheader("Analise a nuvem de palavras e adivinhe o número do artigo:")
    
    # Exibe pontuação atual
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Pontuação", st.session_state.pontuacao)
    with col2:
        st.metric("Rodada", f"{st.session_state.rodada}/10")
    
    # Exibe nuvem de palavras
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(st.session_state.wordcloud, interpolation='bilinear')
    ax.axis('off')
    st.pyplot(fig)
    
    # Opções de resposta
    escolha = st.radio("Qual é o número do artigo?", st.session_state.opcoes, key=f"escolha_{st.session_state.rodada}")
    
    # Botão para mostrar o caput completo (dica)
    if st.button("💡 Ver caput completo (perde 2 pontos)", key=f"dica_{st.session_state.rodada}"):
        st.session_state.mostrar_caput = True
        st.session_state.pontuacao -= 2
    
    if st.session_state.mostrar_caput:
        st.info(f"**Caput do artigo:** {st.session_state.caput_completo}")
    
    # Verificação da resposta
    if st.button("✅ Verificar Resposta", key=f"verificar_{st.session_state.rodada}"):
        if escolha == st.session_state.numero_correto:
            st.success(f"🎉 Parabéns! Você acertou! É o artigo {st.session_state.numero_correto}!")
            st.session_state.pontuacao += 10
            st.info(f"**Caput completo:** {st.session_state.caput_completo}")
        else:
            st.error(f"❌ Resposta incorreta! O artigo correto é o {st.session_state.numero_correto}.")
            st.session_state.pontuacao -= 5
            st.info(f"**Caput completo:** {st.session_state.caput_completo}")
        
        st.session_state.rodada += 1
        st.session_state.mostrar_caput = False
        
        if st.session_state.rodada <= 10:
            st.session_state.wordcloud, st.session_state.numero_correto, st.session_state.opcoes, st.session_state.caput_completo = gerar_nuvem_e_opcoes(df_artigos)
            st.rerun()

else:
    # Fim do jogo
    st.balloons()
    st.title("🏆 Jogo Finalizado!")
    st.subheader(f"Sua pontuação final: {st.session_state.pontuacao} pontos")
    
    if st.session_state.pontuacao >= 70:
        st.success("🌟 Excelente! Você domina o Código Penal!")
    elif st.session_state.pontuacao >= 40:
        st.info("📚 Bom trabalho! Continue estudando!")
    else:
        st.warning("📖 Continue se dedicando aos estudos jurídicos!")
    
    if st.button("🔄 Jogar Novamente"):
        st.session_state.rodada = 1
        st.session_state.pontuacao = 0
        st.session_state.wordcloud = None
        st.session_state.mostrar_caput = False
        st.rerun()
