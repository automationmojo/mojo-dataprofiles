
from typing import Dict, List, Optional, Union

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
    
    def load_datasource_profiles(self, configuration_info: dict, source_uris: Optional[List[str]] = None):
        
        if source_uris != None:
            self._source_uris.extend(source_uris)


        if configuration_info is not None and len(configuration_info) > 0:
            try:
                profiles_list = configuration_info["datasources"]
                errors, warnings = self._validate_datasource_profiles(profiles_list)

                if len(errors) == 0:
                    for profile in profiles_list:
                        # Copy the credential so if we modify it, we dont modify the
                        # original declaration.
                        profile = profile.copy()

                        if "identifier" not in profile:
                            errmsg = "Datasource profile items in 'datasources' must have an 'identifier' member."
                            raise ConfigurationError(errmsg)
                        ident = profile["identifier"]

                        if "category" not in credential and "categories" not in credential:
                            errmsg = "Credential items in 'environment/credentials' must have an 'category' or categories member."
                            raise ConfigurationError(errmsg)

                        # If we find a 'category' or 'categories' parameter we need to pass the categories along as a single
                        # list parameter 
                        categories = []
                        if "category" in credential:
                            category = credential["category"]
                            del credential["category"]

                            if isinstance(category, list):
                                categories = category
                            else:
                                categories = [ category]

                            credential["categories"] = categories
                        
                        elif "categories" in credential:
                            categories = credential["categories"]

                            if isinstance(categories, str):
                                categories = [ categories ]


                        # If the credential has more than one category, we create a simple `BasicCredential` which has a common set of
                        # attributes.  The only credential we support with common attributes is a simple 'username' and 'password' credetial 
                        if len(categories) > 1:

                            for category in categories:
                                if category not in ['basic', 'ssh', 'rest-basic']:
                                    errmsg = "The only categories of credentials that can be used together are ['basic', 'ssh (with password)', 'rest-basic']"
                                    raise ConfigurationError(errmsg)

                            if "username" in credential and "password" in credential:

                                username = credential["username"]
                                password = credential["password"]

                                BasicCredential.validate(credential)
                                credobj = BasicCredential(identifier=ident, categories=categories, username=username, password=password)
                                
                                self._credentials[ident] = credobj
                            
                            else:
                                errmsg = "Multi category credentials must have common attributes. Currently, the only common credential supporte is a 'username' and 'password' credential."
                                raise ConfigurationError(errmsg)

                        else:
                            category = categories[0]

                            if category == "api-token":
                                ApiTokenCredential.validate(credential)
                                credobj = ApiTokenCredential(**credential)
                                self._credentials[ident] = credobj

                            elif category == "aws-access-key":
                                AwsAccessKeyCredential.validate(credential)
                                credobj = AwsAccessKeyCredential(**credential)
                                self._credentials[ident] = credobj

                            elif category == 'azure-client-secret':
                                AzureClientSecretCredential.validate(credential)
                                credobj = AzureClientSecretCredential(**credential)
                                self._credentials[ident] = credobj

                            elif category == "basic" or category == "rest-basic":
                                BasicCredential.validate(credential)
                                credobj = BasicCredential(**credential)
                                self._credentials[ident] = credobj

                            elif category == "personal-api-token":
                                PersonalApiTokenCredential.validate(credential)
                                credobj = PersonalApiTokenCredential(**credential)
                                self._credentials[ident] = credobj

                            elif category == "public-key":
                                PublicKeyCredential.validate(credential)
                                credobj = PublicKeyCredential(**credential)
                                self._credentials[ident] = credobj

                            elif category == "ssh":
                                SshCredential.validate(credential)
                                credobj = SshCredential(**credential)
                                self._credentials[ident] = credobj

                            elif category == "wifi-choice":
                                WifiChoiceCredential.validate(credential)
                                credobj = WifiChoiceCredential(**credential)
                                self._credentials[ident] = credobj
                                
                            else:
                                warnmsg = f"Unknown category '{category}' found in credential '{ident}'"
                                logger.warn(warnmsg)

                else:
                    errmsg_lines = [
                        f"Errors found in credentials.",
                        "ERRORS:"
                    ]
                    for err in errors:
                        errmsg_lines.append(f"    {err}")

                    errmsg_lines.append("WARNINGS:")
                    for warn in warnings:
                        errmsg_lines.append(f"    {warn}")

                    errmsg_lines.append("SOURCE_URIS:")
                    for suri in self._source_uris:
                        errmsg_lines.append(f"    {suri}")

                    errmsg = os.linesep.join(errmsg_lines)
                    raise ConfigurationError(errmsg)

            except KeyError:
                errmsg = f"No 'credentials' field found."
                raise ConfigurationError(errmsg)
        return
    
    def _validate_datasource_profiles(self, profilesß_list: List[Dict[str, str]]):
        return