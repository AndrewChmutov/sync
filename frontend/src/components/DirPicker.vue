<script setup lang="ts">
import { useSocketStore } from '@/stores/socket';
import { onMounted, ref } from 'vue';

let timeout: number | null = null;
const directory = ref<string>("");
const mode = ref<boolean>(false);
const { latency = 500 } = defineProps<{ latency?: number }>();
const socketStore = useSocketStore()

const verify = async () => {
  socketStore.socket!.emit("check_dir", directory.value);
};

const verityLater = async (event: any) => {
  directory.value = event.target.value;
  if (timeout !== null) {
    clearTimeout(timeout);
  }
  timeout = setTimeout(verify, latency);
};

const isOk = (correct: Boolean | null) => {
  mode.value = Boolean(correct);
};

onMounted(async () => {
  await (new Promise(resolve => setTimeout(resolve, 1000)));
  console.log("Setting up 'correct_dir' event");
  socketStore.socket!.on("correct_dir", isOk);
});
</script>

<template>
  <div class="dirpicker-wrapper">
    <button>{{ mode }}</button>
    <input placeholder="Directory" :oninput="verityLater"></input>
  </div>
</template>

<style scoped>
div.dirpicker-wrapper {
  display: grid;
  gap: 0;
  grid-template-columns: 1fr 10fr;
}
</style>
