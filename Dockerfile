FROM python:3.11-buster

# Update package lists and install required dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
	openssl \
	curl \
	build-essential \
	librdkafka-dev \
	libpq-dev

# Install Poetry
RUN pip install poetry

ENV POETRY_NO_INTERACTION=1 \
	POETRY_VIRTUALENVS_IN_PROJECT=1 \
	POETRY_VIRTUALENVS_CREATE=1 \
	POETRY_CACHE_DIR=/tmp/poetry_cache

# Set up the PATH to include the Poetry binaries
ENV PATH="${PATH}:/root/.poetry/bin"

# Create and set up the working directory
WORKDIR /app

# Copy dsh dependencies
COPY dsh-entrypoint ./

# Create dsh group and user
ARG tenantuserid
ENV USERID $tenantuserid
RUN addgroup --gid ${USERID} dsh && adduser --uid ${USERID} --gid ${USERID} --disabled-password --gecos "" dsh

# Set ownership and permissions
RUN chown -R $USERID:$USERID . && \
	chmod +x /app/entrypoint.sh
USER dsh

# Install required Python packages and copy code
COPY pyproject.toml poetry.lock ./
RUN poetry install --no-root && rm -rf $POETRY_CACHE_DIR
COPY src/ ./src


# Entrypoint
ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["poetry", "run", "python", "src/main.py"]

