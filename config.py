import os
import yaml
from pathlib import Path


class Config:
    def __init__(self):
        self._config = self._load_config()

    def _load_config(self):
        # Load the base config file
        env = os.getenv("FLASK_ENV", "development")
        config_path = Path(__file__).parent / f"config.{env}.yml"

        # Fall back to default config if environment-specific one doesn't exist
        if not config_path.exists():
            config_path = Path(__file__).parent / "config.yml"

        with open(config_path) as f:
            return yaml.safe_load(f)

    def __getattr__(self, name):
        """Allow getting config values as attributes"""
        if name.isupper():  # Flask expects uppercase config keys
            # Handle special cases for Flask-SQLAlchemy
            if name == "SQLALCHEMY_DATABASE_URI":
                return (
                    self._config["database"]["postgresql"]["uri"]
                    if self._config["database"]["type"] == "postgresql"
                    else None
                )
            elif name == "SQLALCHEMY_TRACK_MODIFICATIONS":
                return self._config["database"]["postgresql"]["track_modifications"]

            # Convert nested dict keys to uppercase for Flask compatibility
            for section in self._config:
                if isinstance(self._config[section], dict):
                    for key in self._config[section]:
                        if f"{section}_{key}".upper() == name:
                            return self._config[section][key]
                elif section.upper() == name:
                    return self._config[section]
        return None

    def get(self, name, default=None):
        """Get a config value with a default fallback"""
        try:
            # Handle nested keys with dot notation
            keys = name.split(".")
            value = self._config
            for key in keys:
                value = value[key]
            return value
        except:
            return default
