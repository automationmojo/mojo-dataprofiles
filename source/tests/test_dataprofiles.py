
import os
import tempfile
import unittest
import yaml

from mojo.dataprofiles.dataprofilemanager import DataProfileManager
from mojo.dataprofiles.databasebasictcpprofile import DatabaseBasicTcpProfile

LANDSCAPE_CONTENT = """
dataprofiles:
    -   identifier: basic-database
        category: basic-tcp
        dbtype: postgres
        dbname: testdb
        host: somedb.somecompany.com
        port: 8888
        credential: dbadmin
"""

class TestCredentials(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:

        cls.landscape_file = tempfile.mktemp(suffix=".yaml")

        with open(cls.landscape_file, 'w') as cf:
            cf.write(LANDSCAPE_CONTENT)

        landscape_info = None
        with open(cls.landscape_file, 'r') as cf:
            landscape_info = yaml.safe_load(cf)

        cls.profile_mgr = DataProfileManager()
        cls.profile_mgr.load_datasource_profiles(landscape_info, source_uris=[cls.landscape_file])

        return
    
    @classmethod
    def tearDownClass(cls) -> None:
        os.remove(cls.landscape_file)
        return
    
    def test_basic_tcp_profile(self):

        datasource_profiles = self.profile_mgr.profiles

        profile_name = 'basic-database'
        assert profile_name in datasource_profiles, f"There should have been a '{profile_name}' profile."

        testprofile = self.profile_mgr.lookup_profile(profile_name)

        assert isinstance(testprofile, DatabaseBasicTcpProfile), "The datasource profile returned should have been an 'DatabaseBasicTcpProfile'"

        return

if __name__ == '__main__':
    unittest.main()
