import logging

logger = logging.basicConfig(
    level=logging.INFO,  # This is the important line
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
)
