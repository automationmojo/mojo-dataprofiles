
from typing import Dict

from mojo.dataprofiles.basedataprofile import BaseDataProfile

class DatabaseBasicTcpProfile(BaseDataProfile):

    def __init__(self, name: str, *, profile_type: str, host: str, port: int, dbtype: str, dbname: str = None, credential: str = None):
        super().__init__(name, profile_type=profile_type, credential=credential)
        
        self._host = host
        self._port = port
        self._dbtype = dbtype
        self._dbname = dbname

        return
    
    @property
    def dbname(self) -> str:
        return self._dbname
    
    @property
    def dbtype(self) -> str:
        return self._dbtype
    
    @property
    def host(self) -> str:
        return self._host
    
    @property
    def port(self) -> int:
        return self._port

    @classmethod
    def validate(cls, profile_info: Dict[str, str]):
        return