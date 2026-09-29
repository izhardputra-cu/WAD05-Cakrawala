<script setup>
import { ref, computed, watch } from 'vue';
import UserCard from './components/UserCard.vue';

const users = ref([]);
const keadaan = ref('idle');
const queryPencarian = ref('');
const riwayatPencarian = ref([]);

async function muatPengguna() {
  keadaan.value = 'loading';
  try {
    const response = await fetch('https://jsonplaceholder.typicode.com/users');
    if (!response.ok) throw new Error('Status HTTP: ' + response.status);
    const data = await response.json();
    if (!Array.isArray(data)) throw new Error('Data pengguna tidak valid');
    users.value = data;
    keadaan.value = data.length === 0 ? 'empty' : 'success';
  } catch {
    keadaan.value = 'error';
  }
}

const penggunaTersaring = computed(() => {
  const q = queryPencarian.value.toLowerCase().trim();
  if (!q) return users.value;
  return users.value.filter((user) => user.username.toLowerCase().includes(q));
});

const jumlahHasil = computed(() => penggunaTersaring.value.length);

watch(queryPencarian, (nilaiBaru) => {
  if (nilaiBaru.trim() !== '') riwayatPencarian.value.push(nilaiBaru);
});
</script>

<template>
  <header>
    <h1>Dashboard Vue - Pertemuan 5</h1>
    <p>Izhar Rahman Dwiputra | 25120300032</p>
  </header>

  <main>
    <div class="kontrol">
      <button :disabled="keadaan === 'loading'" @click="muatPengguna">Muat Pengguna</button>
      <label for="pencarian">Cari username</label>
      <input id="pencarian" v-model="queryPencarian" type="search" placeholder="Cari username..." />
    </div>

    <p v-if="keadaan === 'idle'" role="status">Klik Muat Pengguna untuk menampilkan daftar.</p>
    <p v-else-if="keadaan === 'loading'" role="status">Memuat data...</p>
    <p v-else-if="keadaan === 'empty'" role="status">Tidak ada pengguna ditemukan.</p>
    <p v-else-if="keadaan === 'error'" role="alert">Gagal memuat data. Coba lagi.</p>
    <section v-else-if="keadaan === 'success'" aria-label="Daftar pengguna">
      <p role="status">Menampilkan {{ jumlahHasil }} dari {{ users.length }} pengguna</p>
      <p v-if="jumlahHasil === 0">Tidak ada username yang cocok.</p>
      <ul v-else>
        <UserCard v-for="user in penggunaTersaring" :key="user.id" :user="user" />
      </ul>
    </section>
  </main>
</template>

<style scoped>
header {
  padding: 1.5rem;
  background: #0b4f6c;
  color: white;
}
h1 { margin: 0; font-size: 1.5rem; }
header p { margin: 0.5rem 0 0; }
main { max-width: 800px; padding: 1.5rem; margin: auto; }
.kontrol { display: flex; gap: 0.75rem; align-items: center; flex-wrap: wrap; }
input { max-width: 100%; min-width: 0; }
ul { list-style: none; padding: 0; border: 1px solid #ddd; border-radius: 4px; background: white; }
</style>
