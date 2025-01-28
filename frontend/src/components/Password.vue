<script setup lang="ts">
import { useSocketStore } from '@/stores/socket';
import { ref } from 'vue';

let timeout: number | null = null;
const password = ref<string>("");
const mode = ref<string>("password");
const { latency = 500 } = defineProps<{ latency?: number }>();
const socketStore = useSocketStore();

const set = async () => {
  socketStore.socket!.emit("set_password", password.value);
}

const setLater = async (event: any) => {
  password.value = event.target.value;
  if (timeout !== null) clearTimeout(timeout);
  timeout = setTimeout(set, latency);
}


async function switchVisibility() {
  mode.value = mode.value === "password" ? "text" : "password";
}

</script>

<template>
  <div class="password-wrapper">
    <input :type="mode" v-model="password" placeholder="Password" :oninput="setLater">
    <button @click="switchVisibility">{{ mode === "password" ? "Show" : "Hide" }}</button>
  </div>
</template>

<style scoped>
div.password-wrapper {
  display: grid;
  gap: 0;
  grid-template-columns: 10fr 1fr;
}
</style>
