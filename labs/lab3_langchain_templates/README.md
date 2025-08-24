# Lab 3 – Šablony a strukturovaný JSON výstup

**Cíle**
- Naučit se používat `PromptTemplate` a `LLMChain` pro systematickou práci s prompty.
- Vynutit od LLM konzistentní strukturu výstupu (JSON).
- Vyzkoušet robustní parsování a validaci výstupů.

---

## 3A – PromptTemplate + LLMChain

**Úkoly**
1. Vytvoř `PromptTemplate` s proměnnými `{topic}` a `{level}`.
2. Přidej omezení:
   - max. 5 vět  
   - přesně 1 krátká analogie  
   - styl: friendly, konkrétní
3. Připoj `Ollama` jako LLM a sestav `LLMChain`.
4. Spusť přes CLI s parametry.

**Spuštění**
```bash
python labs/lab3_langchain_templates/template_demo_student.py --topic "Neurální sítě" --level beginner
```

Očekávaný výstup: krátké přátelské vysvětlení tématu s jednou analogií.

---

## 3B – Strukturovaný JSON výstup

**Úkoly**
1. Vytvoř prompt, který **vynutí** JSON dle schématu:
   ```json
   {
     "title": "string",
     "bullets": ["string", "string", "string"],
     "tags": ["string"],
     "sources": ["string"]
   }
   ```
   - `bullets` vždy 3–5 položek
   - `sources` max 3 položky
2. Implementuj **robustní parsování**:
   - zkus `json.loads`
   - fallback: substring od `{` po `}`
   - pokud selže, vrať:
     ```json
     {"title":"Fallback","bullets":["raw_text"]}
     ```
3. Validuj:
   - `title` jako string
   - `bullets` délka 3–5 (méně doplň „N/A“, více ořízni)
   - `sources` max 3

**Spuštění**
Opět z kořene repozitáře a s nastaveným `PYTHONPATH`. Viz lab2.

```bash
python labs/lab3_langchain_templates/structured_output_student.py --topic "RAG pitfalls"
```

Očekávaný výstup: validní JSON objekt (title, bullets, volitelně tags/sources).

---

## Troubleshooting

- **`ModuleNotFoundError: No module named 'labs'`**
  - Spouštěj z kořene repozitáře:
    ```bash
    python -m labs.lab3_langchain_templates.template_demo_student --topic "X"
    ```
  - nebo nastav `PYTHONPATH`:
    ```bash
    export PYTHONPATH=$(pwd)
    python labs/lab3_langchain_templates/template_demo_student.py --topic "X"
    ```

- **Výstup není validní JSON**
  - Zkontroluj prompt – musí jasně říkat „Vytiskni pouze JSON, žádný doprovodný text“.
  - Použij robustní parser a validátor.

- **Chybí některá pole**
  - Validátor má doplnit výchozí hodnoty (`title="Untitled"`, `bullets=["N/A"]`).

---
