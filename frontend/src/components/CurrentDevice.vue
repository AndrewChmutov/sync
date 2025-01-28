<script setup lang="ts">
const specs = {
  Uptime: '10h',
  'Local state': '0 0 0',
  Agent: navigator.userAgent,
}
</script>

<template>
  <div class="current-device-wrapper">
    <div v-for="[key, value] of Object.entries(specs)" :key="key" class="row">
      <div>{{ key }}</div>
      <div>{{ value }}</div>
    </div>
  </div>
</template>

<style scoped>
div > .current-device-wrapper > .row {
  display: grid;
  gap: 0;
  grid-template-columns: 1fr 1fr;
}

div > .current-device-wrapper > .row > div:last-child {
  margin-left: auto;
  text-align: right;
}
</style>
