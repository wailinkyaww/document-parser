from .logger import get_logger
from pydantic_settings import BaseSettings
from pydantic import Field, ValidationError

logger = get_logger(__file__)


# pydantic BaseSettings will automatically load from env.
# list all the env variables here
class Settings(BaseSettings):
    API_KEY: str = Field(..., description="API Key is used for securing endpoints.")


config: Settings


def initialize_config():
    try:
        logger.info('Validating env variables.')
        global config
        config = Settings()
    except ValidationError as e:
        for missing_var in [err['loc'][0] for err in e.errors()]:
            logger.error(f"Invalid env variable: {missing_var}")

        logger.info("Shutting down the server.")
        raise SystemExit
