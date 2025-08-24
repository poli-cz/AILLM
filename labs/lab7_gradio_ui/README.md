# Lab 7 – Chatbot s UI (Gradio)

## Cíle
- Propojit LLM (Ollama) s FAISS a LangChain.
- Přidat paměť pro krátkodobý kontext.
- Vytvořit jednoduché UI přes Gradio.
- Experimentovat s parametry inference a exportem.

---

## 7A – Základní Gradio UI
**Úkoly**
- Vytvoř chat UI pomocí `gr.ChatInterface`.
- Napoj LLM (Ollama).
- Přidej krátkodobou paměť (`ConversationBufferMemory`).

**Test**
- Polož chatbotovi několik dotazů a ověř, že si pamatuje jméno uživatele.

---

## 7B – RAG s FAISS
**Úkoly**
- Načti FAISS index z labu 6.
- Použij `ConversationalRetrievalChain`.
- Přidej citace `[source#chunk]`.

**Test**
- Ptej se na obsah dokumentů a na nerelevantní dotazy.
- Ověř, že chatbot vrací *Nevím*, když odpověď není v kontextu.

---

## 7C – Pokročilé UI + nastavení
**Úkoly**
- Přidej ovládání `temperature`, `max_tokens`, `k`.
- Implementuj `/reset` pro vymazání paměti.
- Exportuj chat do `conversation.json`.

**Test**
- Vyzkoušej různé parametry a sleduj vliv.
- Exportuj konverzaci a otevři JSON.

---

## Odevzdání
- Soubor `chatbot_student.py` s vyplněným kódem.
- Ukázkový `conversation.json`.

