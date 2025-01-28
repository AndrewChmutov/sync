<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'
import HelloWorld from './components/HelloWorld.vue'
import Settings from './components/Settings.vue';
import Password from './components/Password.vue';
import DirPicker from './components/DirPicker.vue';
import CurrentDevice from './components/CurrentDevice.vue';
import Statistics from './components/Statistics.vue';

import { onMounted } from 'vue';
import { io } from "socket.io-client"
import { useSocketStore } from './stores/socket';

const socketStore = useSocketStore();

onMounted(() => {
  socketStore.connect();
});
</script>

<template>
  <header>
    <h1>SyncD</h1>
  </header>
  <div class="content">
    <Settings />
    <div class="two-columns">
      <div>
        <Password />
        <h2>Remotes</h2>
      </div>
      <div>
        <DirPicker />
        <h2>Current Device</h2>
        <CurrentDevice />
        <h2>Communication statistics</h2>
        <Statistics />
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
