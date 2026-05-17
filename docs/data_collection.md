# Data Collection & Identification

Tahap ini mendokumentasikan identifikasi dan akuisisi data dari 8 dataset yang tersedia di folder proyek `Finance of Robotaxi`. Setiap berkas telah diidentifikasi ukuran, dimensi, dan skema kolomnya untuk memahami hubungan antardata.

## 1. Ringkasan Dataset (Dataset Overview)

| Nama File | Kategori / Deskripsi | Ukuran (KB) | Jumlah Baris | Jumlah Kolom |
| :--- | :--- | :--- | :--- | :--- |
| `ds1_trips.csv` | Operasional - Data Perjalanan Robotaxi | 832.11 KB | 5,000 | 20 |
| `ds1_vehicles.csv` | Operasional - Data Metadata Kendaraan Utama | 624.95 KB | 5,000 | 20 |
| `ds2_customers.csv` | Finansial & Customer - Data Profil Pelanggan | 686.46 KB | 5,000 | 20 |
| `ds2_transactions.csv` | Finansial & Customer - Data Riwayat Transaksi/Pembayaran | 608.58 KB | 5,000 | 20 |
| `ds3_fleet_vehicles.csv` | Pemeliharaan - Data Detail Teknis Armada Aktif | 749.75 KB | 5,000 | 20 |
| `ds3_maintenance_records.csv` | Pemeliharaan - Catatan Bengkel & Perbaikan Kendaraan | 708.99 KB | 5,000 | 20 |
| `ds4_incidents.csv` | Risiko & Asuransi - Data Kejadian Kecelakaan/Insiden | 692.46 KB | 5,000 | 20 |
| `ds4_insurance_policies.csv` | Risiko & Asuransi - Polis Asuransi Armada | 624.2 KB | 5,000 | 20 |

## 2. Struktur Detil Setiap Dataset (Schema & Dtypes)

### `ds1_trips.csv` (Operasional - Data Perjalanan Robotaxi)
- **Dimensi:** 5,000 baris x 20 kolom

| Nama Kolom | Tipe Data (Pandas) | Jumlah Null (Missing) | Nilai Unik | Contoh Nilai |
| :--- | :--- | :--- | :--- | :--- |
| `trip_id` | `int64` | 0 | 4,979 | `279785` |
| `vehicle_id` | `int64` | 0 | 3,284 | `565894` |
| `customer_id` | `int64` | 0 | 3,286 | `570780` |
| `trip_start_time` | `object` | 0 | 5,000 | `2023-02-25 22:18:14` |
| `trip_end_time` | `object` | 0 | 5,000 | `2024-03-09 10:15:45` |
| `pickup_lat` | `float64` | 0 | 5,000 | `44.691291` |
| `pickup_lon` | `float64` | 0 | 5,000 | `-101.407407` |
| `dropoff_lat` | `float64` | 0 | 5,000 | `33.293086` |
| `dropoff_lon` | `float64` | 0 | 4,999 | `-87.385431` |
| `distance_km` | `float64` | 0 | 1,839 | `4.39` |
| `fare_amount_usd` | `float64` | 0 | 3,837 | `87.7` |
| `surge_multiplier` | `float64` | 0 | 7 | `1.0` |
| `payment_method` | `object` | 0 | 6 | `Credit Card` |
| `trip_status` | `object` | 0 | 5 | `Completed` |
| `passenger_rating` | `int64` | 0 | 5 | `3` |
| `cancellation_reason` | `object` | 3,584 | 4 | `Passenger Cancel` |
| `route_type` | `object` | 0 | 5 | `Highway` |
| `weather_condition` | `object` | 0 | 7 | `Clear` |
| `traffic_level` | `object` | 0 | 4 | `Low` |
| `discount_applied_usd` | `int64` | 0 | 5 | `15` |

---

### `ds1_vehicles.csv` (Operasional - Data Metadata Kendaraan Utama)
- **Dimensi:** 5,000 baris x 20 kolom

