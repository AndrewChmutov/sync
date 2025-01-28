<script setup lang="ts">
import { ref } from 'vue';

let timeout: number | null = null;
const password = ref<string>("");
const mode = ref<string>("password");
const { latency = 500 } = defineProps<{ latency?: number }>();

const set = async () => {
  console.log("fast")
  await fetch(
     "/api/set-password", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ dir: password.value })
    }
  );
  timeout = null;
}

const setLater = async (event: any) => {
  password.value = event.target.value;
  if (timeout !== null) {
    clearTimeout(timeout);
  }
  timeout = setTimeout(set, latency);
}


async function switchVisibility() {
  mode.value = mode.value === "password" ? "text" : "password";
}

</script>

<template>
Last Scan
IP
</template>

<style scoped>
div.password-wrapper {
  display: grid;
  gap: 0;
  grid-template-columns: 10fr 1fr;
}
</style>
