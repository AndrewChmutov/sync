<script setup lang="ts">
import { useSocketStore } from '@/stores/socket'
import { onMounted, ref } from 'vue'

let timeout: number | null = null
const directory = ref<string>('')
const mode = ref<boolean>(false)
const { latency = 500 } = defineProps<{ latency?: number }>()
const socketStore = useSocketStore()

const verify = async () => {
  console.log('WebSocket request: check_dir')
  socketStore.socket!.emit('check_dir', directory.value)
}

const verifyLater = async (event: InputEvent) => {
  directory.value = (event.target as HTMLInputElement).value
  if (timeout !== null) {
    clearTimeout(timeout)
  }
  timeout = setTimeout(verify, latency)
}

const isOk = (correct: boolean | null) => {
  mode.value = Boolean(correct)
}

onMounted(async () => {
  await new Promise((resolve) => setTimeout(resolve, 1000))
  console.log("Setting up 'correct_dir' event")
  socketStore.socket!.on('correct_dir', isOk)
})

const scan = () => {
  socketStore.socket!.emit('scan', directory.value)
}
</script>

<template>
  <div class="dirpicker-wrapper">
    <button @click="scan" :style="{ color: mode ? '' : 'red' }">Scan</button>
    <input placeholder="Directory" :oninput="verifyLater" />
  </div>
</template>

<style scoped>
div.dirpicker-wrapper {
  display: grid;
  gap: 0;
  grid-template-columns: 1fr 10fr;
}
</style>
