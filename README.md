# 🧠 Curso NLP 2026 — Procesamiento Natural del Lenguaje
### ITESO · Maestría en Inteligencia Artificial · ALINNCO

---

## 📋 Descripción del Curso

Curso intensivo de **5 semanas** (10 sesiones, 4 hrs cada una) diseñado para estudiantes
con experiencia en programación Python que quieran dominar el Procesamiento Natural del Lenguaje
desde fundamentos hasta modelos Transformer de última generación.

---

## 🗓 Programa del Curso

| Semana | Sesión | Tema | Duración |
|--------|--------|------|----------|
| 1 | Viernes | Fundamentos de NLP | 4 hrs |
| 1 | Sábado | Herramientas base (NLTK, spaCy) | 4 hrs |
| 2 | Viernes | Transformaciones de texto (Stemming, Lematización) | 4 hrs |
| 2 | Sábado | Limpieza y Normalización | 4 hrs |
| 3 | Viernes | Representaciones clásicas (BoW, TF-IDF) | 4 hrs |
| 3 | Sábado | Word Embeddings (Word2Vec, GloVe, FastText) | 4 hrs |
| 4 | Viernes | Clasificación de texto (Naive Bayes, SVM, LR) | 4 hrs |
| 4 | Sábado | Extracción de información (NER, POS) | 4 hrs |
| 5 | Viernes | Arquitectura Transformer y BERT | 4 hrs |
| 5 | Sábado | Proyecto Final + Demo | 4 hrs |

---

## 📁 Estructura de Carpetas

```
Curso_NLP_2026/
│
├── README.md                          ← Este archivo
├── environment.yml                    ← Entorno conda
├── Recursos.md                        ← Bibliografía y recursos
│
├── Introducción/                      ← Semana 1
│   ├── Semana_1_Viernes_Fundamentos.md
│   ├── Semana_1_Sabado_Herramientas.md
│   └── notebooks/
│       ├── 01_Introduccion_NLP.ipynb
│       └── 02_Herramientas_Base.ipynb
│
├── Módulo_1_Preprocesamiento_y_Representación/    ← Semanas 2-3
│   ├── Semana_2_ParteA_Transformaciones.md
│   ├── Semana_2_Sabado_Limpieza.md
│   ├── Semana_3_ParteB_Representaciones.md
│   ├── Semana_3_Sabado_WordEmbeddings.md
│   └── notebooks/
│       ├── 01_Tokenizacion_Stemming_Lemmatizacion.ipynb
│       ├── 02_Limpieza_Normalizacion.ipynb
│       ├── 03_BoW_TFIDF.ipynb
│       └── 04_Word_Embeddings.ipynb
│
├── Módulo_2_Tareas_Clásicas_de_NLP/               ← Semana 4
│   ├── Semana_4_Viernes_Clasificacion.md
│   ├── Semana_4_Sabado_Extraccion.md
│   └── notebooks/
│       ├── 01_Clasificacion_Texto.ipynb
│       └── 02_NER_POS_Extraccion.ipynb
│
├── Módulo_3_Modelos_de_Lenguaje/                  ← Semana 5
│   ├── Semana_5_Viernes_Transformers.md
│   ├── Semana_5_Sabado_Proyecto_Final.md
│   └── notebooks/
│       ├── 01_Transformers_BERT.ipynb
│       └── 02_Proyecto_Final.ipynb
│
├── Actividades/                       ← Ejercicios evaluados
│   ├── Actividad_1_Fundamentos_NLP.ipynb
│   ├── Actividad_2_Preprocesamiento.ipynb
│   ├── Actividad_3_Representacion_Vectorial.ipynb
│   ├── Actividad_4_Clasificacion_NER.ipynb
│   └── Actividad_5_Transformers_Proyecto.ipynb
│
└── Material_de_Apoyo/                 ← Recursos adicionales
    ├── README.md
    ├── datasets/
    └── snippets/
        └── preprocessing.py
```

---

## ⚙️ Instalación del Entorno

### Prerrequisitos
- Anaconda o Miniconda: https://www.anaconda.com/download
- Git (opcional): https://git-scm.com/

### Pasos

```bash
# 1. Crea el entorno desde el archivo
conda env create -f environment.yml

# 2. Activa el entorno
conda activate nlp_curso_2026

# 3. Descarga modelos de spaCy
python -m spacy download es_core_news_sm
python -m spacy download en_core_web_sm

# 4. Descarga recursos de NLTK
python -c "import nltk; [nltk.download(r) for r in ['punkt','punkt_tab','stopwords','wordnet','movie_reviews','averaged_perceptron_tagger','maxent_ne_chunker','words']]"

# 5. Registra el kernel en Jupyter
python -m ipykernel install --user --name nlp_curso_2026 --display-name "Python (NLP 2026)"

# 6. Inicia JupyterLab
jupyter lab
```

---

## 📊 Evaluación

| Componente | Peso |
|---|---|
| Actividad 1 — Fundamentos y Preprocesamiento | 15% |
| Actividad 2 — Stemming y Lematización | 15% |
| Actividad 3 — Representación Vectorial | 20% |
| Actividad 4 — Clasificación y NER | 20% |
| Actividad 5 — Proyecto Final con Transformer | 30% |

---

## 📚 Material Existente del Curso

Este repositorio se complementa con materiales previos disponibles en el directorio raíz:

| Carpeta | Contenido |
|---|---|
| `../Modulo I/` | Introducción a NLP, manejo de archivos, regex, NLTK/spaCy |
| `../Modulo II/` | Tokenización, stemming, Naive Bayes, regresión logística |
| `../Modulo III/` | Word2Vec, FastText, POS tagging, traducción automática |
| `../Actividades/` | Trabajos entregados por estudiantes (referencia) |
| `../Proyecto/` | Análisis de sentimientos en reseñas de películas |

---

## 👨‍🏫 Instructor

Curso NLP 2026 · ITESO Guadalajara, Jalisco, México
Maestría en Inteligencia Artificial · ALINNCO

---

*Para dudas técnicas de instalación, revisa primero la sección de issues conocidos
al final del archivo `environment.yml`.*
