# UTS WAD05 — Inventaris Kantor

Izhar Rahman Dwiputra · 25120300032 · Soal B

## Menjalankan

Jalankan dari root repo `Tugas_IRD/` di dua terminal. Backend (Python 3.10+):

```bash
cd uts/backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

Frontend (Node.js):

```bash
cd uts/frontend
npm install
npm run dev
```

Buka `http://127.0.0.1:5173`. Dokumentasi API tersedia di `http://127.0.0.1:8000/docs`.

Data awal berisi 20 barang kantor dari `backend/seed_barang.json`. Data disimpan di memori dan kembali ke kondisi awal saat backend dimulai ulang. Status stok: **Habis** (0), **Menipis** (1–5), dan **Aman** (lebih dari 5).
