from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem import PorterStemmer, SnowballStemmer, WordNetLemmatizer
from nltk import pos_tag
from nltk.corpus import wordnet
from nltk.corpus import stopwords
import string 
import unicodedata
import pandas as pd
import re

ETAPAS = ['original', 'normalizado', 'sin_stopwords', 'stem_lema']

class NLPTextCleaningPipeline:
    def __init__(self, idioma='spanish',
                 opciones_normalizar={"urls","correos","menciones","hashtags","numeros","emojis","puntuacion","espacios"},
                 remover_acentos=True, remover_stopwords=True,
                 normalizar_unicode=True, metodo_stem='snowball'):
        self.idioma = idioma
        self.stopwords = set(stopwords.words('spanish' if idioma == 'spanish' else 'english'))
        self.lenguaje_stem = idioma if idioma in SnowballStemmer.languages else 'english'
        self.stemmer = SnowballStemmer(self.lenguaje_stem)
        self.lematizer = WordNetLemmatizer()
        self.metodo = metodo_stem
        self.opciones_a_normalizar = opciones_normalizar
        self.remover_acentos = remover_acentos
        self.remover_stopwords = remover_stopwords

    # ---------- Etapas individuales ----------
    # -----------------------------------------
    
    def normalizar(self, texto):
        if self.opciones_a_normalizar is None:
            self.opciones_a_normalizar = {"urls", "correos", "menciones", "hashtags",
                                          "numeros", "emojis", "puntuacion", "espacios"}
        if "urls"       in self.opciones_a_normalizar: texto = re.sub(r'https?://\S+', '', texto)
        if "correos"    in self.opciones_a_normalizar: texto = re.sub(r'[\w.]+@[\w.]+\.[a-zA-Z]{2,}', '', texto)
        if "menciones"  in self.opciones_a_normalizar: texto = re.sub(r'@\w+', '', texto)
        if "hashtags"   in self.opciones_a_normalizar: texto = re.sub(r'#\w+', '', texto)
        if "numeros"    in self.opciones_a_normalizar: texto = re.sub(r'\S*\d\S*', '', texto)
        if "emojis"     in self.opciones_a_normalizar: texto = re.sub(r'[^\x00-\x7Fáéíóúüñ¡¿ÁÉÍÓÚÜÑa-zA-Z \n.,!?]', '', texto)
        if "puntuacion" in self.opciones_a_normalizar: texto = re.sub(r'[^\w\sáéíóúüñÁÉÍÓÚÜÑ]', ' ', texto, flags=re.UNICODE)
        if "espacios"   in self.opciones_a_normalizar: texto = re.sub(r'\s+', ' ', texto).strip()
        return texto.lower()

    def quitar_acentos(self, texto):
        nfkd = unicodedata.normalize('NFKD', texto)
        return ''.join(c for c in nfkd if not unicodedata.combining(c))

    def tokenizar(self, texto):
        # Tokeniza el texto YA normalizado: conserva solo tokens alfabéticos en minúscula
        return [w.lower() for w in texto.split() if w.isalpha()]

    def quitar_stopwords(self, tokens):
        return [t for t in tokens if t not in self.stopwords]

    def stemmeing(self, tokens):
        if self.metodo == 'porter':
            return [PorterStemmer().stem(t) for t in tokens]
        elif self.metodo == 'snowball':
            return [self.stemmer.stem(t) for t in tokens]
        else:
            return tokens

    def get_wn_pos(self, pos):
        # pos_tag devuelve etiquetas como 'VBD', 'NN', 'JJ'... usamos la primera letra
        inicial = pos[0] if pos else 'N'
        if inicial == 'V': return wordnet.VERB
        elif inicial == 'N': return wordnet.NOUN
        elif inicial == 'J': return wordnet.ADJ
        elif inicial == 'R': return wordnet.ADV
        else: return wordnet.NOUN

    def lematizar(self, texto):
        # Devuelve tuplas (token, POS, lema) — solo tiene sentido en inglés (WordNet)
        tokens = word_tokenize(texto.lower(), language=self.idioma)
        tagged = pos_tag(tokens)
        return [(t, tag, self.lematizer.lemmatize(t, pos=self.get_wn_pos(tag))) for t, tag in tagged]

    def lematizar_tokens(self, tokens):
        # Lematiza una lista de tokens y devuelve solo los lemas
        tagged = pos_tag(tokens)
        return [self.lematizer.lemmatize(t, pos=self.get_wn_pos(tag)) for t, tag in tagged]

    # ---------- Vocabulario por etapa ----------
    # -------------------------------------------
    def vocabulario_por_etapa(self, textos, metodo_final='stemming'):
        vocab = {etapa: set() for etapa in ETAPAS}
        for texto in textos:
            etapas = self.procesar(texto, metodo_final=metodo_final)
            for etapa in ETAPAS:
                vocab[etapa].update(etapas[etapa])
        tamanos = {etapa: len(vocab[etapa]) for etapa in ETAPAS}
        return tamanos, vocab


    # ---------- Pipeline integrado ----------
    # ----------------------------------------

    def procesar(self, texto, metodo_final='stemming'):
        """Ejecuta el pipeline completo y devuelve los tokens en cada etapa.
        metodo_final: 'stemming' o 'lematizacion'."""
        etapas = {}
        
        # 0. Texto original (tokenización simple, sin limpiar)
        etapas['original'] = [w.lower() for w in re.findall(r'\w+', texto, flags=re.UNICODE)]
        
        # 1. Normalización
        texto_norm = self.normalizar(texto)
        
        # 2. Tokenización
        tokens = self.tokenizar(texto_norm)
        etapas['normalizado'] = tokens
        
        # 3. Eliminación de stopwords  (se hace antes de quitar acentos para que coincidan)
        if self.remover_stopwords:
            tokens = self.quitar_stopwords(tokens)
        etapas['sin_stopwords'] = tokens        

        # 4. Quitar acentos (opcional)
        if self.remover_acentos:
            tokens = [self.quitar_acentos(t) for t in tokens]
    
        # 5. Stemming o Lematización
        if metodo_final == 'lematizacion':
            tokens = self.lematizar_tokens(tokens)
        else:
            tokens = self.stemmeing(tokens)
        etapas['stem_lema'] = tokens

        return etapas

    def preprocesar(self, texto, metodo_final='stemming'):
        # Devuelve la lista final de tokens limpios
        return self.procesar(texto, metodo_final)['stem_lema']