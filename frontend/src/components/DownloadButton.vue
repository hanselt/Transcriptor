<template>
    <button @click="exportToTxt" class="download-btn">
      <i class="fas fa-download"></i> Descargar TXT
    </button>
  </template>
  
  <script setup>
  import { ref } from 'vue'
  import axios from 'axios'
  
  const props = defineProps({
    text: {
      type: String,
      required: true
    }
  })
  
  const exportToTxt = async () => {
    try {
      const response = await axios.post('/api/export-txt', 
        { corrected_transcription: props.text },
        { responseType: 'blob' }
      )
      
      const url = window.URL.createObjectURL(new Blob([response.data]))
      const link = document.createElement('a')
      link.href = url
      link.setAttribute('download', 'transcripcion.txt')
      document.body.appendChild(link)
      link.click()
      link.remove()
    } catch (error) {
      console.error('Error al exportar:', error)
    }
  }
  </script>
  
  <style scoped>
  .download-btn {
    background-color: #42b983;
    color: white;
    border: none;
    padding: 10px 15px;
    border-radius: 4px;
    cursor: pointer;
    font-size: 1rem;
    transition: background-color 0.3s;
  }
  
  .download-btn:hover {
    background-color: #369f6b;
  }
  
  .download-btn i {
    margin-right: 8px;
  }
  </style>