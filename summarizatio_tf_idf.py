# Run these in terminal
# ! pip install SpeechRecognition
# ! pip install pydub
# ! pip install google-cloud-speech
# ! pip install protobuf
# ! pip install google-cloud-translate
# ! pip install googletrans==3.1.0a0
# ! pip install nltk


import nltk
import os
import re
import math
import operator
from nltk.stem import WordNetLemmatizer as wordlemmatizer
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize,word_tokenize
import speech_recognition as sr 
import speech_recognition as sr 
import os 
from pydub import AudioSegment
from pydub.silence import split_on_silence
import googletrans
import re
import nltk
from nltk import word_tokenize,sent_tokenize
from string import punctuation
from heapq import nlargest
wn = nltk.WordNetLemmatizer()
nltk.download('omw-1.4')
nltk.download('wordnet')
nltk.download('punkt')
nltk.download('stopwords')
stopwords = nltk.corpus.stopwords.words('english')
nltk.download('averaged_perceptron_tagger')


def Story_Summarizer(path, des_language, input_user):
  def lemmatize_words(words):
      lemmatized_words = []
      for word in words:
        lemmatized_words.append(wn.lemmatize(word))
      return lemmatized_words
  
  def stem_words(words):
      stemmed_words = []
      for word in words:
        stemmed_words.append(stemmed_words.stem(word))
      return stemmed_words
  def remove_special_characters(text):
      regex = r'[^a-zA-Z0-9\s]'
      text = re.sub(regex,'',text)
      return text
  def freq(words):
      words = [word.lower() for word in words]
      dict_freq = {}
      words_unique = []
      for word in words:
        if word not in words_unique:
            words_unique.append(word)
      for word in words_unique:
        dict_freq[word] = words.count(word)
      return dict_freq
  def pos_tagging(text):
      pos_tag = nltk.pos_tag(text.split())
      pos_tagged_noun_verb = []
      for word,tag in pos_tag:
          if tag == "NN" or tag == "NNP" or tag == "NNS" or tag == "VB" or tag == "VBD" or tag == "VBG" or tag == "VBN" or tag == "VBP" or tag == "VBZ":
              pos_tagged_noun_verb.append(word)
      return pos_tagged_noun_verb
  def tf_score(word,sentence):
      freq_sum = 0
      word_frequency_in_sentence = 0
      len_sentence = len(sentence)
      for word_in_sentence in sentence.split():
          if word == word_in_sentence:
              word_frequency_in_sentence = word_frequency_in_sentence + 1
      tf =  word_frequency_in_sentence/ len_sentence
      return tf
  def idf_score(no_of_sentences,word,sentences):
      no_of_sentence_containing_word = 0
      for sentence in sentences:
          sentence = remove_special_characters(str(sentence))
          sentence = re.sub(r'\d+', '', sentence)
          sentence = sentence.split()
          sentence = [word for word in sentence if word.lower() not in stopwords and len(word)>1]
          sentence = [word.lower() for word in sentence]
          sentence = [wn.lemmatize(word) for word in sentence]
          if word in sentence:
              no_of_sentence_containing_word = no_of_sentence_containing_word + 1
      idf = math.log10(no_of_sentences/no_of_sentence_containing_word)
      return idf
  def tf_idf_score(tf,idf):
      return tf*idf
  def word_tfidf(dict_freq,word,sentences,sentence):
      word_tfidf = []
      tf = tf_score(word,sentence)
      idf = idf_score(len(sentences),word,sentences)
      tf_idf = tf_idf_score(tf,idf)
      return tf_idf
  def sentence_importance(sentence,dict_freq,sentences):
      sentence_score = 0
      sentence = remove_special_characters(str(sentence)) 
      sentence = re.sub(r'\d+', '', sentence)
      pos_tagged_sentence = [] 
      no_of_sentences = len(sentences)
      pos_tagged_sentence = pos_tagging(sentence)
      for word in pos_tagged_sentence:
            if word.lower() not in stopwords and word not in stopwords and len(word)>1: 
                  word = word.lower()
                  word = wordlemmatizer().lemmatize(word)
                  sentence_score = sentence_score + word_tfidf(dict_freq,word,sentences,sentence)
      return sentence_score



  r = sr.Recognizer()
  translator = googletrans.Translator()



  sound = AudioSegment.from_wav(path)  
  chunks = split_on_silence(sound,
      min_silence_len = 500,
      silence_thresh = sound.dBFS-14,
      keep_silence = 500,
  )
  folder_name = "audio-chunks"

  if not os.path.isdir(folder_name):
    os.mkdir(folder_name)

  I_L_whole_text = ""
  text = ""

  for i, audio_chunk in enumerate(chunks, start=1):
    chunk_filename = os.path.join(folder_name, f"chunk{i}.wav")
    audio_chunk.export(chunk_filename, format="wav")
    with sr.AudioFile(chunk_filename) as source:
      audio_listened = r.record(source)
      try:
        speech_text = r.recognize_google(audio_listened, language = des_language)
      except sr.UnknownValueError as e:
        continue
      else:
        speech_text = f"{speech_text.capitalize()}. "
        I_L_whole_text += speech_text
        translated_text = translator.translate(speech_text, lang_tgt = 'en')
        translated_text = str(translated_text.text)
        text += translated_text
        

  tokenized_sentence = nltk.sent_tokenize(text)
  # tokenized_sentence
  tokenized_sentence = text.split('.')
  # # tokenized_sentence
  text = re.sub(r'\d+', '', text)
  tokenized_words_with_stopwords = nltk.word_tokenize(text)
  tokenized_words = [word for word in tokenized_words_with_stopwords if word not in stopwords]
  tokenized_words = [word for word in tokenized_words if len(word) > 1]
  tokenized_words = [word.lower() for word in tokenized_words]
  tokenized_words = lemmatize_words(tokenized_words)
  word_freq = freq(tokenized_words)
  no_of_sentences = int((input_user * len(tokenized_sentence))/100)
  c = 1
  sentence_with_importance = {}
  for sent in tokenized_sentence:
      sentenceimp = sentence_importance(sent,word_freq,tokenized_sentence)
      sentence_with_importance[c] = sentenceimp
      c = c+1
  sentence_with_importance = sorted(sentence_with_importance.items(), key=operator.itemgetter(1),reverse=True)
  cnt = 0
  summary = []
  sentence_no = []
  for word_prob in sentence_with_importance:
      if cnt < no_of_sentences:
          sentence_no.append(word_prob[0])
          cnt = cnt+1
      else:
        break
  sentence_no.sort()
  cnt = 1
  for sentence in tokenized_sentence:
      if cnt in sentence_no:
        summary.append(sentence)
      cnt = cnt+1
  summary = ". ".join(summary)
  #Translated Summary
  translator = googletrans.Translator()
  translation = translator.translate(summary, dest = des_language)
  summary_I_L = translation.text
  return I_L_whole_text, len(I_L_whole_text.split(" ")), summary_I_L, len(summary_I_L.split(" ")), text, len(text.split(" ")), summary, len(summary.split(" "))
