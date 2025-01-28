<script setup lang="ts">
import PasswordField from './components/PasswordField.vue'
import DirPicker from './components/DirPicker.vue'
import CurrentDevice from './components/CurrentDevice.vue'
import StatisticsView from './components/StatisticsView.vue'

import { onMounted } from 'vue'
import { useSocketStore } from './stores/socket'

const socketStore = useSocketStore()

onMounted(() => {
  socketStore.connect()
})
</script>

<template>
  <header>
    <h1>SyncD</h1>
  </header>
  <div class="content">
    <div class="two-columns">
      <div>
        <PasswordField />
        <h2>Remotes</h2>
      </div>
      <div>
        <DirPicker />
        <h2>Current Device</h2>
        <CurrentDevice />
        <h2>Communication statistics</h2>
        <StatisticsView />
      </div>
    </div>
  </div>
</template>

<style scoped>
header {
  display: flex;
}

header > h1 {
  margin: auto;
  margin-bottom: 2rem;
}
.content {
  margin: 0 15rem;
}

.content .two-columns {
  display: grid;
  grid-template-columns: 1fr 1fr;
}
</style>
