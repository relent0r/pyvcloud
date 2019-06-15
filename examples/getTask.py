import sys
from pyvcloud.vcd.client import BasicLoginCredentials
from pyvcloud.vcd.client import Client
from pyvcloud.vcd.client import EntityType
from pyvcloud.vcd.client import UriObjectType
from pyvcloud.vcd.client import _TaskMonitor
from pyvcloud.vcd.org import Org
from pyvcloud.vcd.utils import extract_uuid_from_url
import requests

if len(sys.argv) != 6:
    print("Usage: python3 {0} host org user password vdc".format(sys.argv[0]))
    sys.exit(1)
host = sys.argv[1]
org = sys.argv[2]
user = sys.argv[3]
password = sys.argv[4]
task = sys.argv[5]

# Disable warnings from self-signed certificates.
requests.packages.urllib3.disable_warnings()

print("Logging in: host={0}, org={1}, user={2}".format(host, org, user))
client = Client(host,
                api_version='29.0',
                verify_ssl_certs=False,
                log_file='pyvcloud.log',
                log_requests=True,
                log_headers=True,
                log_bodies=True)
client.set_credentials(BasicLoginCredentials(user, org, password))
print("API URL is :" + client.get_api_uri())
print("API Version is :" + client.get_api_version())

taskhref = client.get_uriobject_uuid(task, UriObjectType.TASK.value)
print("Task HREF : " + taskhref)
task = _TaskMonitor(client)
task_resource= task._get_task_status(taskhref)
task_status = task.wait_for_success(task_resource)
print("Complete")