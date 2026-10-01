<script setup>
import { computed, onMounted, ref } from 'vue';
import { API_URL } from './api.js';
import TambahBarang from './components/TambahBarang.vue';

const barang = ref([]);
const pencarian = ref('');
const arahUrutan = ref('asc');
const status = ref('idle');
const sedangMenghapus = ref(null);
const idKonfirmasi = ref(null);
const pesanAksi = ref('');
const aksiGagal = ref(false);

async function muatBarang() {
  status.value = 'loading';
  try {
    const response = await fetch(API_URL);
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const data = await response.json();
    if (!Array.isArray(data)) throw new Error('Data tidak valid');
    barang.value = data;
    status.value = data.length ? 'success' : 'empty';
  } catch {
    barang.value = [];
    status.value = 'error';
  }
}

const barangTersaring = computed(() => {
  const kataKunci = pencarian.value.trim().toLocaleLowerCase('id');
  return barang.value.filter((item) =>
    item.nama.toLocaleLowerCase('id').includes(kataKunci) ||
    item.kategori.toLocaleLowerCase('id').includes(kataKunci)
  );
});

const barangTerurut = computed(() =>
  [...barangTersaring.value].sort((a, b) => {
    const hasil = a.nama.localeCompare(b.nama, 'id');
    return arahUrutan.value === 'asc' ? hasil : -hasil;
  })
);

const ringkasan = computed(() => {
  const data = barang.value;
  return [
    { label: 'Total barang', nilai: data.length },
    { label: 'Menipis + habis', nilai: data.filter((item) => item.jumlah_stok <= 5).length },
    { label: 'Kategori', nilai: new Set(data.map((item) => item.kategori)).size },
    { label: 'Total unit', nilai: data.reduce((total, item) => total + item.jumlah_stok, 0) },
  ];
});

function labelStok(jumlah) {
  if (jumlah === 0) return 'Habis';
  return jumlah <= 5 ? 'Menipis' : 'Aman';
}

async function setelahTambah(nama) {
  aksiGagal.value = false;
  pesanAksi.value = `${nama} berhasil ditambahkan.`;
  await muatBarang();
}

async function hapusBarang(item) {
  sedangMenghapus.value = item.id;
  pesanAksi.value = '';
  try {
    const response = await fetch(`${API_URL}/${item.id}`, { method: 'DELETE' });
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    aksiGagal.value = false;
    pesanAksi.value = `${item.nama} dihapus.`;
    idKonfirmasi.value = null;
    await muatBarang();
  } catch {
    aksiGagal.value = true;
    pesanAksi.value = 'Gagal menghapus barang. Coba lagi.';
  } finally {
    sedangMenghapus.value = null;
  }
}

onMounted(muatBarang);
</script>

<template>
  <div class="app-shell">
    <div class="topbar">
      <div class="brand"><span class="brand-mark">IK</span><span>Inventaris Kantor</span></div>
      <span class="topbar-meta">WAD05 / UTS</span>
    </div>

    <main class="page-content">
      <header class="page-header">
        <div>
          <p class="eyebrow">Dashboard inventaris</p>
          <h1>Data barang kantor</h1>
          <p class="page-description">Stok dan lokasi barang dalam satu tampilan.</p>
        </div>
        <p class="owner">Izhar Rahman Dwiputra <span>25120300032</span></p>
      </header>

      <section class="stats" aria-label="Ringkasan inventaris">
        <div v-for="item in ringkasan" :key="item.label" class="stat-card">
          <span>{{ item.label }}</span>
          <strong>{{ item.nilai }}</strong>
        </div>
      </section>

      <div class="workspace-grid">
        <section class="inventory-panel" aria-labelledby="daftar-heading">
          <div class="panel-heading">
            <div>
              <p class="eyebrow">Daftar barang</p>
              <h2 id="daftar-heading">Inventaris</h2>
            </div>
            <button class="button button-secondary" type="button" :disabled="status === 'loading'" @click="muatBarang">Muat ulang</button>
          </div>

          <div class="toolbar">
            <div class="search-field">
              <label for="pencarian">Cari nama atau kategori</label>
              <input id="pencarian" v-model="pencarian" type="search" placeholder="Cari barang..." />
            </div>
            <div class="sort-field" role="group" aria-label="Urutkan berdasarkan nama">
              <button type="button" :class="{ active: arahUrutan === 'asc' }" :aria-pressed="arahUrutan === 'asc'" @click="arahUrutan = 'asc'">A-Z</button>
              <button type="button" :class="{ active: arahUrutan === 'desc' }" :aria-pressed="arahUrutan === 'desc'" @click="arahUrutan = 'desc'">Z-A</button>
            </div>
          </div>

          <p v-if="pesanAksi" class="action-message" :class="{ error: aksiGagal }" :role="aksiGagal ? 'alert' : 'status'">{{ pesanAksi }}</p>

          <p v-if="status === 'loading'" class="state-message" role="status">Memuat data barang...</p>
          <div v-else-if="status === 'error'" class="state-message error" role="alert">
            <p>Gagal terhubung ke backend. Pastikan FastAPI berjalan.</p>
            <button class="button button-primary" type="button" @click="muatBarang">Coba lagi</button>
          </div>
          <p v-else-if="status === 'empty'" class="state-message" role="status">Belum ada barang.</p>
          <p v-else-if="barangTersaring.length === 0" class="state-message" role="status">Tidak ada barang yang cocok dengan pencarian.</p>
          <template v-else>
            <p class="result-count" role="status">Menampilkan {{ barangTerurut.length }} dari {{ barang.length }} barang</p>
            <div class="table-scroll" role="region" aria-label="Tabel inventaris" tabindex="0">
              <table>
                <thead><tr><th scope="col">Barang</th><th scope="col">Kategori</th><th scope="col">Status</th><th scope="col">Stok</th><th scope="col">Lokasi gudang</th><th scope="col">Aksi</th></tr></thead>
                <tbody>
                  <tr v-for="item in barangTerurut" :key="item.id">
                    <td class="item-name">{{ item.nama }}</td>
                    <td>{{ item.kategori }}</td>
                    <td><span class="stock-status" :class="{ aman: item.jumlah_stok > 5, menipis: item.jumlah_stok > 0 && item.jumlah_stok <= 5, habis: item.jumlah_stok === 0 }">{{ labelStok(item.jumlah_stok) }}</span></td>
                    <td>{{ item.jumlah_stok }}</td>
                    <td>{{ item.lokasi_gudang }}</td>
                    <td>
                      <div v-if="idKonfirmasi === item.id" class="delete-actions">
                        <button class="delete-button confirm" type="button" :disabled="sedangMenghapus !== null" :aria-label="`Yakin hapus ${item.nama}`" @click="hapusBarang(item)">{{ sedangMenghapus === item.id ? 'Menghapus...' : 'Yakin hapus?' }}</button>
                        <button class="delete-button" type="button" :disabled="sedangMenghapus !== null" @click="idKonfirmasi = null">Batal</button>
                      </div>
                      <button v-else class="delete-button" type="button" :disabled="sedangMenghapus !== null" :aria-label="`Hapus ${item.nama}`" @click="idKonfirmasi = item.id">Hapus</button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </template>
        </section>
        <TambahBarang @tersimpan="setelahTambah" />
      </div>
    </main>
  </div>
</template>
