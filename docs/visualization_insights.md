# 📊 Dashboard Visualisasi & Wawasan Interaktif (Plotly Dash)

Tahap ini mendokumentasikan aplikasi dashboard interaktif yang dibangun menggunakan **Plotly Dash** untuk menyajikan visualisasi data operasional dan simulasi keuangan Robotaxi secara profesional. Dashboard ini dirancang dengan gaya **Premium Dark Mode & Glassmorphism** untuk menyajikan data secara elegan kepada para eksekutif C-Level.

---

## 1. Desain Sistem & Arsitektur Dashboard

Seluruh kode dashboard diatur dengan arsitektur terpisah untuk kemudahan pemeliharaan (*clean code*):
1. **Logika Backend & Integrasi Data:** Ditulis di file utama [app.py](file:///c:/Users/hpvic/OneDrive/Documents/Finance%20of%20Robotaxi/app.py) menggunakan framework Dash, Flask, dan callback reaktif.
2. **Desain Tampilan & Layout (CSS):** Ditulis di file terpisah [assets/style.css](file:///c:/Users/hpvic/OneDrive/Documents/Finance%20of%20Robotaxi/assets/style.css) yang dimuat otomatis oleh Dash untuk memberikan efek transparansi kartu, gradasi teks neon, serta transisi hover yang mulus.
3. **Kustomisasi Visualisasi (Plotly figures):** Semua grafik menggunakan basis tema `plotly_dark` dengan latar belakang transparan (`rgba(0,0,0,0)`) dan palet warna terkurasi (seperti *Viridis*, *Magma*, *Coolwarm*) untuk estetika visual yang konsisten.

---

## 2. Struktur Modul & Fitur Dashboard

Dashboard memiliki panel navigasi samping (sidebar) untuk berpindah ke 6 halaman analisis utama:

### A. 📈 Executive Overview (Ringkasan Eksekutif)
* **Indikator KPI Utama:** Menampilkan kartu-kartu metrik besar yang bersinar (Pendapatan Bersih Perjalanan, Total Biaya Bengkel, Safety Driver Payout, Loss Ratio Aktual).
* **Kartu Peringatan Kebocoran (Alert Cards):** Menyajikan sorotan instan mengenai pembengkakan biaya pemeliharaan armada dan posisi tawar asuransi.
* **Grafik Rekonsiliasi:** Membandingkan pendapatan bersih dari tiket taksi vs biaya operasional bocor (pemeliharaan dan pembayaran driver).

### B. 🗺️ Perjalanan & Rute (Trips & Routes)
* **Kinerja Status Perjalanan:** Grafik Donut interaktif yang menampilkan tingkat penyelesaian perjalanan (Completed, Cancelled, No Show, Refunded).
* **Sebaran Jarak vs Tarif:** Scatter plot interaktif dari sampel 1.000 perjalanan untuk melihat pola penetapan tarif berdasarkan tipe rute (*Express, Standard, Eco*).

### C. 💳 Finansial & Transaksi
* **Alokasi Transaksi Kotor (GTV):** Pie chart yang membedah aliran dana GTV (61.7% habis untuk Driver Payout, 33.2% menjadi Net Revenue perusahaan, dan sisanya untuk pajak/refund).
* **Tren Harian GTV:** Grafik garis interaktif untuk memantau fluktuasi omzet harian.

### D. 👥 Perilaku Pelanggan
* **Metrik Loyalty Tier:** Grafik batang interaktif yang memetakan jumlah pengguna per level loyalitas (*Bronze, Silver, Gold, Platinum, Diamond*).
* **Kurva Risiko Churn:** Menampilkan tren risiko pelanggan berhenti menggunakan layanan taksi berdasarkan loyalty tier.

### E. 🔧 Pemeliharaan Armada (Maintenance)
* **Analisis Biaya Servis Bengkel:** Grafik batang horizontal berwarna gradasi *Magma* yang memetakan total pengeluaran bengkel di setiap jenis layanan (dari yang termahal *Routine Check* hingga *Deep Clean*).

### F. 🛡️ Manajemen Asuransi & Simulator Negosiasi
* **Sebaran Klaim Insiden:** Memvisualisasikan ganti rugi asuransi terbesar yang dipicu oleh tabrakan (*Collision*), goresan ringan (*Minor Scratch*), hingga vandalisme.
* **CFO Negotiation Tool (Simulator Interaktif):** Fitur slider interaktif di mana pengguna bisa memilih persentase diskon premi asuransi (0% s/d 60%) dan melihat secara langsung **jumlah kas tahunan yang berhasil dihemat** serta **estimasi nilai premi tahunan yang baru** secara real-time di layar.

---

## 3. Cara Menjalankan Dashboard Secara Lokal

Pastikan Anda berada di direktori proyek dan jalankan perintah berikut di terminal:

```bash
python app.py
```

Setelah server aktif, dashboard dapat diakses melalui browser Anda di alamat:
👉 **[http://127.0.0.1:8050/](http://127.0.0.1:8050/)**
