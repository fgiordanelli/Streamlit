import streamlit as st
import pandas as pd
import re
import base64

st.set_page_config(layout="wide")

pd.set_option('display.max_colwidth',1000)
pd.set_option('display.max_rows',10000)

def regex(quero=[], nao_quero=[],quero_completo = [], nao_quero_completo = []):
    guardar1 = []
    guardar2 = []

    backslash = r"\b"

    for i in quero:
        guardar1.append(f'(?=.*{i})')

    for j in nao_quero:
        guardar2.append(f'(?!.*{j})')


    imprimir = ''.join(guardar1 + guardar2)
    return imprimir


#uploaded_file = st.sidebar.file_uploader("Choose a file")
#if uploaded_file is not None:
#df = pd.read_csv(uploaded_file)


if 'df' not in st.session_state:
    st.session_state.df = pd.read_csv('/home/logcomex/Imagens/df2.csv')

st.header('Produto')
user_produto = st.selectbox('Filtrar produto',st.session_state.df['produto'].drop_duplicates().tolist())

myslot = st.empty()

myslot.table(st.session_state.df[st.session_state.df['produto'].isin([user_produto])].head(10000))


st.sidebar.header('Quero')
user_input = st.sidebar.text_input("Palavra 1")

st.sidebar.header('Não quero')
user_input2 = st.sidebar.text_input("Palavra 2","&&&&&")

     
df_filtrado = st.session_state.df[st.session_state.df['desc_prodt'].apply(lambda x: len(re.findall(rf"(?mi)^{regex(quero = user_input.split(' '),nao_quero = user_input2.split(' '))}.*",str(x))) > 0)]
        
    
st.sidebar.header('Selecionar')
opcoes_selecionar = df_filtrado['predito_linha'].drop_duplicates().tolist()
user_input3 = st.sidebar.multiselect("Categoria",opcoes_selecionar)


if len(user_input) > 0  and len(user_input3) > 0:
    myslot.empty()


st.sidebar.header('Atualizar')
categorias = st.sidebar.selectbox('Linha/Familia/Subfamilia',user_input3+st.session_state.df['predito_linha'].drop_duplicates().tolist())



my_slot1 = st.empty()



my_slot1.table(st.session_state.df[st.session_state.df['desc_prodt'].apply(lambda x: len(re.findall(rf"(?mi)^{regex(quero = user_input.split(' '),nao_quero = user_input2.split(' '))}.*",str(x))) > 0) & st.session_state.df['predito_linha'].isin(user_input3)].head(10000))


if st.sidebar.button("Atualizar!"):
    my_slot1.empty()

    st.session_state.df[st.session_state.df['desc_prodt'].apply(lambda x: len(re.findall(rf"(?mi)^{regex(quero = user_input.split(' '),nao_quero = user_input2.split(' '))}.*",str(x))) > 0) & st.session_state.df['predito_linha'].isin(user_input3)] = st.session_state.df[st.session_state.df['desc_prodt'].apply(lambda x: len(re.findall(rf"(?mi)^{regex(quero = user_input.split(' '),nao_quero = user_input2.split(' '))}.*",str(x))) > 0) & st.session_state.df['predito_linha'].isin(user_input3)].assign(predito_linha = categorias)

    st.table(st.session_state.df[st.session_state.df['desc_prodt'].apply(lambda x: len(re.findall(rf"(?mi)^{regex(quero = user_input.split(' '),nao_quero = user_input2.split(' '))}.*",str(x))) > 0) & st.session_state.df['predito_linha'].isin(user_input3)].head(10000))

st.sidebar.header('Fazer Download')       

if st.sidebar.button("Download!"):
    def get_table_download_link_csv(df):
        st.session_state.df[['dsc_linha', 'dsc_familia','dsc_subfamilia']] = st.session_state.df['predito_linha'].str.split('&&&', 2, expand=True)
        csv = st.session_state.df.to_csv().encode()
        b64 = base64.b64encode(csv).decode()
        href = f'<a href="data:file/csv;base64,{b64}" download="captura.csv" target="_blank">Download csv file</a>'
        return href

    st.sidebar.markdown(get_table_download_link_csv(st.session_state.df), unsafe_allow_html=True)

        