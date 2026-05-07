FROM python:3.9-slim

# Mametraka FFmpeg ao anaty rafitra
RUN apt-get update && apt-get install -y ffmpeg && apt-get clean

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Mampandeha ny server (Port 8080 no ampiasain'ny Railway/Render matetika)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
