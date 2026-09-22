# Day 1 Assessment: Agentic AI Foundations & Open-Source Practice

This repository contains the complete implementation and comparative evaluation for **Day 1 Assessment: Comparing a Plain Chatbot, a Rule-Based Workflow, and an AI Agent on a Private-Data Scenario of Your Own**.

## Project Overview

- **Chosen Domain:** Computer Science & Engineering (CSE) Department Cloud & High-Performance Computing (HPC) Cluster.
- **Core Concept:** $\text{Agent} = \text{LLM} + \text{Tools} + \text{Loop}$
- **Inference Engine:** Groq API (`openai/gpt-oss-20b`) / OpenAI-compatible endpoint.

## Repository Structure

```text
Day_1_Assessment/
├── .env                  # API keys and provider configuration (gitignored)
├── .gitignore            # Git exclusion rules
├── requirements.txt      # Python dependencies
├── config.py             # LLM client setup, private cluster catalog & test questions
├── check_setup.py        # Environment & connectivity test
├── chatbot.py            # System 1: Plain LLM Chatbot (no tools, no private data)
├── workflow.py           # System 2: Deterministic Rule-Based Workflow (Regex + if/else)
├── tools.py              # Private lookup tools (get_server_fee, get_server_status) & safe calculator
├── agent.py              # System 3: AI Agent (LLM + Tools + ReAct Loop)
├── challenge.py          # Novel challenge evaluation (combinatorial budget allocation)
├── run_all.py            # Automated test runner saving raw logs into output/
├── output/               # Captured terminal outputs and execution logs
│   ├── setup_check.txt
│   ├── chatbot_output.txt
│   ├── workflow_output.txt
│   ├── agent_output.txt
│   └── challenge_output.txt
├── analysis/
│   └── analysis.md       # Comprehensive evaluation report
├── analysis.md           # Standalone root evaluation report (Sections 3.1 - 3.4)
└── README.md             # Repository documentation
```

## Setup & Running

1. **Activate Virtual Environment:**
   ```powershell
   .venv\Scripts\activate
   ```
2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Configure Environment:**
   Ensure `.env` contains valid credentials:
   ```env
   PROVIDER=groq
   GROQ_API_KEY=your_key_here
   MODEL=openai/gpt-oss-20b
   ```
4. **Run Verification & Systems:**
   ```bash
   python check_setup.py
   python chatbot.py
   python workflow.py
   python agent.py
   python challenge.py
   ```
   Or run all systems simultaneously and save logs:
   ```bash
   python run_all.py
   ```
