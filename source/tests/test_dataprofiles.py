
import os
import tempfile
import unittest
import yaml

from mojo.dataprofiles.dataprofilemanager import DataProfileManager

from mojo.dataprofiles.databasebasictcpprofile import DatabaseBasicTcpProfile
from mojo.dataprofiles.couchdbprofile import CouchDbProfile
from mojo.dataprofiles.mongodbatlasprofile import MongoDBAtlasProfile
from mojo.dataprofiles.snowflakeprofile import SnowflakeProfile

LANDSCAPE_CONTENT = """
dataprofiles:
    -   identifier: basic-database
        category: basic-tcp
        dbtype: postgres
        dbname: testdb
        host: somedb.somecompany.com
        port: 8888
        credential: dbadmin
    -   identifier: mongodb-example
        category: mongodb-atlas
        connection: "mongodb+srv://<username>:<password>@automation-mojo-db.q0jpg0g.mongodb.net/"
        credential: dbadmin
    -   identifier: couchdb-example
        category: couchdb
        dbname: testdb
        host: somedb.somecompany.com
        port: 8888
        credential: dbadmin
    -   identifier: snowflake-example
        category: snowflake
        account: some-account 
        warehouse: some-warehouse
        database: some-database
        schema: some-schema
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
    
    def test_couchdb_profile(self):

        datasource_profiles = self.profile_mgr.profiles

        profile_name = 'couchdb-example'
        assert profile_name in datasource_profiles, f"There should have been a '{profile_name}' profile."

        testprofile = self.profile_mgr.lookup_profile(profile_name)

        assert isinstance(testprofile, CouchDbProfile), "The datasource profile returned should have been an 'CouchDbProfile'"

        return

    def test_mongodb_atlas_profile(self):

        datasource_profiles = self.profile_mgr.profiles

        profile_name = 'mongodb-example'
        assert profile_name in datasource_profiles, f"There should have been a '{profile_name}' profile."

        testprofile = self.profile_mgr.lookup_profile(profile_name)

        assert isinstance(testprofile, MongoDBAtlasProfile), "The datasource profile returned should have been an 'MongoDBAtlasProfile'"

        return

    def test_snowflake_profile(self):

        datasource_profiles = self.profile_mgr.profiles

        profile_name = 'snowflake-example'
        assert profile_name in datasource_profiles, f"There should have been a '{profile_name}' profile."

        testprofile = self.profile_mgr.lookup_profile(profile_name)

        assert isinstance(testprofile, SnowflakeProfile), "The datasource profile returned should have been an 'SnowflakeProfile'"

        return


if __name__ == '__main__':
    unittest.main()
