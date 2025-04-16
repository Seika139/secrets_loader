import os

from dotenv import load_dotenv


class SecretsLoader:
    _instance = None
    _loaded_env: dict[str, str | None] = {}
    _used_keys: set[str] = set()
    _filepath: str | None = None

    def __new__(cls, filepath: str | None = ".env") -> "SecretsLoader":
        if cls._instance is None:
            cls._instance = super(SecretsLoader, cls).__new__(cls)
            cls._filepath = filepath
            cls._load_initial_env(filepath)
        return cls._instance

    @classmethod
    def _load_initial_env(cls, filepath: str | None) -> None:
        if filepath:
            load_dotenv(dotenv_path=filepath, override=True)
            cls._loaded_env.update(os.environ)
        else:
            cls._loaded_env.update(os.environ)

        # Docker Compose secrets の読み込み (存在する場合)
        secrets_dir = "/run/secrets"
        if os.path.isdir(secrets_dir):
            for filename in os.listdir(secrets_dir):
                secret_path = os.path.join(secrets_dir, filename)
                try:
                    with open(secret_path, "r") as f:
                        value = f.read().strip()
                        if filename.upper() not in cls._loaded_env:
                            cls._loaded_env[filename.upper()] = value
                except IOError:
                    pass

        # GitHub Actions secrets の優先的な読み込み (環境変数として設定されている)
        for key, value in os.environ.items():
            if key not in cls._loaded_env:
                cls._loaded_env[key] = value

    def get(self, key: str, default: str | None = None) -> str | None:
        upper_key = key.upper()
        if upper_key in self._loaded_env:
            self._used_keys.add(upper_key)
            return self._loaded_env[upper_key]
        return default

    @property
    def filepath(self) -> str | None:
        return self._filepath

    @property
    def used_keys(self) -> set[str]:
        return set(self._used_keys)

    def __setattr__(self, name: str, value: str) -> None:
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
