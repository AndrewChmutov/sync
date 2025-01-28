<script setup lang="ts">
import { onMounted, onUnmounted, reactive, ref } from 'vue';
import IconClock from './icons/IconClock.vue';
import { useSocketStore } from '@/stores/socket';

let timeout: number | null = null;
const password = ref<string>("");
const mode = ref<string>("password");
const { latency = 500 } = defineProps<{ latency?: number }>();
let interval = null;
const stats = reactive({})

interface IStatistics {
    refreshes: number
    pushes: number
    pulls: number

    sent_bytes: number
    sent_files: number

    received_bytes: number
    received_files: number
};

const socketStore = useSocketStore();
const setStats = (receivedStats: IStatistics) => {
  console.log(`WebSocket response set_stats: ${receivedStats}`)
  Object.assign(stats, {
    "Refreshes": receivedStats.refreshes,
    "Pushes":  receivedStats.pushes,
    "Pulls": receivedStats.pulls,

    "Sent bytes": receivedStats.sent_bytes,
    "Sent files": receivedStats.sent_files,

    "Received bytes": receivedStats.received_bytes,
    "Received files": receivedStats.received_files,
  });
};

const getStats = () => {
  console.log("WebSocket request: get_stats")
  socketStore.socket!.emit("get_stats");
}

onMounted(async () => {
  await (new Promise(resolve => setTimeout(resolve, 1000)));
  console.log("Setting up 'set_stats' event");
  socketStore.socket!.on("set_stats", setStats);

  console.log("Setting up 'get_stats' interval");
  interval = setInterval(getStats, latency);
});

onUnmounted(() => {
  interval = null;
})

</script>

<template>
<div class="stats-wrapper">
  <div v-for="[key, value] of Object.entries(stats)" class="row">

    <div>{{ key }}</div>
    <div>{{ value }}</div>
  </div>
</div>
</template>

<style scoped>
div > .stats-wrapper > .row {
  display: grid;
  gap: 0;
  grid-template-columns: 1fr 1fr;
}

div > .stats-wrapper > .row > div:last-child {
  margin-left: auto;
  text-align: right;
}
</style>
