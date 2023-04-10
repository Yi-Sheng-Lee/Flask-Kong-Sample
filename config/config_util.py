import os
from .config import DevelopmentConfig, ProductionConfig
import logging

logger = logging.getLogger(__name__)


class ConfigUtils:
    def __init__(self):
        self.config_by_name = dict(
            develop=DevelopmentConfig, production=ProductionConfig,
        )

        self.mode = os.getenv("PROD_ENV") or "develop"
        self.config = self.get_current_config()

    def get_current_config(self):
        logger.info(f'Init config with env {self.mode}')
        return self.config_by_name[self.mode]
