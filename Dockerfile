FROM python:3.12-slim

ARG UID
ARG GID=${UID}
ARG USER=dsh
ARG GROUP=dsh

RUN apt-get update && apt-get install -y --no-install-recommends \
	openssl \
	curl \
	build-essential \
	librdkafka-dev \
	libpq-dev

# Create dsh group and user
RUN addgroup --gid ${GID} dsh \
	&& adduser --uid ${UID} --gid ${GID} --disabled-password --gecos "" ${USER}

# Copy the source code and dependencies
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
COPY --chown=${UID}:${GID} --chmod=0755 dsh-entrypoint /home/dsh/dsh
COPY --chown=${UID}:${GID} ./src/ /home/dsh/app/src/
COPY --chown=${UID}:${GID} pyproject.toml uv.lock /home/dsh/app/

WORKDIR /home/dsh/app/
RUN uv pip install -r pyproject.toml --system
RUN uv pip install -e . --system

USER ${USER}
ENTRYPOINT ["python", "-m", "dsh.entrypoint"]
CMD ["python", "/home/dsh/app/src/main.py"]

