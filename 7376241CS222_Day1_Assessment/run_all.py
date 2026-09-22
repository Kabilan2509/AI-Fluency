"""Executes all systems and saves raw terminal logs into output/ directory."""
import subprocess
import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

scripts = [
    ("check_setup.py", "setup_check.txt"),
    ("tools.py", "tools_check.txt"),
    ("chatbot.py", "chatbot_output.txt"),
    ("workflow.py", "workflow_output.txt"),
    ("agent.py", "agent_output.txt"),
    ("challenge.py", "challenge_output.txt"),
]

python_exe = sys.executable

env = dict(os.environ)
env["PYTHONIOENCODING"] = "utf-8"

for script, outfile in scripts:
    print(f"Running {script} -> output/{outfile} ...")
    script_path = os.path.join(BASE_DIR, script)
    out_path = os.path.join(OUTPUT_DIR, outfile)
    res = subprocess.run([python_exe, script_path], capture_output=True, text=True, encoding="utf-8", env=env)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(res.stdout)
        if res.stderr:
            f.write("\n[STDERR]\n" + res.stderr)
    print(f"  Finished {script}")

print("\nAll outputs generated successfully in output/ folder.")
