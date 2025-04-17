# src/secrets_loader/secrets_loader.pyi

from typing import Any, Dict, Optional, Set

class SecretsLoader:
    _instance: Optional["SecretsLoader"]
    _loaded_env: Dict[str, Optional[str]]
    _used_keys: Set[str]
    _filepath: Optional[str]

    def __new__(cls, filepath: Optional[str] = ...) -> "SecretsLoader": ...
    @classmethod
    def _load_initial_env(cls, filepath: Optional[str]) -> None: ...
    def get(self, key: str, default: Optional[str] = ...) -> Optional[str]: ...
    @property
    def filepath(self) -> Optional[str]: ...
    @property
    def used_keys(self) -> Set[str]: ...
    def __setattr__(self, name: str, value: Any) -> None: ...
    def __delattr__(self, name: str) -> None: ...