| Nama Kolom | Tipe Data (Pandas) | Jumlah Null (Missing) | Nilai Unik | Contoh Nilai |
| :--- | :--- | :--- | :--- | :--- |
| `vehicle_id` | `int64` | 0 | 5,000 | `100000` |
| `make` | `object` | 0 | 8 | `Tesla` |
| `model` | `object` | 0 | 8 | `Leaf` |
| `year` | `int64` | 0 | 7 | `2024` |
| `color` | `object` | 0 | 7 | `Gray` |
| `vehicle_type` | `object` | 0 | 4 | `SUV` |
| `home_city` | `object` | 0 | 10 | `Dallas` |
| `battery_capacity_kwh` | `int64` | 0 | 6 | `131` |
| `range_km` | `int64` | 0 | 330 | `322` |
| `purchase_price_usd` | `int64` | 0 | 4,792 | `69636` |
| `monthly_insurance_usd` | `float64` | 0 | 4,718 | `311.76` |
| `registration_state` | `object` | 0 | 8 | `CA` |
| `fleet_zone` | `object` | 0 | 5 | `Zone-E` |
| `operational_status` | `object` | 0 | 5 | `Maintenance` |
| `last_maintenance_date` | `object` | 0 | 821 | `2023-12-18` |
| `total_trips_completed` | `int64` | 0 | 3,808 | `4091` |
| `total_km_driven` | `int64` | 0 | 4,958 | `245814` |
| `charge_level_pct` | `int64` | 0 | 95 | `22` |
| `assigned_depot` | `object` | 0 | 5 | `Depot-Central` |
| `depreciation_rate_pct` | `float64` | 0 | 1,364 | `19.73` |

---

### `ds2_customers.csv` (Finansial & Customer - Data Profil Pelanggan)
- **Dimensi:** 5,000 baris x 20 kolom

| Nama Kolom | Tipe Data (Pandas) | Jumlah Null (Missing) | Nilai Unik | Contoh Nilai |
| :--- | :--- | :--- | :--- | :--- |
| `customer_id` | `int64` | 0 | 5,000 | `100074` |
| `first_name` | `object` | 0 | 14 | `Chris` |
| `last_name` | `object` | 0 | 12 | `Taylor` |
| `email_domain` | `object` | 0 | 5 | `gmail.com` |
| `phone_area_code` | `int64` | 0 | 796 | `967` |
| `join_date` | `object` | 0 | 1,754 | `2025-02-16` |
| `city` | `object` | 0 | 10 | `San Francisco` |
| `loyalty_tier` | `object` | 0 | 5 | `Silver` |
| `total_trips` | `int64` | 0 | 449 | `170` |
| `total_spent_usd` | `float64` | 0 | 4,748 | `216.83` |
| `avg_rating_given` | `float64` | 0 | 26 | `2.6` |
| `preferred_payment` | `object` | 0 | 5 | `Credit Card` |
| `account_status` | `object` | 0 | 5 | `Active` |
| `referral_source` | `object` | 0 | 7 | `Google Ads` |
| `age_group` | `object` | 0 | 6 | `45-54` |
| `gender` | `object` | 0 | 4 | `Female` |
| `subscription_plan` | `object` | 0 | 5 | `Free` |
| `churn_risk_score` | `float64` | 0 | 713 | `0.175` |
| `lifetime_value_usd` | `float64` | 0 | 4,776 | `19.51` |
| `promo_eligible_flag` | `int64` | 0 | 2 | `1` |

---

### `ds2_transactions.csv` (Finansial & Customer - Data Riwayat Transaksi/Pembayaran)
- **Dimensi:** 5,000 baris x 20 kolom

| Nama Kolom | Tipe Data (Pandas) | Jumlah Null (Missing) | Nilai Unik | Contoh Nilai |
| :--- | :--- | :--- | :--- | :--- |
| `transaction_id` | `int64` | 0 | 4,986 | `881267` |
| `customer_id` | `int64` | 0 | 3,305 | `783324` |
| `zone_id` | `int64` | 0 | 3,240 | `805734` |
| `transaction_date` | `object` | 0 | 847 | `2024-01-21` |
| `gross_amount_usd` | `float64` | 0 | 4,096 | `60.46` |
| `tax_amount_usd` | `float64` | 0 | 1,428 | `6.44` |
| `tip_amount_usd` | `int64` | 0 | 7 | `2` |
| `refund_amount_usd` | `int64` | 0 | 5 | `0` |
| `payment_method` | `object` | 0 | 6 | `Debit Card` |
| `payment_status` | `object` | 0 | 6 | `Pending` |
| `promo_code_used` | `object` | 0 | 6 | `SAVE20` |
| `discount_pct` | `int64` | 0 | 6 | `10` |
| `platform_fee_usd` | `float64` | 0 | 401 | `3.72` |
| `driver_payout_usd` | `float64` | 0 | 3,608 | `38.64` |
| `net_revenue_usd` | `float64` | 0 | 2,797 | `9.58` |
| `currency` | `object` | 0 | 3 | `USD` |
| `billing_cycle` | `object` | 0 | 4 | `Weekly` |
| `invoice_number` | `int64` | 0 | 4,998 | `1785802` |
| `reconciliation_status` | `object` | 0 | 4 | `Reconciled` |
| `dispute_flag` | `int64` | 0 | 2 | `0` |

