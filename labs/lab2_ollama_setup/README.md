# Lab 2 – Ollama: Nastavení a první volání

**Cíle**
- Ověřit, že **Ollama daemon běží** a je k dispozici model (`ollama run mistral`).
- Zavolat **REST API** přímo pomocí `requests`.
- Postavit malý **CLI nástroj** pomocí `typer`.
- Experimentovat s **parametry modelu** (`temperature`, `top_p`).
- (Bonus) Změřit jednoduchou **latenci** pro více promptů.

---

## Implementace a spuštění příkladů

Než spustíte příklady, ujistěte se, že jste v **kořenovém adresáři repozitáře** a máte aktivované virtuální prostředí. Spusťte také:

```bash
export PYTHONPATH=$(pwd)
```

Aby se předešlo chybě `ModuleNotFoundError`.

Pokud potřebujete ověřit nastavení, spusťte:

```bash
export PYTHONPATH=$(pwd)
python labs/lab2_ollama_setup/solution/rest_call_solution.py --prompt "Say hi in one sentence."
```

Po implementaci studentských souborů je spustíte podobně:

```bash
# Přímé REST volání
python labs/lab2_ollama_setup/rest_call_student.py --prompt "Say hi in one sentence."

# CLI wrapper
python labs/lab2_ollama_setup/ask_model_student.py --prompt "Explain cosine similarity."

# Parametry (temperature)
python labs/lab2_ollama_setup/options_demo_student.py --prompt "Give 3 creative team names" --temperature 1.2

# Benchmark
python labs/lab2_ollama_setup/benchmark_student.py --prompts "A|B|C"
```

---

## Požadavky

Ollama musí být **nainstalovaná** a **běžet na pozadí**:
```bash
ollama serve &
```
Musí být k dispozici alespoň jeden model (např. Mistral):
```bash
ollama pull mistral
ollama run mistral "Hello"
```

---

## Řešení problémů

- **`ModuleNotFoundError: No module named 'labs'`**
  - Ujistěte se, že spouštíte z **kořene repozitáře**:  
    ```bash
    python -m labs.lab2_ollama_setup.rest_call_student --prompt "Hi"
    ```
  - Nebo nastavte `PYTHONPATH` před spuštěním:  
    ```bash
    export PYTHONPATH=$(pwd)
    python labs/lab2_ollama_setup/rest_call_student.py --prompt "Hi"
    ```

- **`ConnectionError` / `Connection refused`**
  - Ollama daemon neběží. Spusťte jej:
    ```bash
    ollama serve &
    ```

- **`JSONDecodeError`**
  - Ujistěte se, že v payloadu posíláte `"stream": false`.
  - Pro debug si vytiskněte `response.text`.

- **`HTTP 404 / 500`**
  - Špatný název modelu nebo model chybí. Nejprve jej stáhněte:
    ```bash
    ollama pull mistral
    ```

- **Pořád problém?**
  - Zkontrolujte pracovní adresář:
    ```bash
    pwd
    ls labs
    ```
  - Ověřte, že existuje `labs/__init__.py` (aby `labs` byla považována za balíček).
