# Lab 2 – Ollama Setup & First Calls

**Goals**
- Verify Ollama daemon is running and a model is available (`ollama run mistral`).
- Call the REST API directly with `requests`.
- Build a small CLI tool using `typer`.
- Experiment with model options (temperature, top_p).
- (Bonus) Measure simple latency across multiple prompts.

**Run examples**
```bash
# Direct REST call
python labs/lab2_ollama_setup/rest_call_student.py --prompt "Say hi in one sentence."

# CLI wrapper
python labs/lab2_ollama_setup/ask_model_student.py --prompt "Explain cosine similarity."

# Options (temperature)
python labs/lab2_ollama_setup/options_demo_student.py --prompt "Give 3 creative team names" --temperature 1.2

# Benchmark
python labs/lab2_ollama_setup/benchmark_student.py --prompts "A|B|C"
