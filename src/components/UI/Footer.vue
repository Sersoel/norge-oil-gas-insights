<template>
  <footer class="text-sm text-gray-500 p-4 text-center">
    <p v-if="lastUpdate">Data last updated: {{ formatDate(lastUpdate) }}</p>
  </footer>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const lastUpdate = ref(null)

onMounted(async () => {
  const metadata = await fetch('./assets/data/metadata.json').then((res) => res.json())
  lastUpdate.value = metadata.fetched_at
})

function formatDate(isoString) {
  const date = new Date(isoString)
  return date.toLocaleDateString('en-GB', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  })
}
</script>
