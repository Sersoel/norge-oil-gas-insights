<template>
    <section :id="sectionId" class="p-8 border-t border-gray-200">
      <h2 class="text-xl font-bold mb-2">{{ title }}</h2>
      <slot />
    </section>
  </template>
  
  <script setup>
  defineProps({
    title: String,
    sectionId: String
  });
  </script>