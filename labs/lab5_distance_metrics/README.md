# Lab 5 – Vzdálenosti embeddingů (2 úlohy)

## Cíle
- Pochopit, jak fungují metriky podobnosti embeddingů (cosine similarity, eukleidovská vzdálenost, dot product).
- Vyzkoušet si praktické využití těchto metrik při hledání nejpodobnější věty.

---

## 5A – Výpočet metrik podobnosti
**Úkoly**
1. Vytvoř embeddingy pro několik vět pomocí `SentenceTransformer("all-MiniLM-L6-v2")`.
2. Implementuj funkce:
   - `cosine_similarity(v1, v2)`
   - `euclidean_distance(v1, v2)`
   - `dot_product(v1, v2)`
3. Spočítej hodnoty pro všechny dvojice vět a porovnej výsledky.



**Test**
- Zkontroluj, které věty jsou si nejblíž podle různých metrik.
- Diskutuj: dávají všechny metriky stejný výsledek?

---

## 5B – Mini vyhledávač vět
**Úkoly**
1. Měj kolekci vět (např. 8–10 krátkých anglických vět).
2. Uživatel zadá dotaz (např. *"I like playing football"*).
3. Najdi nejpodobnější větu z kolekce:
   - Použij cosine similarity mezi embeddingem dotazu a embeddingy vět.
   - Vrať top 1 a top 3 výsledky.
