# 🔍 Laporan Data Quality Assessment (DQA)

Laporan ini mendokumentasikan temuan anomali, duplikasi, dan inkonsistensi data yang ditemukan pada ke-8 dataset **Finance of Robotaxi**. Pemeriksaan dilakukan menggunakan Jupyter Notebook `notebooks/01_data_quality_assessment.ipynb`.

## 1. Temuan Utama (Key Findings)

Secara umum, dataset ini bersih dari nilai kosong (*null*), namun memiliki **masalah logika dan integritas referensial yang sangat serius** yang dapat merusak analisis jika tidak dibersihkan.

### Summary Masalah Kualitas Data

| Dataset | Jenis Masalah | Detail Masalah | Dampak Bisnis |
| :--- | :--- | :--- | :--- |
| `ds1_trips.csv` | Duplikasi ID & Logika Waktu | - **21 baris duplikat** pada `trip_id`. <br> - **2.466 baris** memiliki `trip_end_time` < `trip_start_time` (hampir 50% data terbalik!). | Analisis durasi perjalanan, kecepatan rata-rata, dan jam sibuk (*peak hours*) akan menjadi tidak akurat atau menghasilkan nilai negatif. |
| `ds1_vehicles.csv` vs `ds3_fleet_vehicles.csv` | Tabrakan ID Armada | - Hanya ada **40 ID yang tumpang tindih**, tetapi menunjuk pada kendaraan yang **berbeda** (Contoh: ID `892800` di ds1 adalah *Tesla Model 3 White*, sedangkan di ds3 adalah *Waymo EV6*). | Dua sistem penomoran armada yang berbeda. Data pemeliharaan tidak bisa langsung digabung dengan data perjalanan berdasarkan ID tanpa pembersihan. |
| **Integritas Referensial (Foreign Keys)** | Hubungan Kunci Hilang | - **4.980 perjalanan** merujuk ke `customer_id` yang **TIDAK ADA** di `ds2_customers.csv`. <br> - **200 transaksi** kehilangan referensi `customer_id`. <br> - **200 catatan pemeliharaan** kehilangan referensi `fleet_vehicle_id`. <br> - **200 insiden** kehilangan referensi `policy_id`. | Sulit untuk melakukan analisis *Customer Lifetime Value (CLV)* secara akurat atau memetakan biaya pemeliharaan secara penuh per kendaraan. |
| `ds3_maintenance_records.csv` | Logika Odometer Terbalik | - **2.315 baris** memiliki `next_service_mileage` < `mileage_at_service` (hampir 50% data). | Penjadwalan pemeliharaan preventif berbasis jarak tempuh akan salah besar. |

---

## 2. Rincian Detil Temuan

### A. Duplikasi ID Unik
Kolom Primary Key yang seharusnya unik ditemukan memiliki data ganda:
* **Trips (`trip_id`):** 21 Duplikat
* **Transactions (`transaction_id`):** 14 Duplikat
* **Maintenance Records (`record_id`):** 12 Duplikat
* **Incidents (`incident_id`):** 13 Duplikat

*Catatan: Kolom ID Pelanggan (`customer_id` di `ds2_customers`), ID Kendaraan Utama (`vehicle_id` di `ds1_vehicles`), ID Armada Teknis (`fleet_vehicle_id` di `ds3_fleet_vehicles`), dan ID Polis (`policy_id` di `ds4_insurance_policies`) terbukti 100% unik.*

### B. Masalah Integritas Referensial (Foreign Key Mismatch)
* **Krisis ID Pelanggan di Trips:** Dari 5.000 perjalanan, hampir semuanya (**4.980 baris**) menggunakan `customer_id` yang tidak terdaftar di daftar pelanggan utama (`ds2_customers.csv`). Hal ini menunjukkan adanya ketidakcocokan antara sistem pelacakan perjalanan (*Trips*) dengan sistem registrasi pelanggan (*CRM*).
* **Kebocoran 200 Baris (Margin of Error):** Ada pola di mana tepat **200 baris** di `ds1_trips` (ke `vehicle_id`), `ds2_transactions` (ke `customer_id`), `ds3_maintenance` (ke `fleet_vehicle_id`), dan `ds4_incidents` (ke `policy_id`) tidak memiliki data induk di tabel utama. Pola "200 baris" yang seragam ini sangat mencurigakan dan kemungkinan merupakan anomali yang sengaja dimasukkan dalam simulasi.

### C. Anomali Logika Waktu & Jarak Tempuh
* **Waktu Perjalanan Terbalik:** Sebanyak **2.466 baris** di `ds1_trips.csv` memiliki waktu selesai (`trip_end_time`) yang terjadi **sebelum** waktu mulai (`trip_start_time`).
* **Jarak Tempuh Perawatan Menurun:** Sebanyak **2.315 baris** di `ds3_maintenance_records.csv` mencatat bahwa jarak tempuh untuk servis berikutnya lebih kecil daripada jarak tempuh saat kendaraan diservis.

---

## 3. Langkah Rekomendasi Pembersihan Data (Data Cleaning Plan)

Kita harus mendiskusikan bagaimana menangani anomali ini sebelum melakukan analisis lebih lanjut:
1. **Mengatasi Duplikat ID:** Menghapus baris duplikat atau memperbarui ID-nya jika ada record yang berbeda.
2. **Memperbaiki Logika Tanggal & Jarak:** 
   - Untuk tanggal terbalik di `trips`, kita bisa menukar nilai `trip_start_time` dan `trip_end_time` pada baris yang salah.
   - Untuk odometer terbalik di `maintenance`, kita bisa menukar nilai `mileage_at_service` dan `next_service_mileage` atau mengoreksinya berdasarkan rata-rata jarak tempuh.
3. **Mengatasi Kunci Referensi yang Hilang (Foreign Keys Mismatch):**
   - Menghapus 200 baris yatim-piatu (*orphan rows*) tersebut atau menandainya dengan kategori "Unknown".
   - Menyelidiki apakah `customer_id` di trips bisa dipetakan ulang atau apakah ada perbedaan format penulisan ID.
