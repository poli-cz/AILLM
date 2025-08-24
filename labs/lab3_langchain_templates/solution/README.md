


## Lab 3A – PromptTemplate + LLMChain
**Cíl**
- Umět parametrizovat prompt (`{topic}`, `{level}`) a řídit styl/výstup.  

**Doplnit**
- Vytvořit `PromptTemplate` s omezeními (≤ 5 vět, 1 analogie).  
- Sestavit `LLMChain` s Ollama.  
- Spustit s různými `--level` a porovnat výstupy.

**Instrukce / tipy**
- `PromptTemplate.from_template("...{topic}...{level}...")`  
- `LLMChain(llm=Ollama(...), prompt=tmpl)`  
- `chain.run({"topic": "...", "level": "beginner"})`

---

## Lab 3B – Strukturovaný JSON výstup
**Cíl**  
- Získat od modelu **validní JSON**, umět **opravit/validovat** odpověď.

**Doplnit**
- Prompt s inline schématem a požadavkem „**JSON only**“.  
- Robustní parsování (json.loads → substring → fallback).  
- Validace: 3–5 bullets, sources ≤ 3.

**Instrukce / tipy**
- Model občas vrátí text navíc → použij fallback extrakci `{...}`.  
- `bullets` < 3 → doplň „N/A“, > 5 → ořízni.  
- Testuj na tématu „RAG pitfalls“.

