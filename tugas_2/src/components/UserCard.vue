<script setup>
import { ref } from 'vue';

defineProps({
  user: { type: Object, required: true },
});

const detailTerbuka = ref(false);
</script>

<template>
  <li class="user-card">
    <div class="ringkasan">
      <div>
        <strong>{{ user.name }}</strong>
        <span>{{ user.email }}</span>
      </div>
      <button
        :aria-expanded="detailTerbuka"
        :aria-controls="'detail-' + user.id"
        @click="detailTerbuka = !detailTerbuka"
      >
        {{ detailTerbuka ? 'Sembunyikan' : 'Lihat Detail' }}
      </button>
    </div>
    <dl v-if="detailTerbuka" :id="'detail-' + user.id">
      <dt>Telepon</dt><dd>{{ user.phone }}</dd>
      <dt>Perusahaan</dt><dd>{{ user.company.name }}</dd>
      <dt>Kota</dt><dd>{{ user.address.city }}</dd>
    </dl>
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
.ringkasan { display: flex; justify-content: space-between; align-items: center; gap: 0.75rem; flex-wrap: wrap; }
.ringkasan span { display: block; margin-top: 0.25rem; }
dl { display: grid; grid-template-columns: auto 1fr; gap: 0.5rem; margin: 0.5rem 0 0; padding: 0.75rem; background: #f5f7f8; }
dt { font-weight: bold; }
dd { margin: 0; min-width: 0; }
</style>
