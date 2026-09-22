"""Shared configuration: choices of LLM provider and private CSE Department Cloud Cluster data."""
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

PROVIDER = os.getenv("PROVIDER", "groq").strip().lower()

if PROVIDER == "ollama":
    BASE_URL = "http://localhost:11434/v1"
    API_KEY = "ollama"
    MODEL = os.getenv("MODEL", "qwen2.5:1.5b")
elif PROVIDER == "groq":
    BASE_URL = "https://api.groq.com/openai/v1"
    API_KEY = os.getenv("GROQ_API_KEY")
    MODEL = os.getenv("MODEL", "openai/gpt-oss-20b")
elif PROVIDER == "huggingface":
    BASE_URL = "https://router.huggingface.co/v1"
    API_KEY = os.getenv("HF_TOKEN")
    MODEL = os.getenv("MODEL", "openai/gpt-oss-20b")
else:
    raise SystemExit(f"Unknown PROVIDER '{PROVIDER}'. Use ollama, groq or huggingface.")

if not API_KEY:
    raise SystemExit(f"No API key found for PROVIDER={PROVIDER}. Check your .env file.")

client = OpenAI(base_url=BASE_URL, api_key=API_KEY)

# Private CSE Department Cluster catalog (Confidential internal rates & real-time operational status)
SERVER_DATA = {
    "HPC01": {
        "name": "High-Performance GPU Cluster Node (4x NVIDIA RTX 4090, 128GB RAM)",
        "fee_per_hour": 450,
        "status": "Available in Server Room Rack 4 (Node A)",
    },
    "VM101": {
        "name": "Virtual Machine Cluster (64 vCPU, 256GB RAM, Web & Database Staging)",
        "fee_per_hour": 180,
        "status": "Under Maintenance (Linux kernel security patch in progress)",
    },
    "EDGE01": {
        "name": "Embedded IoT & Edge AI Gateway (NVIDIA Jetson AGX Orin 64GB)",
        "fee_per_hour": 90,
        "status": "In Use (Reserved by Distributed Systems Lab until 6 PM)",
    },
    "SAND01": {
        "name": "Isolated Cybersecurity Sandbox (Malware Analysis on isolated VLAN 99)",
        "fee_per_hour": 250,
        "status": "Available in Isolated Network Rack 2",
    },
}

QUESTIONS = [
    # Q1: Direct Private Attribute Lookup
    "What is the hourly usage fee for HPC01?",

    # Q2: Multi-Step Calculation with Hours & Research Grant Discount
    "What is the total cost for running HPC01 for 10 hours and VM101 for 20 hours after a 15% departmental research grant discount?",

    # Q3: Relational / Comparative Analysis
    "Is SAND01 more expensive per hour than VM101, and by how much?",

    # Q4: Private Operational Status Lookup
    "What is the current operational status of VM101?",

    # Q5: Unique CSE Domain Technical Troubleshooting (Zero-Tool Restraint Test)
    "Our Python deep learning script threw 'CUDA out of memory: Tried to allocate 4.00 GiB on GPU 0'. What code optimizations can we apply to fix this?",

    # Q6: Out-of-Scope Non-Existent Entity Test
    "Can you check if quantum simulator node QBIT01 is online and what its hourly billing rate is?",
]

def banner(system_name: str) -> None:
    print(f"\n=== {system_name} | provider: {PROVIDER} | model: {MODEL} ===\n")
