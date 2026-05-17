import os
import pandas as pd
import numpy as np

def run_cleaning():
    data_dir = r"c:\Users\hpvic\OneDrive\Documents\Finance of Robotaxi"
    cleaned_dir = os.path.join(data_dir, "cleaned_data")
    os.makedirs(cleaned_dir, exist_ok=True)
    
    print("--- Memulai Data Cleaning Pipeline ---")
    
    # 1. Load Data
    trips = pd.read_csv(os.path.join(data_dir, 'ds1_trips.csv'))
    vehicles_ds1 = pd.read_csv(os.path.join(data_dir, 'ds1_vehicles.csv'))
    customers = pd.read_csv(os.path.join(data_dir, 'ds2_customers.csv'))
    transactions = pd.read_csv(os.path.join(data_dir, 'ds2_transactions.csv'))
    fleet_vehicles_ds3 = pd.read_csv(os.path.join(data_dir, 'ds3_fleet_vehicles.csv'))
    maintenance = pd.read_csv(os.path.join(data_dir, 'ds3_maintenance_records.csv'))
    incidents = pd.read_csv(os.path.join(data_dir, 'ds4_incidents.csv'))
    insurance = pd.read_csv(os.path.join(data_dir, 'ds4_insurance_policies.csv'))
    
    # 2. Drop Duplicates
    trips = trips.drop_duplicates(subset=['trip_id'], keep='first')
    transactions = transactions.drop_duplicates(subset=['transaction_id'], keep='first')
    maintenance = maintenance.drop_duplicates(subset=['record_id'], keep='first')
    incidents = incidents.drop_duplicates(subset=['incident_id'], keep='first')
    print("[OK] Duplikasi ID unik dihapus.")
    
    # 3. Drop Orphan Rows (Tepat 200 Baris)
    transactions = transactions[transactions['customer_id'].isin(customers['customer_id'])]
    maintenance = maintenance[maintenance['fleet_vehicle_id'].isin(fleet_vehicles_ds3['fleet_vehicle_id'])]
    incidents = incidents[incidents['policy_id'].isin(insurance['policy_id'])]
    print("[OK] Baris yatim-piatu (orphan records) dihapus.")
    
    # 4. Modulo Key Repair (Integritas Referensial Trips)
    cust_list = customers['customer_id'].tolist()
    trips['customer_id'] = trips['customer_id'].apply(lambda x: cust_list[x % len(cust_list)])
    
    veh_list = vehicles_ds1['vehicle_id'].tolist()
    trips['vehicle_id'] = trips['vehicle_id'].apply(lambda x: veh_list[x % len(veh_list)])
    print("[OK] Kunci referensial Trips diperbaiki dengan Modulo Key Repair.")
    
    # 5. Koreksi Tanggal Perjalanan (Same-Day & Midnight Cross)
    start_dt = pd.to_datetime(trips['trip_start_time'])
    end_dt = pd.to_datetime(trips['trip_end_time'])
    
    cleaned_end_dt = start_dt.dt.normalize() + pd.to_timedelta(end_dt.dt.time.astype(str))
    mask = cleaned_end_dt < start_dt
    cleaned_end_dt.loc[mask] = cleaned_end_dt.loc[mask] + pd.Timedelta(days=1)
    
    trips['trip_start_time'] = start_dt.dt.strftime('%Y-%m-%d %H:%M:%S')
    trips['trip_end_time'] = cleaned_end_dt.dt.strftime('%Y-%m-%d %H:%M:%S')
    trips['trip_duration_mins'] = round((cleaned_end_dt - start_dt).dt.total_seconds() / 60.0, 2)
    print("[OK] Logika tanggal perjalanan dikoreksi (Same-Day & Midnight Cross).")
    
    # 6. Koreksi Odometer Bengkel (Swap Mileage)
    mask_m = maintenance['next_service_mileage'] < maintenance['mileage_at_service']
    maintenance.loc[mask_m, 'mileage_at_service'], maintenance.loc[mask_m, 'next_service_mileage'] = (
        maintenance.loc[mask_m, 'next_service_mileage'],
        maintenance.loc[mask_m, 'mileage_at_service']
    )
    print("[OK] Odometer terbalik pada catatan pemeliharaan ditukar.")
    
    # 7. Pengisian Missing Values
    trips['cancellation_reason'] = trips['cancellation_reason'].fillna('Not Cancelled')
    print("[OK] Missing values diisi.")
    
    # 8. Simpan
    trips.to_csv(os.path.join(cleaned_dir, 'ds1_trips_cleaned.csv'), index=False)
    vehicles_ds1.to_csv(os.path.join(cleaned_dir, 'ds1_vehicles_cleaned.csv'), index=False)
    customers.to_csv(os.path.join(cleaned_dir, 'ds2_customers_cleaned.csv'), index=False)
    transactions.to_csv(os.path.join(cleaned_dir, 'ds2_transactions_cleaned.csv'), index=False)
    fleet_vehicles_ds3.to_csv(os.path.join(cleaned_dir, 'ds3_fleet_vehicles_cleaned.csv'), index=False)
    maintenance.to_csv(os.path.join(cleaned_dir, 'ds3_maintenance_records_cleaned.csv'), index=False)
    incidents.to_csv(os.path.join(cleaned_dir, 'ds4_incidents_cleaned.csv'), index=False)
    insurance.to_csv(os.path.join(cleaned_dir, 'ds4_insurance_policies_cleaned.csv'), index=False)
    
    print(f"[OK] Seluruh data bersih disimpan di: {cleaned_dir}")
    print("--- Data Cleaning Selesai ---")

if __name__ == "__main__":
    run_cleaning()
