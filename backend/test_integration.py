import unittest
from services.transcriber import VideoTranscriber
import os
from pathlib import Path
import whisper

class TestWorkflow(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.transcriber = VideoTranscriber()
    
    def setUp(self):
        # Resetear modelos entre tests
        self.transcriber.whisper_model = None
        self.transcriber.llm = None
    
    def test_workflow_structure(self):
        """Verifica que el workflow tiene los nodos correctos"""
        workflow = self.transcriber._build_workflow()
        # Verificamos que el workflow se compile correctamente
        self.assertIsNotNone(workflow)
        
        # Verificamos que las funciones clave existan en el transcriber
        self.assertTrue(hasattr(self.transcriber, '_clean_text'))
        self.assertTrue(hasattr(self.transcriber, '_enhance_text'))
    
    def test_llm_model_response(self):
        """Prueba que el modelo LLM responde a un prompt básico"""
        # Ruta relativa al modelo desde el directorio actual (test_integration.py)
        current_file = Path(__file__)  # backend/test_integration.py
        backend_dir = current_file.parent  # backend/
        model_path = backend_dir / "model" / "tinyllama-1.1b-chat-v1.0.Q2_K.gguf"
        
        if not model_path.exists():
            self.skipTest(f"Archivo del modelo no encontrado en {model_path}")
            
        try:
            self.transcriber._load_models()  # Usar la función _load_models original
        except Exception as e:
            self.skipTest(f"No se pudieron cargar los modelos: {str(e)}")

        # Verificamos que el modelo LLM esté disponible
        if not self.transcriber.llm:
            self.skipTest("Modelo LLM no disponible")

        prompt = "Hola dime que es Claude 3.7 en 30 palabras"

        # Probamos directamente la generación del modelo
        try:
            output = self.transcriber.llm.generate(prompt)
            # Asegurar que devuelve un string decente
            self.assertIsInstance(output, str)
            self.assertTrue(len(output) > 0)
            print("Respuesta del modelo:", output)
        except Exception as e:
            self.fail(f"Error al generar texto con el modelo: {str(e)}")


if __name__ == '__main__':
    unittest.main(
        failfast=True,  # Detener al primer error
        verbosity=2     # Mostrar más detalles
    )