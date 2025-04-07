<template>
    <button @click="retornarBase" class="retornar-btn">
      <i class="fas fa-download"></i> Volver a Cargar otro video
    </button>
  </template>
  
  <script setup>
    import { useRouter } from 'vue-router'

    const router = useRouter()

    const retornarBase = () => {
    // Navegar programáticamente al inicio (ruta home)
    router.push({ name: 'upload' }) // 'upload' es el nombre de la ruta de carga
    }
    </script>
  
  <style scoped>
    .retornar-btn {
        background-color: #34495e;
        color: white;
        border: none;
        padding: 10px 15px;
        border-radius: 4px;
        cursor: pointer;
        font-size: 1rem;
        transition: background-color 0.3s;
        margin-left: 5px;
    }

    .retornar-btn:hover {
        background-color: #3b5f83;
    }

    .retornar-btn i {
        margin-right: 8px;
    }
    </style>