---

### `ds3_fleet_vehicles.csv` (Pemeliharaan - Data Detail Teknis Armada Aktif)
- **Dimensi:** 5,000 baris x 20 kolom

| Nama Kolom | Tipe Data (Pandas) | Jumlah Null (Missing) | Nilai Unik | Contoh Nilai |
| :--- | :--- | :--- | :--- | :--- |
| `fleet_vehicle_id` | `int64` | 0 | 5,000 | `100416` |
| `vin` | `object` | 0 | 5,000 | `WBA56360706172` |
| `make` | `object` | 0 | 8 | `Cruise` |
| `model` | `object` | 0 | 8 | `e-tron` |
| `year` | `int64` | 0 | 7 | `2024` |
| `acquisition_date` | `object` | 0 | 1,954 | `2024-02-21` |
| `acquisition_cost_usd` | `int64` | 0 | 4,788 | `39135` |
| `current_value_usd` | `int64` | 0 | 4,803 | `40083` |
| `odometer_km` | `int64` | 0 | 4,946 | `261240` |
| `battery_health_pct` | `int64` | 0 | 45 | `56` |
| `software_version` | `object` | 0 | 6 | `v5.2` |
| `hardware_revision` | `object` | 0 | 4 | `HW4.0` |
| `depot_location` | `object` | 0 | 5 | `Depot-Central` |
| `operational_zone` | `object` | 0 | 5 | `Zone-A` |
| `vehicle_class` | `object` | 0 | 5 | `Premium` |
| `lease_or_owned` | `object` | 0 | 4 | `Owned` |
| `lease_expiry_date` | `object` | 0 | 1,706 | `2026-08-10` |
| `compliance_status` | `object` | 0 | 4 | `Compliant` |
| `last_inspection_date` | `object` | 0 | 670 | `2025-03-23` |
| `decommission_flag` | `int64` | 0 | 2 | `0` |

---

### `ds3_maintenance_records.csv` (Pemeliharaan - Catatan Bengkel & Perbaikan Kendaraan)
- **Dimensi:** 5,000 baris x 20 kolom

| Nama Kolom | Tipe Data (Pandas) | Jumlah Null (Missing) | Nilai Unik | Contoh Nilai |
| :--- | :--- | :--- | :--- | :--- |
| `record_id` | `int64` | 0 | 4,988 | `179405` |
| `fleet_vehicle_id` | `int64` | 0 | 3,308 | `905300` |
| `technician_id` | `int64` | 0 | 3,297 | `566177` |
| `service_date` | `object` | 0 | 1,168 | `2023-03-04` |
| `service_type` | `object` | 0 | 10 | `Software Update` |
| `parts_cost_usd` | `float64` | 0 | 4,604 | `110.4` |
| `labor_cost_usd` | `float64` | 0 | 4,553 | `115.38` |
| `total_cost_usd` | `float64` | 0 | 4,443 | `105.28` |
| `downtime_hours` | `float64` | 0 | 278 | `21.4` |
| `mileage_at_service` | `int64` | 0 | 4,958 | `289193` |
| `next_service_mileage` | `int64` | 0 | 4,968 | `37326` |
| `warranty_claim` | `int64` | 0 | 2 | `1` |
| `fault_code` | `object` | 0 | 10 | `F020` |
| `severity_level` | `object` | 0 | 4 | `Low` |
| `repair_status` | `object` | 0 | 5 | `Completed` |
| `vendor_name` | `object` | 0 | 7 | `UrbanMech` |
| `invoice_number` | `int64` | 0 | 4,999 | `1730171` |
| `approval_status` | `object` | 0 | 3 | `Approved` |
| `estimated_hours` | `float64` | 0 | 156 | `10.9` |
| `actual_hours` | `float64` | 0 | 196 | `7.2` |

---

### `ds4_incidents.csv` (Risiko & Asuransi - Data Kejadian Kecelakaan/Insiden)
- **Dimensi:** 5,000 baris x 20 kolom

