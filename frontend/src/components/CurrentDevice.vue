<script setup lang="ts">
import { useSocketStore } from '@/stores/socket'
import { onMounted, reactive } from 'vue'
import { faFile, faFolderOpen, faDatabase } from '@fortawesome/free-solid-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

interface LocalState {
  n_dirs: number
  n_bytes: number
  n_files: number
}

interface CurrentDevice {
  uptime: number
  path: string
  local_state: LocalState | null
  agent: string
}

const specs = reactive<CurrentDevice>({
  uptime: 0,
  path: '',
  local_state: {
    n_dirs: 0,
    n_bytes: 0,
    n_files: 0,
  },
  agent: '',
})

const socketStore = useSocketStore()
const setCurrentDevice = (receivedCurrentDevice: CurrentDevice) => {
  console.log(`WebSocket response set_current_device: ${JSON.stringify(receivedCurrentDevice)}`)
  Object.assign(specs, receivedCurrentDevice)
}

onMounted(async () => {
  await new Promise((resolve) => setTimeout(resolve, 1000))
  console.log("Setting up 'set_current_device' event")
  socketStore.socket!.on('set_current_device', setCurrentDevice)
})

const formatTime = (seconds: number) => {
  const totalSeconds = Math.floor(seconds)

  const hours = Math.floor(totalSeconds / 3600)
  const minutes = Math.floor((totalSeconds % 3600) / 60)
  const secs = totalSeconds % 60

  const paddedHours = String(hours).padStart(2, '0')
  const paddedMinutes = String(minutes).padStart(2, '0')
  const paddedSeconds = String(secs).padStart(2, '0')

  return `${paddedHours}:${paddedMinutes}:${paddedSeconds}`
}

const formatSize = (bytes: number) => {
  if (bytes < 1024) {
    return bytes + ' B'
  } else if (bytes < 1024 * 1024) {
    return (bytes / 1024).toFixed(2) + ' Kb'
  } else if (bytes < 1024 * 1024 * 1024) {
    return (bytes / (1024 * 1024)).toFixed(2) + ' Mb'
  } else {
    return (bytes / (1024 * 1024 * 1024)).toFixed(2) + ' Gb'
  }
}
</script>

<template>
  <div class="current-device-wrapper">
    <div class="table">
      <div class="row">
        <div>Uptime</div>
        <div>{{ formatTime(specs.uptime) }}</div>
      </div>
      <div class="row">
        <div>Path</div>
        <div>{{ specs.path }}</div>
      </div>
      <div class="row">
        <div>Local state</div>
        <div v-if="specs.local_state">
          <FontAwesomeIcon :icon="faFolderOpen" /> {{ specs.local_state.n_dirs }}
          <FontAwesomeIcon :icon="faFile" /> {{ specs.local_state.n_files }}
          <FontAwesomeIcon :icon="faDatabase" /> {{ formatSize(specs.local_state.n_bytes) }}
        </div>
        <div v-else>Loading</div>
      </div>
      <div class="row">
        <div>Agent</div>
        <div>{{ specs.agent }}</div>
      </div>
    </div>
  </div>
</template>

<style scoped>
div > .current-device-wrapper > .table > .row {
  display: grid;
  gap: 0;
  grid-template-columns: 1fr 1fr;
}

div > .current-device-wrapper > .table > .row > div:last-child {
  margin-left: auto;
  text-align: right;
}
</style>
