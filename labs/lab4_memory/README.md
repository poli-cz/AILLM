# Lab 4 – Paměť v LangChain (3 úlohy)

## Cíle
- Zvolit vhodný typ paměti (window/summary/vector).
- Držet kontext v rozumném limitu.
- Kombinovat více pamětí dohromady.

---

## 4A – Chat s oknem a rozpočtem
**Úkoly**
1. Spusť `ConversationBufferWindowMemory(window_size=N)`.
2. Implementuj `/reset`, `/save PATH`.
3. Hlídání limitu: jakmile odhad kontextu > `--limit`, sniž `window_size`.


**Test**
- Napiš 8–12 zpráv, ověř snižování okna a funkčnost uloženého přepisu.

---

## 4B – Shrnovací paměť
**Úkoly**
1. Nastav `ConversationSummaryMemory` s vlastním summarizačním promptem.
2. Před každou odpovědí, když `len(summary) > --limit_chars`, zkrať/přegeneruj.
3. Otestuj ztrátu detailu otázkami k dřívějším částem konverzace.


---

## 4C – Kombinace pamětí (okno + shrnutí)
**Úkoly**
1. Vytvoř chain, který využívá **dvě paměti současně**:
   - `ConversationBufferWindowMemory` – krátkodobá paměť (posledních N zpráv).
   - `ConversationSummaryMemory` – dlouhodobé shrnutí celé konverzace.
2. Do promptu vlož obě části: `{history_window}`, `{history_summary}`.
3. Implementuj příkaz `/show`, který vypíše obsah obou pamětí.
4. Otestuj na delší konverzaci, kde je potřeba kombinovat okno i shrnutí.


**Test**
- Vytvoř sérii 10–15 zpráv (např. plánování dovolené).
- Vlož detail v 1.–2. zprávě a ověř, že se dá vybavit i na konci (přes shrnutí).
- Diskutuj, zda shrnutí zachovalo všechny důležité detaily nebo něco zkreslilo.

---