# Streamlit app for the project
import streamlit as st
# Model
import joblib
# Load Model

# Pandas
import pandas as pd

# Matplotlib
import matplotlib.pyplot as plt

# Audio recorder streamlit
from audio_recorder_streamlit import audio_recorder

# Audio class
from Audio import Audio

# Os to get the path
import os

model = joblib.load('model/classifier_v2.pkl')

def main():
    options = ['Classificar áudio', 'Sobre']
    page_options = st.sidebar.selectbox('Escolha uma opção', options)
    
    if page_options == 'Sobre':
        homepage()
    if page_options == 'Classificar áudio':
        classify_audio()
                
def homepage():
    st.markdown('''
                Dados:  
                [Suicide Rates Overview 1985 to 2016](https://www.kaggle.com/datasets/russellyates88/suicide-rates-overview-1985-to-2016?resource=download)  

                [Suicide and Depression Detection](https://www.kaggle.com/datasets/nikhileswarkomati/suicide-watch)  

                Referências:  

                https://www.kaggle.com/code/fthdmirr/suicide-rates-and-possible-causes  
                https://www.kaggle.com/code/spidy20/suicide-data-visualization-beginner-guide  
                https://www.kaggle.com/code/antonaks/suicide-attempt-prediction-foreveralone-dataset/data  
                ''')
    
def classify_audio():
    
    st.title('Classifica pelo áudio se a pessoa irá cometer suicídio')
    audio_bytes = audio_recorder()
    
    if audio_bytes:
        
        audio = Audio( audio_name = "audio.mp3", audio_bytes= audio_bytes)
        # Get audio from audio_recorder and save
        audio.write_audio_to_mp3()
        # Convert the audio into text
        audio.get_audio_return_text()
        # Translated Text
        text_tranlated_to_english = audio.translate_audio()
        # Make prediction with the audio -> text passed
        prediction = model.predict_proba([text_tranlated_to_english])
        
        non_suicide = round(prediction[0][0]*100,2)
        suicide = round(prediction[0][1]*100, 2)

        lst = [['Não Suicídio', non_suicide], ['Suicídio', suicide]]
        
        df = pd.DataFrame(lst, columns =['taxa','valor'])
        
        st.title('Previsão do modelo:')
        st.markdown(f"""
                    
                    
                     Taxa de NÃO suicídio: {non_suicide} %  
                     
                     Taxa de suicício: {suicide} %
                    """)
        fig, ax = plt.subplots()
        plt.bar(df['taxa'], df['valor'])
        plt.title('Taxa por valor')
        plt.xlabel('Taxa')
        plt.ylabel('Valores')
        plt.xticks(df['taxa'], df['taxa'])
        st.pyplot(fig)
        
if __name__ == '__main__':
    main()
