import subprocess
import time

pipeline_steps = [
    "01_extract.py",
    "02_load_to_mysql.py",
    "03_run_analysis.py"
]

print("=== STARTING ELT PIPELINE ===")
start_time = time.time()

for step in pipeline_steps:
    print(f"\nExecuting {step}...")
    # This runs the script as if you typed it in the terminal
    result = subprocess.run(["python", step], capture_output=True, text=True)
    
    if result.returncode == 0:
        print(result.stdout.strip())
    else:
        print(f"PIPELINE FAILED AT {step}:")
        print(result.stderr)
        break # Stop the pipeline if a step fails

end_time = time.time()
print(f"\n=== PIPELINE COMPLETE IN {round(end_time - start_time, 2)} SECONDS ===")