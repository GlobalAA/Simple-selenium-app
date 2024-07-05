from os import path

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
	GITHUB_USER_USERNAME: str
	GITHUB_USER_PASSWORD: SecretStr

	model_config = SettingsConfigDict(
		env_file=path.join(path.dirname(__file__), '.env'),
		env_file_encoding='utf-8'
	)
	
config = Config()