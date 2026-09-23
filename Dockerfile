FROM python:3.12-slim
WORKDIR /app
COPY requirements-minimal.txt .
RUN pip install --no-cache-dir -r requirements-minimal.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
