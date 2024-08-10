
from typing import Dict

from mojo.dataprofiles.basedataprofile import BaseDataProfile

class DatabaseBasicProfile(BaseDataProfile):

    def __init__(self, identifier: str, *, category: str, dbtype: str, dbname: str = None, credential: str = None):
        super().__init__(identifier, category=category, credential=credential)
        
        self._dbtype = dbtype
        self._dbname = dbname

        return
    
    @property
    def dbname(self) -> str:
        return self._dbname
    
    @property
    def dbtype(self) -> str:
        return self._dbtype

    @classmethod
    def validate(cls, profile_info: Dict[str, str]):
        return