
from typing import Optional, Union

class BaseDataProfile:

    def __init__(self, name: str, *, profile_type: str, credential: Optional[str] = None):
        self._name = name
        self._profile_type = profile_type
        self._credential = credential
        return

    @property
    def credential(self) -> Union[str, None]:
        return self._credential

    @property
    def name(self) -> str:
        return self._name

    @property
    def profile_type(self) -> str:
        return self._profile_type
