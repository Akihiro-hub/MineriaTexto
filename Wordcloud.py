import streamlit as st
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
import PyPDF2
import re

# Streamlit UIの設定
st.write("## :blue[Análisis de Texto o Documento por la Inteligencia Artificial]") 
st.write("###### Word Cloud o Nube de Palabras es una representación visual, por la aplicación de la Inteligencia Artificial, de texto donde las palabras más frecuentes o importantes en un conjunto de datos se muestran más grandes y destacadas. Es una herramienta útil para visualizar la importancia relativa de términos dentro de un texto de manera rápida y comprensible.")
st.write("##### :green[Paso 1: Pegue el texto para el análisis o suba un archivo PDF.]")

# テキストエリアとPDFファイルアップロードのオプション
texto = st.text_area("Introduce el texto aquí", "")
pdf_file = st.file_uploader("O sube un archivo PDF", type="pdf")

# 除外したい単語の入力
st.write("##### :green[Paso 2: Note abajo las palabras qie deben excluirse del análisis, si las tiene.]")
col1, col2, col3 = st.columns(3)
with col1:
    exclude_word1 = st.text_input("Palabra a excluir 1", "")
    exclude_word2 = st.text_input("Palabra a excluir 2", "")
with col2:
    exclude_word3 = st.text_input("Palabra a excluir 3", "")
    exclude_word4 = st.text_input("Palabra a excluir 4", "")
with col3:
    exclude_word5 = st.text_input("Palabra a excluir 5", "")
    exclude_word6 = st.text_input("Palabra a excluir 6", "")

# デフォルトで除外する単語のリスト
default_excluded_words = {
    "la", "el", "los", "las", "él", "ella", "en", "de", "del", "un", "que", "soy", "eres", "es", "somos", "son",
    "estoy", "estás", "le", "poder", "hace", "año", "mes", "he", "estado", "había", "años", "meses",
    "está", "estamos", "están", "este", "aquello", "aquella", "esta", "estas", "estos", "cual", "y", "ya", "hay", "a", "al",
    "lo", "desde", "hasta", "hacia", "usted", "tú", "yo", "compartir", "con", "para", "su", "nuestro", "sea", "sean", "esté", "estén", 
    "o", "u", "e", "por", "eso", "foto", "fotos", "local", "reseñas", "más", "mas", "nos", "os", "ser", "estar", "sí", "si", "estuviese", "estuviera",
    "no", "ni", "guide", "hay", "se", "una", "uno", "fuí", "fue", "fuera", "fuese", "hubiera", "estaba", "estaban", "estuve", "estuvo", "estuvieron"
}

# 入力された除外単語をセットに追加
user_excluded_words = {exclude_word1, exclude_word2, exclude_word3, exclude_word4, exclude_word5, exclude_word6}
excluded_words = default_excluded_words.union(user_excluded_words)

if pdf_file:
    # PDFからテキストを抽出
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    texto = ""
    for page in pdf_reader.pages:
        texto += page.extract_text()

if texto:
    # テキストのトークン化と前処理
    words = re.findall(r'\b\w+\b', texto.lower())
    filtered_words = [word for word in words if word not in excluded_words]

    # Word Cloudの作成
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(" ".join(filtered_words))

# 分析ボタンの表示
if st.button("Analizar"):

    # Word Cloudの表示
    st.subheader("Nube de Palabras (Word Cloud)")
    
    fig, ax = plt.subplots()
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis("off")
    st.pyplot(fig)
    
    # 頻出する単語の組み合わせ
    st.subheader("Combinaciones de palabras más comunes")
    bigram_freq = Counter(list(zip(filtered_words[:-1], filtered_words[1:])))
    trigram_freq = Counter(list(zip(filtered_words[:-2], filtered_words[1:-1], filtered_words[2:])))
        
    st.write("Bigrams más comunes:")
    for bigram, freq in bigram_freq.most_common(3):
        st.write(f"{' '.join(bigram)}: {freq}")

    st.write("Trigrams más comunes:")
    for trigram, freq in trigram_freq.most_common(3):
        st.write(f"{' '.join(trigram)}: {freq}")

