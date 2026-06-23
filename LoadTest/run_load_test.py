# LoadTest/run_load_test.py
import os
import sys
import time
import json
import subprocess
from pathlib import Path

# Try to import psutil. If not available, print error (though we installed it successfully)
try:
    import psutil
except ImportError:
    print("[ERROR] psutil is not installed. Please install it with pip install psutil.")
    sys.exit(1)

WORKSPACE_ROOT = Path("D:/My repositories/Pipeline")
LOAD_TEST_DIR = WORKSPACE_ROOT / "LoadTest"
GLOBAL_CONFIG = "ude/ude_global_config.json"

# Sorted list of SDKs with Python SWIG wrappers, ordered by size ascending
SDKS = [
    {"name": "Sdai", "folder": "Sdai", "lower_id": "sdai_api_py", "files": 2, "size": "30.53 KB"},
    {"name": "BrepModeler", "folder": "BrepModeler", "lower_id": "brepmodeler_api_py", "files": 1, "size": "434.10 KB"},
    {"name": "FacetModeler", "folder": "FacetModeler", "lower_id": "facetmodeler_api_py", "files": 2, "size": "514.58 KB"},
    {"name": "Components", "folder": "Components", "lower_id": "components_api_py", "files": 7, "size": "952.82 KB"},
    {"name": "bimnv", "folder": "bimnv", "lower_id": "bimnv_api_py", "files": 20, "size": "3.30 MB"},
    {"name": "Step", "folder": "Step", "lower_id": "step_api_py", "files": 6, "size": "5.19 MB"},
    {"name": "Drawings", "folder": "Drawings", "lower_id": "drawings_api_py", "files": 28, "size": "7.13 MB"},
    {"name": "Kernel", "folder": "Kernel", "lower_id": "kernel_api_py", "files": 22, "size": "9.18 MB"},
    {"name": "Dgn", "folder": "Dgn", "lower_id": "dgn_api_py", "files": 6, "size": "14.99 MB"},
    {"name": "BimRv", "folder": "BimRv", "lower_id": "bimrv_api_py", "files": 28, "size": "54.24 MB"},
    {"name": "Ifc", "folder": "Ifc", "lower_id": "ifc_api_py", "files": 18, "size": "82.94 MB"}
]

# Results dictionary to store stats for each SDK
# Status options: "Pending", "Running...", "Completed", "Failed"
results = {
    sdk["name"]: {
        "status": "Pending",
        "doxygen_time": 0.0,
        "doxygen_mem": 0.0,
        "doxygen_cpu": 0.0,
        "ude_time": 0.0,
        "ude_mem": 0.0,
        "ude_cpu": 0.0,
        "error_msg": ""
    }
    for sdk in SDKS
}

def format_time(seconds):
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    return f"{h:02d}:{m:02d}:{s:02d}"

def format_memory(bytes_val):
    if bytes_val <= 0:
        return "0.0 MB"
    mb = bytes_val / (1024 * 1024)
    if mb < 1024:
        return f"{mb:.1f} MB"
    return f"{mb / 1024:.2f} GB"

def write_report():
    report_path = LOAD_TEST_DIR / "report.md"
    
    # Formulate Markdown content
    lines = [
        "# ODA SDK Python API Documentation Load Test Report",
        "",
        "This report is generated dynamically by the automated load testing runner. "
        "It monitors Doxygen and UDE (Universal Documentation Engine) execution metrics, including runtime, memory footprint, and CPU utilization.",
        "",
        f"**Last updated:** {time.strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        "## Real-time Metrics Table",
        "",
        "| SDK Name | Wrapper Files | Total Size | Status | Doxygen Time | Doxygen Max Mem | Doxygen CPU | UDE Time | UDE Max Mem | UDE CPU |",
        "| :--- | ---: | ---: | :--- | ---: | ---: | ---: | ---: | ---: | ---: |"
    ]
    
    for sdk in SDKS:
        name = sdk["name"]
        res = results[name]
        
        status_str = res["status"]
        if status_str == "Running...":
            status_str = "🟡 **Running...**"
        elif status_str == "Completed":
            status_str = "🟢 Completed"
        elif status_str == "Failed":
            status_str = f"🔴 Failed"
        
        dox_time = format_time(res["doxygen_time"]) if res["doxygen_time"] > 0 or res["status"] in ["Completed", "Failed"] else "-"
        dox_mem = format_memory(res["doxygen_mem"]) if res["doxygen_mem"] > 0 else "-"
        dox_cpu = f"{res['doxygen_cpu']:.1f} cores" if res["doxygen_cpu"] > 0 else "-"
        
        ude_time = format_time(res["ude_time"]) if res["ude_time"] > 0 or res["status"] in ["Completed", "Failed"] else "-"
        ude_mem = format_memory(res["ude_mem"]) if res["ude_mem"] > 0 else "-"
        ude_cpu = f"{res['ude_cpu']:.1f} cores" if res["ude_cpu"] > 0 else "-"
        
        lines.append(
            f"| {name} | {sdk['files']} | {sdk['size']} | {status_str} | {dox_time} | {dox_mem} | {dox_cpu} | {ude_time} | {ude_mem} | {ude_cpu} |"
        )
        
    lines.append("")
    
    # Add a section for detailed failures if any occurred
    has_errors = any(res["error_msg"] for res in results.values())
    if has_errors:
        lines.append("## Error Logs / Details")
        lines.append("")
        for sdk in SDKS:
            name = sdk["name"]
            res = results[name]
            if res["error_msg"]:
                lines.append(f"### 🔴 {name} Failure Details")
                lines.append(f"```\n{res['error_msg']}\n```")
                lines.append("")

    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

