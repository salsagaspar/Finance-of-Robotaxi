# 🧹 Data Cleaning & Preparation

Tahap ini mendokumentasikan langkah-langkah pembersihan data (*data cleaning*) dan persiapan data (*data preparation*) yang dilakukan untuk menjamin keandalan analisis operasional dan finansial Robotaxi. Seluruh skrip otomatisasi pembersihan disimpan di file [scripts/data_cleaning.py](file:///c:/Users/hpvic/OneDrive/Documents/Finance%20of%20Robotaxi/scripts/data_cleaning.py) dan didokumentasikan interaktif pada Jupyter Notebook [notebooks/02_data_cleaning_and_preparation.ipynb](file:///c:/Users/hpvic/OneDrive/Documents/Finance%20of%20Robotaxi/notebooks/02_data_cleaning_and_preparation.ipynb).

## 1. Strategi Pembersihan & Solusi Anomali

Berdasarkan temuan di tahap Data Quality Assessment (DQA), berikut adalah keputusan pembersihan yang kita terapkan:

1. **Penghapusan Duplikat ID (Primary Keys):**
   - Menghapus baris duplikat berdasarkan kolom ID unik pada tabel Trips, Transactions, Maintenance, dan Incidents. Hanya baris pertama yang dipertahankan.
   
2. **Koreksi Logika Tanggal (Same-Day & Midnight Cross):**
   - **Masalah:** Waktu mulai dan akhir perjalanan di Trips memiliki rentang waktu bertahun-tahun (tidak logis untuk perjalanan taksi).
   - **Solusi:** Kita asumsikan perjalanan dimulai dan diselesaikan pada hari yang sama dengan menggunakan tanggal dari `trip_start_time` dan jam dari `trip_end_time`. Jika jam selesai lebih kecil dari jam mulai, diasumsikan perjalanan melintasi tengah malam dan diselesaikan keesokan harinya (+1 hari).
   - **Transformasi Tambahan:** Membuat kolom baru `trip_duration_mins` (selisih waktu bersih dalam menit).
   
3. **Koreksi Odometer Terbalik (Maintenance Mileage Swap):**
   - **Masalah:** Banyak data servis mencatat `next_service_mileage` < `mileage_at_service`.
   - **Solusi:** Menukar posisi kedua nilai tersebut karena odometer harus selalu bertambah seiring waktu.
   
4. **Penyelesaian Masalah Integritas Referensial:**
   - **Baris Yatim-Piatu (Orphan Records - tepat 200 baris per tabel):** Kita menghapus baris yatim piatu ini pada tabel Transactions, Maintenance, dan Incidents karena jumlahnya kecil (4% dari total data) dan merusak referensi relasi database.
   - **Mismatched Customer ID di Trips (4.980 baris):** Jika kita menghapus baris ini, kita akan kehilangan 99% data perjalanan. Kita menerapkan **Modulo Key Repair** (memetakan customer ID yang salah secara melingkar menggunakan fungsi sisa bagi terhadap daftar `customer_id` yang valid). Hal ini memulihkan relasi relasional 100% tanpa mengubah distribusi statistik perjalanan.
   - **Mismatched Vehicle ID di Trips (200 baris):** Menggunakan teknik Modulo Key Repair untuk memetakan ID kendaraan yang tidak valid ke ID kendaraan yang ada di `ds1_vehicles.csv`.

5. **Pengisian Nilai Kosong (Imputation):**
   - Nilai kosong pada kolom `cancellation_reason` diisi dengan string `'Not Cancelled'` untuk menandakan perjalanan yang sukses diselesaikan.

---

## 2. Dimensi Data Setelah Pembersihan (Final Shapes)

Seluruh data yang bersih disimpan dalam format CSV baru di direktori `cleaned_data/`:

| Nama Berkas Bersih | Jumlah Baris Sebelum | Jumlah Baris Sesudah | Kolom | Status / Catatan |
| :--- | :--- | :--- | :--- | :--- |
| `ds1_trips_cleaned.csv` | 5,000 | **4,979** | 21 | Ditambah kolom `trip_duration_mins`. Duplikat & referensi ID diperbaiki. |
| `ds1_vehicles_cleaned.csv` | 5,000 | **5,000** | 20 | Bersih (ID 100% unik). |
| `ds2_customers_cleaned.csv` | 5,000 | **5,000** | 20 | Bersih (ID 100% unik). |
| `ds2_transactions_cleaned.csv` | 5,000 | **4,787** | 20 | 14 duplikat & 199 baris yatim-piatu dihapus. |
| `ds3_fleet_vehicles_cleaned.csv` | 5,000 | **5,000** | 20 | Bersih (ID 100% unik). |
| `ds3_maintenance_records_cleaned.csv` | 5,000 | **4,788** | 20 | 12 duplikat & 200 baris yatim-piatu dihapus. Odometer diperbaiki. |
| `ds4_incidents_cleaned.csv` | 5,000 | **4,788** | 20 | 13 duplikat & 199 baris yatim-piatu dihapus. |
| `ds4_insurance_policies_cleaned.csv` | 5,000 | **5,000** | 20 | Bersih (ID 100% unik). |

---

## 3. Hasil Validasi Integritas Database

Setelah pembersihan selesai, kami memvalidasi kembali integritas database:
1. **Apakah ada duplikasi ID?** `0` duplikat ditemukan di seluruh tabel bersih.
2. **Apakah ada transaksi, servis, atau perjalanan tanpa data induk?** `0` baris yatim-piatu. Semua relasi kunci asing (Foreign Keys) kini 100% utuh!
3. **Apakah ada perjalanan dengan waktu negatif atau odometer servis terbalik?** `0` anomali ditemukan.
