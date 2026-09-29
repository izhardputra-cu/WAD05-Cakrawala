<script setup>
defineProps({
  user: { type: Object, required: true },
});
</script>

<template>
  <li class="user-card">
    <strong>{{ user.name }}</strong>
    <span>{{ user.email }}</span>
  </li>
</template>

<style scoped>
.user-card {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  padding: 0.75rem 1rem;
  border-bottom: 1px solid #ddd;
  overflow-wrap: anywhere;
}
.user-card:last-child { border-bottom: 0; }
</style>
