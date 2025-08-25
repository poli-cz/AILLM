# Lab 4 – Paměť v LangChain (Window / Summary / Hybrid + Forget)

Cíl labu:
- Umět zvolit (a zkombinovat) vhodný typ paměti: **okno** vs. **shrnutí**.
- Udržet kontext v rozumném limitu (simulace „token budgetu“).
- Ukládat / čistit historii a předvést „selektivní zapomínání“.

> Všechny ukázky používají **Ollama** model z `labs/common/settings.py` (proměnná `LLM_MODEL`).

---

## 4A – Chat s oknem a rozpočtem (ConversationBufferWindowMemory)

**Cíle**
1. Spustit `ConversationBufferWindowMemory(window_size=N)`.
2. Implementovat příkazy:
   - `/reset` – smaže historii v okně,
   - `/save PATH` – uloží přepis do JSON.
3. Hlídání limitu: když odhad kontextu překročí `--limit`, **sniž** `window_size` (např. o 1) a informuj uživatele.

**Spuštění**
```bash
python labs/lab4_memory/memory_chat_student.py --window 6 --limit 1200
python labs/lab4_memory/memory_chat_solution.py --window 6 --limit 1400
```

**Tipy pro test**
- Napiš 8–12 zpráv tak, aby se okno muselo „zúžit“.
- Ověř, že `/save transcript.json` vytvoří čitelný JSON s rolemi a obsahem.

---

## 4B – Shrnovací paměť (ConversationSummaryMemory)

**Cíle**
1. Použít `ConversationSummaryMemory` s **vlastním** summarizačním promptem.
2. Udržovat shrnutí krátké: pokud `len(summary) > --limit_chars`, zkrať/přegeneruj.
3. Otestuj ztrátu detailu: zeptej se na informaci ze startu konverzace.

**Spuštění**
```bash
python labs/lab4_memory/summary_memory_student.py --limit_chars 800
python labs/lab4_memory/summary_memory_solution.py --limit_chars 800
```

**Tip**
- `memory.buffer` obsahuje aktuální shrnutí. Vypiš si ho pomocí příkazu `/show`.

---

## 4C – Hybrid (okno + shrnutí dohromady)

**Cíle**
1. Vytvořit prompt s oběma částmi:
   - `{history_window}` – posledních N zpráv,
   - `{history_summary}` – dlouhodobé shrnutí.
2. Implementovat `/show` pro zobrazení obou pamětí.
3. Ukázat, že se víc detailů udrží díky kombinaci obou přístupů.

**Spuštění**
```bash
python labs/lab4_memory/hybrid_summary_student.py --window 4
python labs/lab4_memory/hybrid_summary_solution.py --window 4
```

---

## 4X – Selektivní zapomínání (/forget)

**Cíle**
- Rozšířená ukázka: hybridní paměť + příkaz `/forget <keyword>`,
- Zapomenout zprávy obsahující klíčové slovo z krátkodobé paměti **i** shrnutí (shrnutí přegenerovat).

**Spuštění**
```bash
python labs/lab4_memory/memory_forget_demo.py --window 5
```

---

## Známé limity / Poznámky
- Ukázky používají `LLMChain.invoke(...)` (bez `run`) kvůli deprecations.
- `LLMChain` je v novějších verzích dále „na ústupu“. Pro produkci zvaž `prompt | llm` + `RunnableWithMessageHistory`.
- Odhad tokenů je **přibližný** – stačí pro účely labu (viz komentáře v kódu).
