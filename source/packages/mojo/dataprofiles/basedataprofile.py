
from typing import Optional, Union

class BaseDataProfile:
    """
        The :class:`BaseDataProfiles` object serves as a base class for data source profile objects.
    """
    def __init__(self, identifier: str, *, category: str, credential: Optional[str] = None):
        self._identifier = identifier
        self._category = category
        self._credential = credential
        return

    @property
    def credential(self) -> Union[str, None]:
        return self._credential

    @property
    def identifier(self) -> str:
        return self._identifier

    @property
    def category(self) -> str:
        return self._category