def monitor_process_tree(proc_id, sdk_name):
    """
    Monitors a spawned process and its children.
    Attributes metrics to Doxygen if doxygen is running, otherwise to UDE.
    """
    try:
        main_proc = psutil.Process(proc_id)
    except psutil.NoSuchProcess:
        return

    # Track time and stats
    last_check_time = time.time()
    
    # To filter out initial 0.0 cpu readings
    main_proc.cpu_percent(interval=None)

    # Poll process tree until main process exits
    while main_proc.is_running() and main_proc.status() != psutil.STATUS_ZOMBIE:
        current_time = time.time()
        elapsed = current_time - last_check_time
        last_check_time = current_time
        
        try:
            # Check for child processes recursively
            children = main_proc.children(recursive=True)
            
            doxygen_proc = None
            for child in children:
                try:
                    if "doxygen" in child.name().lower():
                        doxygen_proc = child
                        break
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue

            if doxygen_proc:
                # Doxygen is running
                results[sdk_name]["doxygen_time"] += elapsed
                
                # Monitor Doxygen memory
                try:
                    dox_mem = doxygen_proc.memory_info().rss
                    results[sdk_name]["doxygen_mem"] = max(results[sdk_name]["doxygen_mem"], dox_mem)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
                    
                # Monitor Doxygen CPU
                try:
                    dox_cpu = doxygen_proc.cpu_percent(interval=None)
                    # Convert percent to cores (e.g. 200.0% -> 2.0 cores)
                    cores = dox_cpu / 100.0
                    results[sdk_name]["doxygen_cpu"] = max(results[sdk_name]["doxygen_cpu"], cores)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
            else:
                # UDE is running (Python parser/renderer phases)
                results[sdk_name]["ude_time"] += elapsed
                
                # Monitor UDE memory (sum of main process + children that are NOT doxygen)
                try:
                    ude_mem = main_proc.memory_info().rss
                    for child in children:
                        try:
                            if "doxygen" not in child.name().lower():
                                ude_mem += child.memory_info().rss
                        except (psutil.NoSuchProcess, psutil.AccessDenied):
                            continue
                    results[sdk_name]["ude_mem"] = max(results[sdk_name]["ude_mem"], ude_mem)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
                    
                # Monitor UDE CPU
                try:
                    ude_cpu = main_proc.cpu_percent(interval=None)
                    for child in children:
                        try:
                            if "doxygen" not in child.name().lower():
                                ude_cpu += child.cpu_percent(interval=None)
                        except (psutil.NoSuchProcess, psutil.AccessDenied):
                            continue
                    cores = ude_cpu / 100.0
                    results[sdk_name]["ude_cpu"] = max(results[sdk_name]["ude_cpu"], cores)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass

        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
            
        # Write report to update progress online
        write_report()
        time.sleep(0.5) # Poll frequently for fine-grained real-time metrics

def run_pipeline_for_sdk(sdk):
    name = sdk["name"]
    folder = sdk["folder"]
    lower_id = sdk["lower_id"]
    
    print(f"\n>>> [STARTING] {name} HTML Doc Generation Load Test...")
    results[name]["status"] = "Running..."
    write_report()
    
    sdk_config = f"ude/{folder}/ude_sdk_config.json"
    doc_config = f"ude/{folder}/{lower_id}/ude_doc_config.json"
    
    cmd = [
        sys.executable,
        "-m", "ude.cli",
        "--global-config", GLOBAL_CONFIG,
        "--sdk-config", sdk_config,
        "--doc-config", doc_config,
        "--format", "html"
    ]
    
    start_time = time.time()
    
    try:
        # Launch UDE CLI process
        p = subprocess.Popen(
            cmd,
            cwd=str(WORKSPACE_ROOT),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Monitor the process and its children in real-time
        monitor_process_tree(p.pid, name)
        
        # Wait for completion and get output
        stdout, stderr = p.communicate()
        
        if p.returncode == 0:
            results[name]["status"] = "Completed"
            print(f">>> [SUCCESS] {name} build completed successfully.")
        else:
            results[name]["status"] = "Failed"
            results[name]["error_msg"] = f"Exit code: {p.returncode}\nStderr:\n{stderr}\nStdout:\n{stdout}"
            print(f">>> [FAILED] {name} build failed with exit code {p.returncode}.")
            
    except Exception as e:
        results[name]["status"] = "Failed"
        results[name]["error_msg"] = str(e)
        print(f">>> [EXCEPTION] {name} failed: {e}")
        
    write_report()

def main():
    print("=" * 70)
    print("  ODA SDK PYTHON HTML DOCUMENTATION LOAD TESTING RUNNER")
    print("=" * 70)
    print(f"Monitoring output target: {LOAD_TEST_DIR / 'report.md'}")
    
    LOAD_TEST_DIR.mkdir(parents=True, exist_ok=True)
    write_report()
    
    for sdk in SDKS:
        run_pipeline_for_sdk(sdk)
        
    print("\n" + "=" * 70)
    print("  LOAD TESTING RUN COMPLETED FOR ALL SDK WRAPPERS!")
    print("=" * 70)

if __name__ == "__main__":
    main()
