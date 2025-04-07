<template>
    <form @submit.prevent="uploadFile">
      <input type="file" @change="handleFileChange">
      <button type="submit">Transcribir</button>
    </form>
  </template>