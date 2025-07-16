FROM python:3.12

RUN apt-get update && apt-get install -y --no-install-recommends \
    binutils \
    build-essential \
    gettext \
    libproj-dev \
    python3-dev \
    wget \
    && mkdir /var/log/uwsgi \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

ENV DOCKERIZE_VERSION v0.6.1
RUN wget --secure-protocol=TLSv1_2 --max-redirect=5 https://github.com/jwilder/dockerize/releases/download/"$DOCKERIZE_VERSION"/dockerize-linux-amd64-"$DOCKERIZE_VERSION".tar.gz \
    && tar -C /usr/local/bin -xzvf dockerize-linux-amd64-"$DOCKERIZE_VERSION".tar.gz \
    && rm dockerize-linux-amd64-"$DOCKERIZE_VERSION".tar.gz

# --- Install uv (universal dependency manager) ---
RUN curl -LsSf https://astral.sh/uv/install.sh | sh \
    && mv /root/.local/bin/uv /usr/local/bin/

# --- Set working directory early for clarity ---
WORKDIR /app

# --- Copy and install only dependencies first (for better Docker layer caching) ---
COPY pyproject.toml uv.lock ./
RUN uv pip install --system --group main

# --- Now copy full source ---
COPY . .

COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

EXPOSE 3031

ENTRYPOINT [ "/app/entrypoint.sh" ]

CMD ["gunicorn", "cubot.wsgi:application", "-b", "0.0.0.0:3031", "-w", "5", "-t", "180"]