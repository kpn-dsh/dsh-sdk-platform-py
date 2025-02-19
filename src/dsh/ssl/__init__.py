from pathlib import Path
import os
import subprocess
import json
import requests
from loguru import logger


class DshCertificateManager:
    def __init__(self):
        self.pki_dir = Path("/home/dsh/pki")
        self.pki_dir.mkdir(parents=True, exist_ok=True)

        # Required env vars
        self.kafka_config_host = os.environ["KAFKA_CONFIG_HOST"]
        self.dsh_secret_token = os.environ["DSH_SECRET_TOKEN"]
        self.mesos_task_id = os.environ["MESOS_TASK_ID"]
        self.marathon_app_id = os.environ["MARATHON_APP_ID"]
        self.dsh_ca_certificate = os.environ["DSH_CA_CERTIFICATE"]

        # Derived values
        self.tenant_name = self.marathon_app_id.split("/")[1]
        self.dns_name = self._get_dns_name()

        # Certificate paths
        self.ca_cert_path = self.pki_dir / "ca.crt"
        self.client_key_path = self.pki_dir / "client.key"
        self.client_csr_path = self.pki_dir / "client.csr"
        self.client_cert_path = self.pki_dir / "client.crt"

    def _get_dns_name(self) -> str:
        """Convert marathon app ID to DNS name"""
        parts = self.marathon_app_id.split("/")
        parts.reverse()
        return ".".join(part for part in parts if part) + ".marathon.mesos"

    def setup_certificates(self):
        logger.info("Setting up DSH tenant certificates and configuration")

        # Write CA cert
        self.ca_cert_path.write_text(self.dsh_ca_certificate)

        # Get DN from config host
        dn = self._get_dn()
        logger.info(f"Retrieved DN: {dn}")

        self._generate_key_and_csr(dn)
        self._get_signed_certificate()
        config = self._get_tenant_config()
        self._export_env_vars(config)

    def _get_dn(self) -> str:
        """Get Distinguished Name from Kafka config host"""
        url = f"https://{self.kafka_config_host}/dn/{self.tenant_name}/{self.mesos_task_id}"
        response = requests.get(url, verify=self.ca_cert_path)
        response.raise_for_status()
        return response.text

    def _generate_key_and_csr(self, dn: str):
        # Generate private key
        subprocess.run(
            ["openssl", "genrsa", "-out", str(self.client_key_path), "4096"], check=True
        )

        # Generate CSR
        dn_parts = [f"/{part.strip()}" for part in dn.split(",")]
        subject = "".join(dn_parts)

        subprocess.run(
            [
                "openssl",
                "req",
                "-key",
                str(self.client_key_path),
                "-new",
                "-out",
                str(self.client_csr_path),
                "-subj",
                subject,
            ],
            check=True,
        )

    def _get_signed_certificate(self):
        """Get signed certificate from Kafka config host"""
        url = f"https://{self.kafka_config_host}/sign/{self.tenant_name}/{self.mesos_task_id}"
        headers = {"X-Kafka-Config-Token": self.dsh_secret_token}

        with open(self.client_csr_path, "rb") as f:
            response = requests.post(
                url, headers=headers, data=f.read(), verify=self.ca_cert_path
            )
        response.raise_for_status()

        self.client_cert_path.write_bytes(response.content)

    def _get_tenant_config(self) -> dict:
        """Get tenant configuration"""
        url = f"https://{self.kafka_config_host}/kafka/config/{self.tenant_name}/{self.mesos_task_id}?format=json"
        response = requests.get(
            url,
            verify=self.ca_cert_path,
            cert=(self.client_cert_path, self.client_key_path),
        )
        response.raise_for_status()
        return response.json()

    def _export_env_vars(self, config: dict):
        """Export required environment variables"""
        os.environ["DSH_PKI_CACERT"] = str(self.ca_cert_path)
        os.environ["DSH_PKI_KEY"] = str(self.client_key_path)
        os.environ["DSH_PKI_CERT"] = str(self.client_cert_path)
        os.environ["TENANT_NAME"] = self.tenant_name
        os.environ["DNS_NAME"] = self.dns_name
        os.environ["JSON_TENANT_CONFIG"] = json.dumps(config)
