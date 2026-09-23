# Day 2 Assessment: Reasoning and Acting

This project uses a campus equipment-rental scenario. Its private catalogue has daily rates for `CAMERA`, `DRONE`, and `MIC`; the ReAct agent must use tools to retrieve them rather than inventing a price.

## Setup and runs

1. Create `.env` from `.env.example` and enter a supported provider credential, or use a running Ollama server.
2. Install dependencies: `pip install -r requirements.txt`.
3. Run `python cot_compare.py`, `python self_consistency.py`, and `python react_trace.py`.
4. Save screenshots of the three command outputs in `screenshots/` before submission.

The written assessment is in `analysis.md`.
