<script setup lang="ts">
import { ref } from 'vue';
import IconClock from './icons/IconClock.vue';
let timeout: number | null = null;
const password = ref<string>("");
const mode = ref<string>("password");
const { latency = 500 } = defineProps<{ latency?: number }>();

const specs = {
  "Uptime": "10h",
  "Local state": "0 0 0",
  "Agent": navigator.userAgent,
};

</script>

<template>
<div class="current-device-wrapper">
  <div v-for="[key, value] of Object.entries(specs)" class="row">

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
