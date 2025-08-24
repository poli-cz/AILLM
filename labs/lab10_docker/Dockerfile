FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
ENV OLLAMA_BASE_URL=http://host.docker.internal:11434
CMD ["python","labs/lab8_gradio_ui/app.py"]