| Nama Kolom | Tipe Data (Pandas) | Jumlah Null (Missing) | Nilai Unik | Contoh Nilai |
| :--- | :--- | :--- | :--- | :--- |
| `incident_id` | `int64` | 0 | 4,987 | `689223` |
| `policy_id` | `int64` | 0 | 3,324 | `666363` |
| `geo_zone_id` | `int64` | 0 | 3,304 | `854853` |
| `incident_date` | `object` | 0 | 1,170 | `2024-04-01` |
| `incident_type` | `object` | 0 | 10 | `Minor Scratch` |
| `severity` | `object` | 0 | 4 | `Minor` |
| `fault_determination` | `object` | 0 | 6 | `No Fault` |
| `claim_amount_usd` | `float64` | 0 | 4,894 | `1030.77` |
| `settlement_amount_usd` | `float64` | 0 | 4,981 | `2457.92` |
| `deductible_paid_usd` | `int64` | 0 | 6 | `1000` |
| `injuries_count` | `int64` | 0 | 6 | `0` |
| `property_damage_flag` | `int64` | 0 | 2 | `1` |
| `police_report_filed` | `int64` | 0 | 2 | `0` |
| `legal_action_flag` | `int64` | 0 | 2 | `0` |
| `investigation_status` | `object` | 0 | 6 | `Closed` |
| `resolution_date` | `object` | 0 | 1,142 | `2025-01-23` |
| `repair_cost_usd` | `float64` | 0 | 4,986 | `1228.17` |
| `liability_pct` | `int64` | 0 | 5 | `100` |
| `reimbursement_status` | `object` | 0 | 5 | `Pending` |
| `incident_code` | `object` | 0 | 10 | `INC-B` |

---

### `ds4_insurance_policies.csv` (Risiko & Asuransi - Polis Asuransi Armada)
- **Dimensi:** 5,000 baris x 20 kolom

| Nama Kolom | Tipe Data (Pandas) | Jumlah Null (Missing) | Nilai Unik | Contoh Nilai |
| :--- | :--- | :--- | :--- | :--- |
| `policy_id` | `int64` | 0 | 5,000 | `100073` |
| `provider_name` | `object` | 0 | 10 | `Nationwide` |
| `policy_type` | `object` | 0 | 5 | `Fleet Comprehensive` |
| `coverage_start_date` | `object` | 0 | 1,538 | `2023-05-21` |
| `coverage_end_date` | `object` | 0 | 1,277 | `2027-04-17` |
| `premium_monthly_usd` | `float64` | 0 | 4,962 | `555.47` |
| `deductible_amount_usd` | `int64` | 0 | 6 | `2500` |
| `coverage_limit_usd` | `int64` | 0 | 5 | `1000000` |
| `liability_coverage` | `int64` | 0 | 2 | `1` |
| `collision_coverage` | `int64` | 0 | 2 | `1` |
| `comprehensive_cov` | `int64` | 0 | 2 | `0` |
| `uninsured_motorist` | `int64` | 0 | 2 | `1` |
| `policy_status` | `object` | 0 | 5 | `Expired` |
| `renewal_count` | `int64` | 0 | 8 | `0` |
| `claims_count` | `int64` | 0 | 12 | `8` |
| `claims_total_value_usd` | `float64` | 0 | 4,994 | `9324.36` |
| `risk_category` | `object` | 0 | 4 | `High` |
| `discount_applied_pct` | `int64` | 0 | 7 | `10` |
| `agent_id` | `int64` | 0 | 4,848 | `91831` |
| `fleet_segment` | `object` | 0 | 5 | `Standard` |

---

## 3. Peta Hubungan Data (Data Relationship & Entity-Relationship Map)

Berdasarkan investigasi kolom identitas kunci (Keys), berikut adalah dugaan hubungan antar dataset yang bisa diintegrasikan:

1. **Relasi Operasional (Trips & Vehicles)**
   - `ds1_trips.csv` berelasi dengan `ds1_vehicles.csv` melalui kunci kunci kendaraan. *(Mari kita periksa nama kolom kuncinya nanti: misal `vehicle_id`)*

2. **Relasi Finansial & Customer**
   - `ds2_transactions.csv` berelasi dengan `ds2_customers.csv` melalui kolom `customer_id` (atau sejenisnya).
   - Layanan perjalanan `ds1_trips.csv` kemungkinan berelasi dengan `ds2_customers.csv` untuk mencocokkan perjalanan dengan pelanggan yang melakukan perjalanan.

3. **Relasi Pemeliharaan & Armada**
   - `ds3_maintenance_records.csv` berelasi dengan `ds3_fleet_vehicles.csv` melalui kunci kendaraan (`fleet_vehicle_id` atau `vehicle_id`).

4. **Relasi Risiko & Asuransi**
   - `ds4_incidents.csv` berelasi dengan `ds4_insurance_policies.csv` melalui kunci `policy_id`.
   - `ds4_incidents.csv` juga kemungkinan bisa dihubungkan ke data armada kendaraan/trip untuk melihat kendaraan mana yang mengalami kecelakaan.

---
*Catatan: Pada tahap eksplorasi berikutnya (Data Understanding), kita akan memverifikasi keselarasan kunci-kunci ini (apakah ID-nya cocok atau ada inkonsistensi).*
