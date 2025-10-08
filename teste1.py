import streamlit as st

nome = st.text_input("Digite o seu nome:")
if nome: 
    st.write(nome.upper())
    
