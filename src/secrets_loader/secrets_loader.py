import os
from pathlib import Path
from typing import Any, Dict, Optional

from dotenv import load_dotenv


class SecretsLoader:
    _instance: Optional["SecretsLoader"] = None
    _loaded_env: Dict[str, Optional[str]] = {}
    _used_keys: set[str] = set()
    _filepath: Optional[str] = None

    def __new__(cls, filepath: Optional[str] = ".env") -> "SecretsLoader":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._filepath = filepath
            cls._load_initial_env(filepath)
        return cls._instance

    @classmethod
    def _load_initial_env(cls, filepath: Optional[str]) -> None:
        if filepath:
            env_file_path = Path(filepath)
            if env_file_path.exists():
                load_dotenv(dotenv_path=filepath, override=True)
                cls._loaded_env.update(os.environ)
            else:
                print(f"Warning: .env file not found at {filepath}")
        else:
            cls._loaded_env.update(os.environ)

        cls._load_docker_secrets()
        cls._load_github_actions_secrets()

    @classmethod
    def _load_docker_secrets(cls) -> None:
        print("DEBUG: _load_docker_secrets called")
        secrets_dir = Path("/run/secrets")
        if secrets_dir.is_dir():
            print(f"DEBUG: Secrets directory found: {secrets_dir}")
            for filename in secrets_dir.iterdir():
                print(f"DEBUG: Processing secret file: {filename}")
                try:
                    value = filename.read_text().strip()
                    cls._loaded_env[filename.name.upper()] = value
                    print(f"DEBUG: Loaded secret: {filename.name.upper()} = {value}")
                except IOError:
                    print(f"Warning: Could not read Docker Secret: {filename}")
        else:
            print("DEBUG: Secrets directory not found")

    @classmethod
    def _load_github_actions_secrets(cls) -> None:
        cls._loaded_env.update(os.environ)  # GitHub Actions secrets are in os.environ

    def get(self, key: str, default: Optional[str] = None) -> Optional[str]:
        upper_key = key.upper()
        if upper_key in self._loaded_env:
            self._used_keys.add(upper_key)
            return self._loaded_env[upper_key]
        return default

    @property
    def filepath(self) -> Optional[str]:
        return self._filepath

    @property
    def used_keys(self) -> set[str]:
        return set(self._used_keys)

    def __setattr__(self, name: str, value: Any) -> None:
        if name in self.__dict__:
            raise AttributeError(f"Cannot reassign instance attribute '{name}'")
        super().__setattr__(name, value)

    def __delattr__(self, name: str) -> None:
        if name in self.__dict__:
            raise AttributeError(f"Cannot delete instance attribute '{name}'")
        super().__delattr__(name)


# Example usage:
if __name__ == "__main__":
    loader1 = SecretsLoader(".env.example")
    api_key1 = loader1.get("API_KEY")
    db_url1 = loader1.get("DATABASE_URL", "default_url")
    print(f"Loader 1 - API Key: {api_key1}, DB URL: {db_url1}")
    print(f"Loader 1 - Filepath: {loader1.filepath}")
    print(f"Loader 1 - Used Keys: {loader1.used_keys}")

    loader2 = SecretsLoader()  # Uses default .env
    api_key2 = loader2.get("API_KEY")
    print(f"Loader 2 - API Key: {api_key2}")

    try:
        # Attempting to reassign the attribute should raise an error
        loader1.filepath = "another_path"  # type: ignore
    except AttributeError as e:
        print(f"Error: {e}")
