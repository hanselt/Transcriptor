markdown
Copy
# Transcripción Automática de Videos

Aplicación para transcribir videos a texto usando Whisper (para transcripción) y modelos LLM (para corrección y mejora del texto).

## 🚀 Características principales

- Conversión de video a audio
- Transcripción automática usando Whisper
- Corrección y mejora del texto con LLMs
- Interfaz web moderna (Vue.js)
- API REST (Flask)
- Soporte para múltiples formatos de video

## 📦 Dependencias del proyecto

### Backend (Python/Flask)

import os
from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, END
from groq import Groq
from dotenv import load_dotenv
from moviepy.editor import VideoFileClip
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask import send_file
import io
from werkzeug.utils import secure_filename
from pathlib import Path
import time
Frontend (Vue.js)
Vue 3

## Vue Router

Axios

Element Plus (opcional)

## 🛠️ Instalación
Requisitos previos
Python 3.9+

Node.js 16+

FFmpeg (para procesamiento de video)

## Git

1. Clonar el repositorio
bash

git clone https://github.com/tu-usuario/tu-repositorio.git
cd tu-repositorio
2. Configurar backend
Instalar dependencias de Python
bash

pip install -r requirements.txt
Archivo requirements.txt

flask==3.0.2
flask-cors==4.0.0
python-dotenv==1.0.0
moviepy==1.0.3
groq==0.3.0
langgraph==0.0.12
openai-whisper==20231117
werkzeug==3.0.1
Variables de entorno (.env)
Crea un archivo .env en la raíz del proyecto con:

init
##  .env config

GROQ_API_KEY=tu_api_key_de_groq
UPLOAD_FOLDER=./uploads
ALLOWED_EXTENSIONS=mp4,mov,avi,mkv
3. Configurar frontend
bash

cd frontend
npm install
4. Ejecutar el proyecto
Iniciar backend (desde la raíz del proyecto)
bash

python app.py
Iniciar frontend (desde /frontend)
bash

npm run dev
