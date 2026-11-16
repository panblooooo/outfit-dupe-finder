# Outfit Dupe Finder — Frontend

Frontend React + Vite yang mengikuti tiga layar Figma: Catalog, Detail & Filter, dan Comparison.

## Menjalankan aplikasi

1. Jalankan backend FastAPI dari folder `backend`:
   ```bash
   python -m app.seed
   uvicorn app.main:app --reload
   ```
2. Buka terminal baru:
   ```bash
   cd frontend
   npm install
   cp .env.example .env
   npm run dev
   ```
3. Buka alamat Vite yang ditampilkan (umumnya http://localhost:5173).

Atur `VITE_API_BASE_URL` di file `.env` jika backend berjalan di host/port lain.

## Integrasi API

- `GET /health` — status koneksi backend
- `GET /products?q=&page=&per_page=` — katalog dan pencarian
- `GET /products/{id}` — detail produk dan atribut
- `GET /products/{id}/dupes?max_price=&limit=5` — hasil dupe terurut
- `GET /go/{dupe_id}?ref={reference_id}` — redirect affiliate

Kategori katalog dibaca dari field `kategori` pada respons produk. Produk lama yang tidak mengisi gambar akan menggunakan placeholder sampai URL gambar produk ditambahkan ke database.
