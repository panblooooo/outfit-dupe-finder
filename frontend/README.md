# Outfit Dupe Finder — Frontend

Frontend React + Vite yang mengikuti tiga layar Figma: Catalog, Detail & Filter, dan Comparison.

## Persiapan awal

Pastikan backend dan frontend sudah memiliki dependensi yang diperlukan.

### 1. Inisialisasi database (hanya untuk database baru)

Jika ini pertama kali menyiapkan database lokal, jalankan perintah berikut dari folder `backend`:

```bash
python -m app.seed
```

**Peringatan:** perintah seed akan menghapus tabel yang ada (`drop_all`) lalu membuat ulang tabel dan mengisi data contoh. Data yang tersimpan di database lokal dapat hilang. Jangan jalankan perintah ini setiap kali memulai aplikasi atau jika database berisi data yang ingin dipertahankan.

Jika database sudah pernah diinisialisasi dan berisi data yang ingin digunakan, lewati langkah ini.

## Menjalankan aplikasi

Jalankan backend dan frontend di dua terminal terpisah.

### 1. Backend

Dari folder utama repository:

```bash
cd backend
uvicorn app.main:app --reload
```

Backend berjalan di `http://127.0.0.1:8000`.

### 2. Frontend

Buka terminal baru dari folder utama repository:

```bash
cd frontend
npm install
```

Salin `.env.example` menjadi `.env`. Di Windows PowerShell, gunakan:

```powershell
Copy-Item .env.example .env
```

Di macOS/Linux, gunakan:

```bash
cp .env.example .env
```

Kemudian jalankan:

```bash
npm run dev
```

Buka alamat Vite yang ditampilkan di terminal (umumnya `http://localhost:5173`).

Atur `VITE_API_BASE_URL` di file `.env` jika backend berjalan di host atau port lain. Contoh nilai bawaan:

```env
VITE_API_BASE_URL=http://127.0.0.1:8000
```

## Integrasi API

- `GET /health` — status koneksi backend
- `GET /products?q=&page=&per_page=` — katalog dan pencarian
- `GET /products/{id}` — detail produk dan atribut
- `GET /products/{id}/dupes?max_price=&limit=5` — hasil dupe terurut berdasarkan skor kemiripan
- `GET /go/{dupe_id}?ref={reference_id}` — redirect affiliate

Skor kemiripan dihitung di backend menggunakan Weighted Cosine Similarity. Frontend menampilkan skor yang dikirim oleh API.

Kategori katalog dibaca dari field `kategori` pada respons produk. Produk yang belum memiliki URL gambar akan menggunakan placeholder sampai URL gambar ditambahkan ke database.
