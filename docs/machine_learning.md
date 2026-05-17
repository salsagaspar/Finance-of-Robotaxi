# 🤖 Machine Learning Modeling: Churn Prediction

Tahap ini mendokumentasikan proses pelatihan model prediktif **Machine Learning (Predictive Analytics)** untuk memprediksi pelanggan dengan **Risiko Churn Tinggi (*High Churn Risk*)** menggunakan data pelanggan Robotaxi. Seluruh skrip otomatisasi pelatihan disimpan di file [scripts/train_churn_model.py](file:///c:/Users/hpvic/OneDrive/Documents/Finance%20of%20Robotaxi/scripts/train_churn_model.py) dan didokumentasikan interaktif pada Jupyter Notebook [notebooks/04_machine_learning_modeling.ipynb](file:///c:/Users/hpvic/OneDrive/Documents/Finance%20of%20Robotaxi/notebooks/04_machine_learning_modeling.ipynb).

---

## 1. Definisi Masalah & Variabel Target

* **Definisi Bisnis:** Mengidentifikasi pelanggan yang memiliki probabilitas tinggi untuk berhenti menggunakan layanan Robotaxi kita (*churn*), agar tim pemasaran dapat memberikan promo khusus secara proaktif.
* **Target Pemodelan:** Churn diklasifikasikan sebagai masalah klasifikasi biner:
  * **Class 1 (High Churn Risk):** `churn_risk_score` > 0.5 (Tinggi)
  * **Class 0 (Low Churn Risk):** `churn_risk_score` ≤ 0.5 (Rendah)
* **Ketidakseimbangan Kelas (Class Imbalance):**
  * Class 0: **89.3%** (4.465 pelanggan)
  * Class 1: **10.7%** (535 pelanggan)

---

## 2. Rekayasa Fitur & Preprocessing

Fitur yang digunakan untuk membangun model mencakup:
* **Fitur Numerik:** `total_trips` (jumlah perjalanan), `total_spent_usd` (total belanja), `avg_rating_given` (peringkat rata-rata dari pelanggan), `lifetime_value_usd` (nilai seumur hidup pelanggan), `promo_eligible_flag` (status kelayakan promo), dan `days_since_joined` (umur keanggotaan dalam hari).
* **Fitur Kategorikal:** `loyalty_tier`, `subscription_plan`, `preferred_payment`, `account_status`, `referral_source`, `age_group`, `gender`, dan `city`.

**Pipeline Preprocessing (Scikit-Learn ColumnTransformer):**
1. Fitur numerik distandardisasi dengan `StandardScaler`.
2. Fitur kategorikal di-encode dengan `OneHotEncoder` untuk menangani nilai baru di masa depan secara aman.

---

## 3. Pelatihan & Performa Model

Kami memilih algoritma **Random Forest Classifier** yang kuat, dengan mengaktifkan penanganan ketidakseimbangan kelas menggunakan parameter `class_weight='balanced'`.

### Hasil Evaluasi Awal:
* **Akurasi Model:** **89.30%**
* **ROC-AUC Score:** **48.74%**

---

## 4. Temuan Kritis & Diagnostik Data (World-Class Data Science Insights) ⚠️

Sebagai seorang Data Scientist profesional, kami menganalisis mengapa model memiliki akurasi yang tinggi (89.30%) namun nilai ROC-AUC yang sangat rendah (48.74% - setara tebakan koin acak):

### A. Penyebab Utamanya: Korelasi Nol (Zero Correlation)
Ketika kami melakukan visualisasi korelasi linier pada dataset, kami menemukan temuan yang sangat mencengangkan:
* Korelasi `total_trips` vs `churn_risk_score`: **0.0068**
* Korelasi `avg_rating_given` vs `churn_risk_score`: **0.0013**
* Korelasi `total_spent_usd` vs `churn_risk_score`: **0.0009**

> [!WARNING]
> Korelasi seluruh fitur terhadap target churn **berkisar di angka 0.00**. Ini berarti variabel `churn_risk_score` dalam dataset ini dihasilkan secara acak (*random noise*), yang merupakan karakteristik khas dari **data sintetis/simulasi**. 
> 
> Tidak ada pola matematis asli yang menghubungkan profil pelanggan dengan risiko churn mereka. Oleh karena itu, model machine learning mana pun tidak akan mampu memprediksi target ini dengan performa prediktif di atas tebakan acak.

### B. Rekomendasi untuk Dunia Industri Nyata:
Di industri nyata, temuan diagnostik ini akan menghasilkan **tindakan strategis yang sangat berharga**:
1. **Rapat Evaluasi Produk:** Menyarankan kepada tim Product & Engineering untuk mengumpulkan fitur prediktif yang lebih kuat (seperti: frekuensi aplikasi crash, lama waktu tunggu jemput taksi, respon pengguna terhadap lonjakan tarif).
2. **Koreksi Data Pipeline:** Menyelidiki apakah ada kesalahan penyimpanan data di log server yang menyebabkan nilai churn ter-acak.

---

## 5. Deployment Model

Trained pipeline (termasuk preprocessing scaler dan random forest classifier) telah berhasil disimpan dalam format biner ter-serialisasi:
📂 **[models/churn_classifier.pkl](file:///c:/Users/hpvic/OneDrive/Documents/Finance%20of%20Robotaxi/models/churn_classifier.pkl)**

Model ini siap di-load oleh dashboard Plotly Dash untuk memprediksi risiko pelanggan secara langsung di masa depan jika data fitur baru dimasukkan!
