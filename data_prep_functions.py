import pandas as pd
import numpy as np
import unidecode
import re
import spacy
from nltk.corpus import stopwords
from happytransformer import HappyTextToText
from happytransformer import TTSettings
from langdetect import detect

happy_tt = HappyTextToText("MARIAN", "Helsinki-NLP/opus-mt-fr-en")
args = TTSettings(min_length=2)
nlp_en = spacy.load('en_core_web_md')

def columns_treatment(df):
    df = df.iloc[:,[0,1,3]]
    df = df.rename(columns={'Objet':'objet','Corps':'corps', 'De: (adresse)':'adresse'})
    return df

def remove_https(corps):

    text_file = open(r'corps.txt', 'w',  encoding="utf-8")
    text_file.write(corps)
    text_file.close()

        
    final_text_file = open(r'final_corps.txt', 'w',  encoding="utf-8")
    reading_text_file = open(r'corps.txt', 'r',  encoding="utf-8")
    for line in reading_text_file:
        if "http" not in line:
            final_text_file.write(line)
            
    final_text_file.close()
    reading_text_file.close()

    with open('final_corps.txt', 'r', encoding="utf-8") as file:
        return file.read()

def text_cleaning(text):
    text = str(text)
    text = unidecode.unidecode(text)
    text = re.sub(r"""[.,(/"'?:)!;\\]""", '', text)
    text = re.sub(r"""[0-9]+""", '', text) #removing numbers
    text = re.sub(r"""-""", ' ', text) #uniquement - pour les mots du style "allez-vous"
    text = re.sub(r"""_""", ' ', text) 
    text = re.sub('\s+', ' ', text)
    text = re.sub(r'\<.*?\>', ' ', text)
    return text

def text_translation(text):
    try:
        lang = detect(text)
    except:
        lang = "error"
    if lang == "fr":
        #translate
        final_trans_text = ""
        ran = round(len(text.split())/50)
        if ran == 0:
            trans_text = happy_tt.generate_text(text, args=args)
            final_trans_text = trans_text.text
        else:
            for i in range(ran):
                piece_of_text = ' '.join(text.split()[i*50:50+(i*50)])                
                trans_text = happy_tt.generate_text(piece_of_text, args=args)
                final_trans_text = final_trans_text + " " + trans_text.text
        
    elif lang == "en":
        final_trans_text = text
    else:
        #classify the email as autre
        final_trans_text = text
    return final_trans_text

def stop_words_english(text):
    stop_words = stopwords.words('english')
    text = [word for word in text.split() if ((word not in stop_words) and (len(word)>1))]
    
    return text

def lemmatization(nlp, texte):
    i = 0
    # On regarde chaque mot dans le texte
    # Chaque mot a le numéro i
    for mot in texte:
        # on va lemmatizer
        doc = nlp(mot)
        for token in doc:
            texte[i] = token.lemma_.lower()
            
        i += 1
    
            
    return texte