from flask import Flask, request, jsonify
from flask_cors import CORS  # Para evitar problemas CORS
from flask import send_file
import io
import os
from services.transcriber import VideoTranscriber
from services.transcriber import convertir_video_a_audio
from werkzeug.utils import secure_filename
from dotenv import load_dotenv  # Para variables de entor
from pathlib import Path
import time

# Cargar variables .env
load_dotenv()

app = Flask(__name__)
CORS(app)  # Habilita CORS
#configuraciones base
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024 * 1024  # 500MB
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

#Verificacion de extensiones
ALLOWED_EXTENSIONS = {'mp4', 'mov', 'avi', 'mkv'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/api/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400
        
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "Empty filename"}), 400
    
    if not allowed_file(file.filename):
        return jsonify({"error": "Formato de archivo no permitido"}), 400

    try:
        # 1. Guardar archivo temporal
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # 2. Verificar que el archivo se guardó correctamente
        if not Path(filepath).exists():
            raise RuntimeError("El archivo no se guardó correctamente")
        
        # 3. Convertir el video a audio 
        path_audio = os.path.join(app.config['UPLOAD_FOLDER'], 'audio.wav')
        convertir_video_a_audio(filepath, path_audio)

        # 4. Procesar con el transcriber
        transcriber = VideoTranscriber(path_audio)
        workflow = transcriber._build_workflow()

        while not Path(path_audio).exists():
            time.sleep(1)  # Esperar 1 segundo antes de verificar nuevamente

        result = workflow.invoke({})  # Ejecutar el workflow

        # 5. Obtener resultados del workflow
        raw_text = result.get("raw_text", "")
        texto_corregido = result.get("texto_corregido", raw_text)
        idioma_detectado = result.get("idioma", "desconocido")

        os.remove(filepath)
        os.remove(path_audio)

        # 6. Devolver respuesta estructurada al frontend
        return jsonify({
            "status": "success",
            "data": {
                "language": idioma_detectado,
                "raw_transcription": raw_text,
                "corrected_transcription": texto_corregido,
                "model_used": {
                    "transcription": "whisper-large-v3",
                    "language_detection": "gemma2-9b-it",
                    "text_correction": "meta-llama/llama-4-scout-17b-16e-instruct"
                }
            }
        })
        
    except Exception as e:
        # Limpieza en caso de error
        if 'filepath' in locals() and Path(filepath).exists():
            os.remove(filepath)
        if 'path_audio' in locals() and Path(path_audio).exists():
            os.remove(path_audio)
            
        return jsonify({
            "status": "error",
            "message": str(e),
            "details": f"Error al procesar {file.filename}"
        }), 500

@app.route('/api/export-txt', methods=['POST'])
def export_txt():
    try:
        data = request.json
        transcription = data.get('corrected_transcription', '')
        
        if not transcription:
            return jsonify({"error": "No transcription text provided"}), 400
            
        # Crear archivo en memoria
        file_obj = io.BytesIO()
        file_obj.write(transcription.encode('utf-8'))
        file_obj.seek(0)
        
        return send_file(
            file_obj,
            mimetype='text/plain',
            as_attachment=True,
            download_name='transcripcion.txt'
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/')
def main():
    return jsonify({"mensaje":"Inicio válido"})

@app.route('/api/test')
def test():
    return jsonify({"message": "Backend funcionando!"})

@app.errorhandler(500)
def handle_vertex_errors(e):
    if "VertexAI" in str(e):
        return jsonify({
            "status": "error",
            "message": "Error en el modelo de IA",
            "solution": "Verifique la configuración de Gemini en .env"
        }), 500
    return e

if __name__ == '__main__':
    app.run(debug=True)