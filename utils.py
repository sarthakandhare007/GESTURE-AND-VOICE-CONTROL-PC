import logging

def setup_logging():
    logging.basicConfig(
        filename="pc_control.log",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )

def log_command(command):
    logging.info(f"Command executed: {command}")