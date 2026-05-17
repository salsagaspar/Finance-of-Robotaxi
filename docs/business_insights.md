# 📊 Executive Summary: Finansial & Operasional Insights Robotaxi

Dokumen ini menyajikan temuan utama dan wawasan bisnis (business insights) dari analisis eksploatif data (**Exploratory Data Analysis - EDA**) terhadap armada Robotaxi. Analisis ini ditujukan kepada tim C-Level (CEO, CFO, COO) untuk segera mengambil keputusan strategis guna menghentikan "kebocoran biaya" (*cost leaks*) dan memaksimalkan laba bersih.

---

## 1. Tiga Kebocoran Biaya Terbesar (The Big 3 Cost Leaks)

Berdasarkan hasil pengolahan data bersih di notebook [notebooks/03_exploratory_data_analysis.ipynb](file:///c:/Users/hpvic/OneDrive/Documents/Finance%20of%20Robotaxi/notebooks/03_exploratory_data_analysis.ipynb), perusahaan kita mengalami tiga masalah struktural yang sangat serius dari sisi operasional dan finansial:

### A. Kebocoran Pemeliharaan (The Maintenance Cost Black Hole) 🕳️
* **Angka Kritis:** 
  * Pendapatan Bersih Perjalanan: **$242,009.53**
  * Total Biaya Pemeliharaan Armada: **$1,343,102.67**
  * **Rasio Kerugian:** Biaya perawatan armada mencapai **5.5 kali lipat** dari seluruh pendapatan perjalanan taksi kita!
* **Analisis Masalah:**
  * Layanan terbanyak adalah *Routine Check* (1.149 kali) dengan biaya total **$322,182.03** dan *Battery Service* (653 kali) sebesar **$178,879.44**.
  * Rata-rata biaya per servis di seluruh kategori (mulai dari pembersihan mendalam hingga pembaruan software) seragam di kisaran **$260 s/d $300**. Hal ini tidak logis secara operasional (misalnya: masa biaya cuci mobil/deep clean hampir sama dengan brake replacement?). Ini mengindikasikan adanya pemborosan sistematis atau pihak vendor perawatan yang mengenakan tarif berlebihan (*overcharging*).
* **Rekomendasi Strategis:**
  * Negosiasi ulang kontrak vendor atau buat bengkel internal (*in-house maintenance*) untuk menekan biaya per servis rutin.
  * Terapkan penjadwalan pemeliharaan prediktif berbasis AI untuk melakukan servis hanya saat benar-benar dibutuhkan.

### B. Beban Pengemudi Keselamatan (The Safety Driver Financial Burden) 👤
* **Angka Kritis:**
  * Nilai Transaksi Kotor (GTV): **$296,164.35**
  * Pembayaran Pengemudi Keselamatan (*Driver Payout*): **$182,799.38**
  * **Rasio Pengeluaran:** Pembayaran pengemudi menyedot **61.7% dari total nilai transaksi kotor** perusahaan!
* **Analisis Masalah:**
  * Meskipun bisnis kita dipasarkan sebagai layanan "Robotaxi Otonom", laporan transaksi menunjukkan kita masih mengeluarkan biaya yang sangat besar untuk pengemudi keselamatan di dalam kendaraan (*safety drivers*). 
  * Dari sisa transaksi setelah dipotong pengemudi, perusahaan hanya mendapatkan pendapatan bersih (*Net Revenue*) sebesar **$98,290.40** (33.2% dari GTV). Ini berarti model bisnis saat ini masih sangat bergantung pada tenaga manusia dan belum sepenuhnya menikmati efisiensi armada otonom.
* **Rekomendasi Strategis:**
  * Percepat program pengujian tanpa pengemudi (*driverless operation*) di area tertentu untuk mengeliminasi kebutuhan pengemudi keselamatan. Jika biaya driver ini dihilangkan, margin laba bersih operasional kita akan melonjak sebesar 185%!

### C. Pemborosan Premi Asuransi (The Insurance Premium Leverage) 🛡️
* **Angka Kritis:**
  * Premi Bulanan yang Dibayar ke Provider: **$89,735,549.88 (per tahun)**
  * Penyelesaian Klaim Insiden dari Provider: **$19,998,685.26**
  * **Loss Ratio Asuransi:** Hanya **22.29%**!
* **Analisis Masalah:**
  * Kita membayar premi asuransi tahunan yang sangat fantastis senilai **$89.7 Juta** untuk 5.000 kendaraan. Ini berarti premi bulanan rata-rata per mobil berkisar di angka $1.500 (sangat mahal!).
  * Namun, tingkat keselamatan armada kita sangat tinggi. Sepanjang periode data, total kerugian dari kecelakaan/insiden yang diklaim hanya sebesar **$20 Juta**.
  * Di industri asuransi, rasio kerugian (*Loss Ratio*) 22% adalah keuntungan yang terlampau besar bagi perusahaan asuransi, dan kerugian efisiensi kas bagi kita selaku nasabah.
* **Rekomendasi Strategis:**
  * Gunakan data keselamatan ini sebagai **alat negosiasi yang kuat** dengan perusahaan asuransi. Tunjukkan bahwa armada Robotaxi otonom kita jauh lebih aman dibanding pengemudi manusia biasa.
  * Minta penurunan premi tahunan sebesar 40% hingga 50%, yang berpotensi langsung menghemat kas perusahaan sebesar **$35 Juta s/d $45 Juta per tahun**!

---

## 2. Rincian Metrik & Distribusi Data

### Distribusi Status Perjalanan (Trips Status)
Dari 4.979 perjalanan yang terekam, tingkat keberhasilan perjalanan adalah:
* **Completed (Berhasil):** 3.581 perjalanan (71.9%)
* **Cancelled (Dibatalkan):** 589 perjalanan (11.8%)
* **No Show (Penumpang Tidak Datang):** 260 perjalanan (5.2%)
* **Refunded (Dikembalikan):** 241 perjalanan (4.8%)
* **In Progress (Sedang Berjalan):** 308 perjalanan (6.2%)

*Kebocoran Operasional:* Sebanyak **21.8% perjalanan gagal diselesaikan** (Cancelled + No Show + Refunded), yang berarti 1 dari 5 perjalanan membuang waktu utilisasi armada tanpa menghasilkan pendapatan optimal.

### Distribusi Kerugian Berdasarkan Jenis Insiden (Incidents)
Ketika terjadi kecelakaan, jenis insiden yang menelan biaya ganti rugi terbesar dari asuransi adalah:
1. **Collision (Tabrakan):** Total Ganti Rugi = **$4,625,866.05** (1.153 insiden)
2. **Minor Scratch (Goresan Ringan):** Total Ganti Rugi = **$3,453,633.60** (842 insiden)
3. **Vandalism (Vandalisme):** Total Ganti Rugi = **$2,294,609.58** (529 insiden)

*Wawasan Tambahan:* Meskipun frekuensi tabrakan tinggi, biaya rata-rata per kecelakaan seragam di angka **$4.000 s/d $4.500** untuk seluruh tipe insiden (mulai dari goresan ringan hingga kecelakaan pejalan kaki). Hal ini menunjukkan adanya kebijakan penaksiran kerusakan yang tidak proporsional dari pihak bengkel rekanan asuransi.
