<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const responseData = ref(null)
const errorMessage = ref(null)

onMounted(async () => {
  try {
    const response = await axios.get('/api/test')
    responseData.value = response.data
  } catch (error) {
    errorMessage.value = `Error: ${error.message}`
    console.error('Detalles del error:', error)
  }
})
</script>

<template>
  <div class="container">
    <h1>Prueba de conexión Flask-Vue</h1>
    
    <div v-if="responseData" class="alert success">
      <h3>✅ Conexión exitosa</h3>
      <pre>{{ responseData }}</pre>
    </div>
    
    <div v-if="errorMessage" class="alert error">
      <h3>❌ Error de conexión</h3>
      <p>{{ errorMessage }}</p>
    </div>

    <div class="debug-info">
      <h4>Información para depuración:</h4>
      <p><strong>Endpoint llamado:</strong> /api/test</p>
      <p><strong>Proxy configurado:</strong> http://localhost:5000</p>
    </div>
  </div>
</template>

<style scoped>
.container {
  max-width: 800px;
  margin: 2rem auto;
  padding: 1rem;
}

.alert {
  padding: 1rem;
  border-radius: 8px;
  margin: 1rem 0;
}

.success {
  background-color: #e6ffed;
  border: 1px solid #a3f3a3;
}

.error {
  background-color: #ffebee;
  border: 1px solid #ffcdd2;
}

.debug-info {
  margin-top: 2rem;
  padding: 1rem;
  background-color: #f5f5f5;
  border-radius: 8px;
}
</style>