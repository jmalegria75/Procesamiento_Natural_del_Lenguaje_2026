from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer, SnowballStemmer, WordNetLemmatizer
from nltk import pos_tag
from nltk.corpus import wordnet, stopwords
import unicodedata, re, pandas as pd

ETAPAS=['original','normalizado','sin_stopwords','stem_lema']

class NLPTextCleaningPipeline:
    def __init__(self, idioma='spanish',
                 opciones_normalizar={"urls","correos","menciones","hashtags","numeros","emojis","puntuacion","espacios"},
                 remover_acentos=True, remover_stopwords=True, normalizar_unicode=True, metodo_stem='snowball'):
        self.idioma = idioma
        self.stopwords = set(stopwords.words('spanish' if idioma=='spanish' else 'english'))
        lenguaje_stem = idioma if idioma in SnowballStemmer.languages else 'english'
        self.stemmer = SnowballStemmer(lenguaje_stem)
        self.lematizer = WordNetLemmatizer()
        self.metodo = metodo_stem
        self.opciones_a_normalizar = opciones_normalizar
        self.remover_acentos = remover_acentos
        self.remover_stopwords = remover_stopwords
    def normalizar(self, texto):
        if "urls" in self.opciones_a_normalizar: texto = re.sub(r'https?://\S+','',texto)
        if "correos" in self.opciones_a_normalizar: texto = re.sub(r'[\w.]+@[\w.]+\.[a-zA-Z]{2,}','',texto)
        if "menciones" in self.opciones_a_normalizar: texto = re.sub(r'@\w+','',texto)
        if "hashtags" in self.opciones_a_normalizar: texto = re.sub(r'#\w+','',texto)
        if "numeros" in self.opciones_a_normalizar: texto = re.sub(r'\S*\d\S*','',texto)
        if "emojis" in self.opciones_a_normalizar: texto = re.sub(r'[^\x00-\x7Fáéíóúüñ¡¿ÁÉÍÓÚÜÑa-zA-Z \n.,!?]','',texto)
        if "puntuacion" in self.opciones_a_normalizar: texto = re.sub(r'[^\w\sáéíóúüñÁÉÍÓÚÜÑ]',' ',texto, flags=re.UNICODE)
        if "espacios" in self.opciones_a_normalizar: texto = re.sub(r'\s+',' ',texto).strip()
        return texto.lower()
    def quitar_acentos(self, texto):
        nfkd = unicodedata.normalize('NFKD', texto)
        return ''.join(c for c in nfkd if not unicodedata.combining(c))
    def tokenizar(self, texto):
        return [w.lower() for w in texto.split() if w.isalpha()]
    def quitar_stopwords(self, tokens):
        return [t for t in tokens if t not in self.stopwords]
    def stemmeing(self, tokens):
        if self.metodo=='porter': return [PorterStemmer().stem(t) for t in tokens]
        elif self.metodo=='snowball': return [self.stemmer.stem(t) for t in tokens]
        return tokens
    def get_wn_pos(self, pos):
        inicial = pos[0] if pos else 'N'
        return {'V':wordnet.VERB,'N':wordnet.NOUN,'J':wordnet.ADJ,'R':wordnet.ADV}.get(inicial, wordnet.NOUN)
    def lematizar_tokens(self, tokens):
        tagged = pos_tag(tokens)
        return [self.lematizer.lemmatize(t, pos=self.get_wn_pos(tag)) for t,tag in tagged]
    def procesar(self, texto, metodo_final='stemming'):
        etapas={}
        etapas['original']=[w.lower() for w in re.findall(r'\w+',texto, flags=re.UNICODE)]
        tokens=self.tokenizar(self.normalizar(texto))
        etapas['normalizado']=tokens
        if self.remover_stopwords: tokens=self.quitar_stopwords(tokens)
        etapas['sin_stopwords']=tokens
        if self.remover_acentos: tokens=[self.quitar_acentos(t) for t in tokens]
        etapas['stem_lema']=self.lematizar_tokens(tokens) if metodo_final=='lematizacion' else self.stemmeing(tokens)
        return etapas

def vocabulario(clean, textos, m='stemming'):
    v={e:set() for e in ETAPAS}
    for t in textos:
        et=clean.procesar(t, m)
        for e in ETAPAS: v[e].update(et[e])
    return {e:len(v[e]) for e in ETAPAS}

textos_en=['Natural language processing systems are becoming increasingly sophisticated.',
 'Deep learning models have revolutionized text classification and generation tasks.',
 'Tokenization is the fundamental first step in any NLP preprocessing pipeline.',
 'Researchers are studying computational approaches to human language understanding.']
textos_es=['Apple presentó su nuevo chip M4 con IA integrada. La presentación fue en WWDC 2026 #Apple #M4',
 'Google lanzó Gemini Ultra, su modelo más poderoso. Supera a GPT-4 en benchmarks https://blog.google.com',
 'El peso mexicano se fortalece frente al dólar: $17.50 por USD en mercados internacionales']


print('EN lematizacion:', vocabulario(NLPTextCleaningPipeline('english'), textos_en, 'lematizacion'))
print('ES stemming:', vocabulario(NLPTextCleaningPipeline('spanish'), textos_es, 'stemming'))
print('Demo EN procesar:', NLPTextCleaningPipeline('english').procesar(textos_en[0],'lematizacion'))
print('OK')
