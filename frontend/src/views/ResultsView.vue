<template>
    <div class="results-container">
      <h2>Resultado de Transcripción</h2>
      <div class="metadata">
        <span>Idioma: {{ language }}</span>
        <span>Caracteres: {{ text.length }}</span>
      </div>
      <div class="transcription-content">
        <pre>{{ text }}</pre>
      </div>
      <DownloadButton :text="text" />
      <RetornarButton/>
    </div>
  </template>
  
  <script setup>
  import DownloadButton from '@/components/DownloadButton.vue'
import RetornarButton from '@/components/RetornarButton.vue'
  import { computed } from 'vue'
  import { useRoute } from 'vue-router'
  
  const route = useRoute()
  const text = computed(() => route.query.transcription || '')
  const language = computed(() => route.query.language || 'desconocido')
  </script>
  
  <style scoped>
  .results-container {
    max-width: 800px;
    margin: 2rem auto;
    padding: 2rem;
  }
  
  .metadata {
    display: flex;
    gap: 1rem;
    margin-bottom: 1rem;
    color: #666;
  }
  
  .transcription-content {
    background: #f8f9fa;
    padding: 1.5rem;
    border-radius: 8px;
    margin: 1.5rem 0;
    white-space: pre-wrap;
    max-height: 60vh;
    overflow-y: auto;
  }
  </style>