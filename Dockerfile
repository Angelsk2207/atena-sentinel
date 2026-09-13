FROM python:3.12-alpine
WORKDIR /app
COPY server.py .
ENV PYTHONDONTWRITEBYTECODE=1
CMD ["python","server.py"]
