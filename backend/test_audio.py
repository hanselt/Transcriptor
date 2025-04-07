import os
import pytest
from pathlib import Path
from services.transcriber import convertir_video_a_audio
from werkzeug.utils import secure_filename

# Configuración del directorio de pruebas
UPLOAD_FOLDER = './uploads'  # Directorio donde se guardan los archivos de video y audio

# Función de prueba para verificar la conversión de video a audio
@pytest.fixture(scope='module')
def setup_video_file():
    # Ruta del archivo de video en la carpeta de prueba
    video_filepath = os.path.join(UPLOAD_FOLDER, 'video_test_langchain_1.mp4')
    
    # Asegurarse de que el archivo de video existe
    assert os.path.exists(video_filepath), "El archivo de video no se encuentra en el directorio de prueba"
    
    # Convertir el video a audio usando la función definida en tu aplicación
    audio_filepath = os.path.join(UPLOAD_FOLDER, 'audio.wav')  # Ruta del archivo de audio de salida        
    convertir_video_a_audio(video_filepath, audio_filepath)  # Llamar directamente la función

    # Asegurarse de que el archivo de audio fue creado correctamente
    assert os.path.exists(audio_filepath), f"El archivo de audio {audio_filepath} no se ha creado"
    
    return audio_filepath

def test_video_to_audio_conversion(setup_video_file):
    audio_filepath = setup_video_file
    
    # Verificar si el archivo de audio tiene la extensión correcta (por ejemplo, .wav)
    assert audio_filepath.endswith('.wav'), f"El archivo de audio debe ser un WAV, pero tiene {audio_filepath.split('.')[-1]}"
    
    # Opcional: Verificar que el archivo no esté vacío
    file_size = os.path.getsize(audio_filepath)
    assert file_size > 0, "El archivo de audio está vacío"
    
    # Imprimir el éxito
    print(f"El archivo de audio se generó correctamente: {audio_filepath}")
    
    # Eliminar el archivo de prueba después de la prueba
    try:
        os.remove(audio_filepath)
        print(f"Archivo de audio eliminado: {audio_filepath}")
    except Exception as e:
        print(f"Error al eliminar el archivo de audio: {e}")

# Ejecutar las pruebas con pytest
if __name__ == "__main__":
    pytest.main()
