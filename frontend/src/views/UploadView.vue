<template>
    <div class="upload-container">
      <h2>Cargar Video para Transcripción</h2>
      <form @submit.prevent="handleSubmit" class="upload-form">
        <input 
          type="file" 
          ref="fileInput"
          accept=".mp4,.mov,.avi,.mkv" 
          @change="handleFileChange"
        >
        <button type="submit" :disabled="!file || isUploading">
          {{ isUploading ? 'Procesando...' : 'Transcribir archivo' }}
        </button>
      </form>
      <div v-if="error" class="error-message">
        {{ error }}
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue'
  import axios from 'axios'
  import { useRouter } from 'vue-router'
  
  const file = ref(null)
  const isUploading = ref(false)
  const error = ref(null)
  const router = useRouter()
  
  const handleFileChange = (e) => {
    file.value = e.target.files[0]
  }
  
  const handleSubmit = async () => {
    try {
      const formData = new FormData()
      formData.append('file', file.value)
      
      const response = await axios.post('/api/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })
      
      if (response.data.status === 'success') {
        const result = response.data.data
        router.push({
          name: 'results',
          query: { 
            transcription: result.corrected_transcription,
            language: result.language,
            modelos: result.model_used
          }
        })
      }
    } catch (error) {
      console.error('Error uploading file:', error)
    }
  }
  </script>
  
  <style scoped>
  .upload-container {
    max-width: 600px;
    margin: 2rem auto;
    padding: 2rem;
    border: 1px solid #e1e1e1;
    border-radius: 8px;
  }
  
  .upload-form {
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }
  
  .error-message {
    color: #ff4444;
    margin-top: 1rem;
  }
  </style>