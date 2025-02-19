import sys
import subprocess
from loguru import logger
from .ssl import DshCertificateManager

def main():
    """Main entrypoint function"""
    try:
        # Set up certificates
        cert_manager = DshCertificateManager()
        cert_manager.setup_certificates()
        
        # Execute the command passed to the entrypoint
        if len(sys.argv) > 1:
            cmd = sys.argv[1:]
            logger.info(f"Executing command: {' '.join(cmd)}")
            subprocess.run(cmd, check=True)
        else:
            logger.error("No command specified")
            sys.exit(1)
            
    except Exception as e:
        logger.error(f"Error in entrypoint: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 