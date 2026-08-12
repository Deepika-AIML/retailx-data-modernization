import time
import subprocess
import os

def run_script(script_name, description):
    print(f"\n==================================================")
    print(f"▶️  EXECUTING: {description} ({script_name})")
    print(f"==================================================")
    start_time = time.time()
    
    script_path = os.path.join("scripts", script_name)
    result = subprocess.run(["python", script_path], capture_output=False)
    
    elapsed = time.time() - start_time
    if result.returncode == 0:
        print(f"✅ {script_name} completed successfully in {elapsed:.2f}s!")
    else:
        print(f"❌ ERROR in {script_name}! Pipeline execution aborted.")
        exit(1)

def main():
    print("🚀 STARTING RETAILX DATA MODERNIZATION END-TO-END PIPELINE")
    pipeline_start = time.time()
    
    # 1. Generate Synthetic Raw Source Data
    run_script("generate_data.py", "Phase 1: Raw Data Generation (CSV & Excel)")
    
    # 2. Ingest Disparate Sources into Bronze Parquet Lakehouse
    run_script("ingest_to_bronze.py", "Phase 2: Ingestion to Bronze Layer")
    
    # 3. Clean, Deduplicate & Quarantine Data into Silver
    run_script("process_to_silver.py", "Phase 3: Data Cleaning & Quarantine to Silver Layer")
    
    # 4. Transform into Star Schema & Aggregates in Gold
    run_script("process_to_gold.py", "Phase 4: Dimensional Star Schema Modeling to Gold Layer")
    
    total_time = time.time() - pipeline_start
    print(f"\n==================================================")
    print(f"🎉 RETAILX MEDALLION PIPELINE COMPLETED SUCCESSFULLY!")
    print(f"⏱️  Total Execution Time: {total_time:.2f} seconds")
    print(f"==================================================")

if __name__ == "__main__":
    main()