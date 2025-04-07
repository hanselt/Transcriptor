import os
from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, END
from groq import Groq
from dotenv import load_dotenv  # Para variables de entor
from moviepy.editor import VideoFileClip

load_dotenv()

client = Groq(api_key=os.getenv("GROG_API"))
folder_documentos = os.getenv("UPLOAD_FOLDER")

def convertir_video_a_audio(video_filepath, audio_filepath):
        try:
            # Convertir video a audio
            video = VideoFileClip(video_filepath)
            audio = video.audio
            audio.write_audiofile(
                audio_filepath, 
                codec='pcm_s16le', 
                ffmpeg_params=['-ac', '1', '-ar', '16000']  # Mono, 16kHz
            ) # Guardar el archivo de audio
            video.close()  # Cerrar el archivo de video
            
            # Verificar si el archivo de audio fue creado correctamente
            if not os.path.exists(audio_filepath):
                raise FileNotFoundError(f"No se pudo crear el archivo de audio: {audio_filepath}")
            
            print(f"Audio guardado correctamente en: {audio_filepath}")
            

        except Exception as e:
            print(f"Error durante la conversión o reproducción del audio: {e}")
            raise

class VideoTranscriber:
    def __init__(self, audio_path):
        self.audio_path = audio_path      
        
    def _build_workflow(self):
        """Workflow simplificado con LangGraph para transcribir audio y guardar la transcripción"""
        # Define el estado que pasa entre nodos
        class WorkflowState(TypedDict):
            raw_text: Annotated[str, "Texto original transcrito"]
            idioma: Annotated[str, "Idioma detectado"]
            texto_corregido: Annotated[str, "Texto corregido"]

        workflow = StateGraph(WorkflowState)

        # Nodo 1: Transcripción de audio
        def transcribir_audio_node(state):            
            transcription = self.transcribir_audio()
            if transcription:
                return {"raw_text": transcription['text'] if isinstance(transcription, dict) else transcription}
            return {}

        workflow.add_node("transcribe_audio", transcribir_audio_node)

        # Nodo 2: Detectar idioma
        def detectar_idioma_node(state):
            idioma = self.detectar_idioma(state["raw_text"])
            return {"idioma": idioma}

        workflow.add_node("detectar_idioma", detectar_idioma_node)

        # Nodo 3: Corregir texto
        def corregir_texto_node(state):
            texto_corregido = self.corregir_texto(state["raw_text"])
            return {"texto_corregido": texto_corregido}
        
        workflow.add_node("corregir_texto", corregir_texto_node)

        # Nodo 4: Guardar transcripción final
        def copiar_transcripcion_node(state):
            texto = state.get("texto_corregido", state.get("raw_text", ""))
            idioma = state.get("idioma", "Desconocido")
            texto_final = f"[Idioma detectado: {idioma}]\n\n{texto}"
            self.copiar_transcripcion(texto_final)
            return state

        workflow.add_node("copy_transcription", copiar_transcripcion_node)

        # Enlaces
        workflow.set_entry_point("transcribe_audio")

        # Flujos paralelos desde transcripción
        workflow.add_edge("transcribe_audio", "detectar_idioma")
        workflow.add_edge("transcribe_audio", "corregir_texto")

        # Ambas ramas terminan en el nodo de escritura
        workflow.add_edge("detectar_idioma", "copy_transcription")
        workflow.add_edge("corregir_texto", "copy_transcription")

        # Nodo final
        workflow.set_finish_point("copy_transcription")

        return workflow.compile()

    def transcribir_audio(self):
        try:
            with open(self.audio_path, "rb") as audio_archivo:
                transcripcion = client.audio.transcriptions.create(
                    file=(os.path.basename(self.audio_path), audio_archivo.read()),
                    model="whisper-large-v3",
                    prompt="""el audio es una conversación o entrevista de un grupo de personas""",
                    response_format="text",
                )
            return transcripcion
        except Exception as e:
            print(f"Error: {str(e)}")
            return None

    def copiar_transcripcion(self, text):
        path_doc = os.path.join(folder_documentos, 'transcription.txt')
        try:
            with open(path_doc, "w", encoding="utf-8") as file:
                file.write(text)
            print(f"Transcripción guardada en {path_doc}")
        except Exception as e:
            print(f"Error al guardar la transcripción: {str(e)}")

    def detectar_idioma(self, texto):
        prompt = f"Detecta el idioma de este texto. Solo responde con el nombre del idioma:\n\n\"{texto}\""
        respuesta = client.chat.completions.create(
            model="gemma2-9b-it",
            messages=[{"role": "user", "content": prompt}]
        )
        return respuesta.choices[0].message.content.strip()

    def corregir_texto(self, texto):
        prompt = f"""Corrige la ortografía y agrega signos de puntuación al siguiente texto, sin cambiar el idioma ni el contenido:\n\n{texto}"""
        respuesta = client.chat.completions.create(
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            messages=[{"role": "user", "content": prompt}]
        )
        return respuesta.choices[0].message.content.strip()

    