
from typing import List, Optional, Union

import os

from mojo.errors.exceptions import ConfigurationError

from mojo.dataprofiles.databasebasicprofile import DatabaseBasicProfile
from mojo.dataprofiles.databasebasictcpprofile import DatabaseBasicTcpProfile

class DataProfileManager:
    """
    """

    def __init__(self):

        self._profiles = {}
        self._source_uris = []

        return
    
    @property
    def profiles(self):
        return self._profiles
    
    def lookup_profile(self, profkey: str) -> Union[DatabaseBasicProfile, DatabaseBasicTcpProfile]:
        """
            Lookup a data source profile by key.
        """
        
        if profkey not in self._profiles:
            errmsg_lines = [
                f"Error missing data source profile '{profkey}'."
            ]
        
            if len(self._source_uris) > 0:
                errmsg_lines.append("PROFILES URIS:")

                for cfile in self._source_uris:
                    errmsg_lines.append(f"    {cfile}")

            errmsg = os.linesep.join(errmsg_lines)

            raise ConfigurationError(errmsg)

        profile = self._profiles[profkey]

        return profile
    
    def load_profiles(self, profile_info: dict, source_uris: Optional[List[str]] = None):
        
        if source_uris != None:
            self._source_uris.extend(source_uris)

        return