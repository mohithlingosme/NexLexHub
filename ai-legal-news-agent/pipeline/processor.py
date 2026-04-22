import logging
from abc import ABC, abstractmethod
from utils.file_utils import load_json, save_json

logger = logging.getLogger(__name__)

class Processor(ABC):
    @abstractmethod
    def process(self, articles):
        pass

def main():
    # Stub for generic processing
    logger.info("Generic processor stub - extend for custom processing")

