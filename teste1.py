import streamlit as st

nome = st.input_box("Digite o seu nome:")
if nome: 
    st.write(nome.upper())
    
