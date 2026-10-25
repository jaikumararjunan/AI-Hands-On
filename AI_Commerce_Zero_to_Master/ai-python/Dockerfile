FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app ./app
COPY vector_from_scratch_demo.py ./vector_from_scratch_demo.py
COPY docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh
# Windows Git checkouts can convert .sh files to CRLF. Strip any trailing CR
# inside the Linux image so the entrypoint remains executable on every clone.
RUN sed -i 's/\r$//' /usr/local/bin/docker-entrypoint.sh \
    && chmod +x /usr/local/bin/docker-entrypoint.sh
EXPOSE 8000
HEALTHCHECK --interval=10s --timeout=5s --start-period=45s --retries=18 CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health', timeout=3)"
# Invoke the script through /bin/sh as an extra guard against shebang/line-ending issues.
ENTRYPOINT ["/bin/sh", "/usr/local/bin/docker-entrypoint.sh"]
