FROM debian:bullseye

# Update package lists and install required dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
	python3 \
	python3-pip \
	openssl \
	curl \
	build-essential \
	librdkafka-dev \
	libpq-dev

# Copy dsh dependencies
COPY dsh-entrypoint /home/dsh/dsh

# Create dsh group and user
ARG tenantuserid
ENV USERID $tenantuserid
RUN addgroup --gid ${USERID} dsh && adduser --uid ${USERID} --gid ${USERID} --disabled-password --gecos "" dsh

# Install required Python packages
RUN pip3 install googleapis-common-protos confluent-kafka requests && \
	pip3 install /home/dsh/dsh/lib/envelope-0.1.tar.gz

# Copy the source code
COPY src/ /home/dsh/app/

# Set ownership and permissions
RUN chown -R $USERID:$USERID /home/dsh/ && \
	chmod +x /home/dsh/dsh/entrypoint.sh

USER dsh
WORKDIR /home/dsh/app

# Entrypoint
ENTRYPOINT ["/home/dsh/dsh/entrypoint.sh"]
CMD ["python3", "-u", "main.py"]


