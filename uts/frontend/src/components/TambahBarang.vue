<script setup>
import { ref } from 'vue';
import { API_URL } from '../api.js';

const emit = defineEmits(['tersimpan']);
const nama = ref('');
const kategori = ref('');
const jumlahStok = ref(0);
const lokasiGudang = ref('');
const sedangMenyimpan = ref(false);
const pesanError = ref('');

async function simpan() {
  sedangMenyimpan.value = true;
  pesanError.value = '';
  try {
    const response = await fetch(API_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        nama: nama.value.trim(),
        kategori: kategori.value.trim(),
        jumlah_stok: jumlahStok.value,
        lokasi_gudang: lokasiGudang.value.trim(),
      }),
    });
    if (response.status === 422) throw new Error('Periksa kembali isian barang.');
    if (!response.ok) throw new Error('Gagal menyimpan barang. Coba lagi.');
    const tersimpan = await response.json();
    nama.value = '';
    kategori.value = '';
    jumlahStok.value = 0;
    lokasiGudang.value = '';
    emit('tersimpan', tersimpan.nama);
  } catch (error) {
    pesanError.value = error instanceof TypeError ? 'Gagal terhubung ke backend.' : error.message;
  } finally {
    sedangMenyimpan.value = false;
  }
}
</script>

<template>
  <section class="form-panel" aria-labelledby="tambah-heading">
    <p class="eyebrow">Input barang</p>
    <h2 id="tambah-heading">Tambah barang</h2>
    <p class="form-description">Isi data barang yang masuk ke gudang.</p>

    <form @submit.prevent="simpan">
      <div class="form-fields">
        <div class="form-field">
          <label for="nama-barang">Nama barang</label>
          <input id="nama-barang" v-model="nama" name="nama" type="text" maxlength="80" placeholder="Contoh: Lampu meja" required />
        </div>
        <div class="form-field">
          <label for="kategori-barang">Kategori</label>
          <input id="kategori-barang" v-model="kategori" name="kategori" type="text" maxlength="40" placeholder="Contoh: Perlengkapan" required />
        </div>
        <div class="form-field">
          <label for="jumlah-stok">Jumlah stok</label>
          <input id="jumlah-stok" v-model.number="jumlahStok" name="jumlah_stok" type="number" min="0" step="1" required />
        </div>
        <div class="form-field">
          <label for="lokasi-gudang">Lokasi gudang</label>
          <input id="lokasi-gudang" v-model="lokasiGudang" name="lokasi_gudang" type="text" maxlength="60" placeholder="Contoh: Rak ATK A" required />
        </div>
      </div>
      <p v-if="pesanError" class="form-error" role="alert">{{ pesanError }}</p>
      <button class="button button-primary submit-button" type="submit" :disabled="sedangMenyimpan">{{ sedangMenyimpan ? 'Menyimpan...' : 'Simpan barang' }}</button>
    </form>
  </section>
</template>
