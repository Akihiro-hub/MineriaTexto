import streamlit as st
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
import nltk
from nltk.corpus import stopwords
from nltk import bigrams, trigrams
import PyPDF2

# Streamlit UIの設定
st.write("### :blue[Análisis de Texto o Documento]") 
st.write("###### Minería de Texto con la Inteligencia Artificial")
st.write("Pegue el texto para el análisis o suba un archivo PDF.")

# テキストエリアとPDFファイルアップロードのオプション
texto = st.text_area("Introduce el texto aquí", "")
pdf_file = st.file_uploader("O sube un archivo PDF", type="pdf")

# 除外したい単語の入力
col1, col2, col3 = st.columns(3)
with col1:
    exclude_word1 = st.text_input("Palabra a excluir 1", "")
    exclude_word2 = st.text_input("Palabra a excluir 2", "")
with col2:
    exclude_word4 = st.text_input("Palabra a excluir 3", "")
    exclude_word5 = st.text_input("Palabra a excluir 4", "")
with col3:
    exclude_word7 = st.text_input("Palabra a excluir 5", "")
    exclude_word8 = st.text_input("Palabra a excluir 6", "")

excluded_words = {exclude_word1, exclude_word2, exclude_word3, exclude_word4, exclude_word5, exclude_word6}

if pdf_file:
    # PDFからテキストを抽出
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    texto = ""
    for page in pdf_reader.pages:
        texto += page.extract_text()

if texto:
    # テキストのトークン化と前処理
    words = nltk.word_tokenize(texto.lower())
    words = [word for word in words if word.isalpha()]
    filtered_words = [word for word in words if word not in spanish_stopwords and word not in english_stopwords and word not in ser_estar_words and word not in excluded_words]

    # 頻出単語のカウント
    word_freq = Counter(filtered_words)
    most_common_words = word_freq.most_common(10)

    # Word Cloudの作成
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(" ".join(filtered_words))

    # 分析ボタンの表示
    if st.button("Analizar"):

        # Word Cloudの表示
        st.subheader("Nube de Palabras (Word Cloud)")
        st.write("###### Un Word Cloud o nube de palabras es una representación visual de texto donde las palabras más frecuentes o importantes en un conjunto de datos se muestran más grandes y destacadas. Es una herramienta útil para visualizar la importancia relativa de términos dentro de un texto de manera rápida y comprensible.")
        fig, ax = plt.subplots()
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.axis("off")
        st.pyplot(fig)

        # 頻出単語のグラフ表示
        st.subheader("Frecuencia de las 10 palabras más comunes")
        word_freq_dict = dict(most_common_words)
        sns.barplot(x=list(word_freq_dict.values()), y=list(word_freq_dict.keys()), orient='h')
        plt.xlabel("Frecuencia")
        plt.ylabel("Palabra")
        st.pyplot(plt)

        # 頻出する単語の組み合わせ
        st.subheader("Combinaciones de palabras más comunes")
        bigram_freq = Counter(bigrams(filtered_words))
        trigram_freq = Counter(trigrams(filtered_words))
        
        st.write("Bigrams más comunes:")
        for bigram, freq in bigram_freq.most_common(3):
            st.write(f"{' '.join(bigram)}: {freq}")

        st.write("Trigrams más comunes:")
        for trigram, freq in trigram_freq.most_common(3):
            st.write(f"{' '.join(trigram)}: {freq}")
