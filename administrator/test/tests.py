import unittest
import tempfile
import os
import logging
import administrator
import sys
import json
import md5

class AdministratorTests(unittest.TestCase):


    """
    Request convenience methods
    """

    def add_jobs(self, jobs, admin_id, password):
        return self.app.post('/add', data=dict(
          jobs=json.dumps(jobs),
          administrator_id=admin_id,
          password=password), follow_redirects=True)

    def get_job(self, admin_id):
        return self.app.post('/get', data=dict(
            administrator_id=admin_id))

    def confirm_job(self, admin_id, job_id):
        return self.app.post('/confirm', data=dict(
            administrator_id=admin_id,
            job_id = job_id))

    """
    Re-usable structs
    """
    abc_aid = "abc"
    abc_jobs = [{"job_secret": "a"},
                {"job_secret": "b"},
                {"job_secret": "c"}]

    """
    Test setUp
    """

    def setUp(self):
        self.db_fd, administrator.app.config['DATABASE'] = tempfile.mkstemp()
        administrator.app.config['TESTING'] = True
        administrator.app.config['PASSWORD_HASH'] = md5.new('real_password').digest()
        self.app = administrator.app.test_client()
        administrator.init_db()

        # Set up logging if you want
        logging.basicConfig( stream=sys.stderr )
        # logging.getLogger("AdministratorTests.test_get_job").setLevel(logging.DEBUG)

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(administrator.app.config['DATABASE'])

    def test_add_jobs_password(self):
        log = logging.getLogger( "AdministratorTests.test_db_has_administrator_table")
        rv = self.add_jobs(self.abc_jobs, self.abc_aid, "fake_password")
        self.assertIn("Password invalid", rv.data)

        rv = self.add_jobs(self.abc_jobs, self.abc_aid, "real_password")
        self.assertIn("Jobs added", rv.data)

    def test_get_job_empty(self):
        rv = self.get_job(self.abc_aid)
        self.assertIn("No jobs available", rv.data)

    def test_get_job(self):
        log = logging.getLogger( "AdministratorTests.test_get_job")
        
        rv = self.add_jobs(self.abc_jobs, self.abc_aid, "real_password")

        log.debug("abc_aid = %s", self.abc_aid)
        rv = self.get_job(self.abc_aid)
        log.debug("get_job response mimetype is '%s'", rv.mimetype)
        log.debug("get_job response payload is '%s'", rv.data)
        self.assertEqual(rv.mimetype, 'application/json')

        payload = json.loads(rv.data)["payload"]
        self.assertIn(payload["job_secret"], "abc")

    def test_exhaust_jobs(self):
        self.add_jobs(self.abc_jobs, self.abc_aid, "real_password")
        
        rv = self.get_job(self.abc_aid)
        self.assertNotIn("No jobs available", rv.data)
        rv = self.get_job(self.abc_aid)
        self.assertNotIn("No jobs available", rv.data)
        rv = self.get_job(self.abc_aid)
        self.assertNotIn("No jobs available", rv.data)

        rv = self.get_job(self.abc_aid)
        self.assertIn("No jobs available", rv.data)

    def test_confirm_job(self):
        self.add_jobs(self.abc_jobs, self.abc_aid, "real_password")
        
        rv = self.get_job(self.abc_aid)
        job_id = json.loads(rv.data)['job_id']

        rv = self.confirm_job(self.abc_aid, job_id)
        self.assertIn("Job confirmed complete", rv.data)

    # def test_confirm_unowned_job(self):

    # def test_timeout_job

if __name__ == '__main__':
    unittest.main()