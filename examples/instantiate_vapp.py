from collections import namedtuple
import requests
import sys
import time
import yaml
from lxml import etree
from pyvcloud.vcd.client import E
from pyvcloud.vcd.client import Client
from pyvcloud.vcd.client import BasicLoginCredentials
from pyvcloud.vcd.client import UriObjectType
from pyvcloud.vcd.client import _TaskMonitor
from pyvcloud.vcd.vapp import VApp

if len(sys.argv) != 7:
    print("Usage: python3 {0} host org user password vdc_uuid configyaml".format(sys.argv[0]))
    sys.exit(1)
host = sys.argv[1]
org = sys.argv[2]
user = sys.argv[3]
password = sys.argv[4]
vdc_uuid = sys.argv[5]
config_yaml = sys.argv[6]

with open(config_yaml, "r") as config_file:
    config_dict = yaml.safe_load(config_file)
    cfg = namedtuple('ConfigObject', config_dict.keys())(**config_dict)

# Login. SSL certificate verification is turned off to allow self-signed
# certificates.  You should only do this in trusted environments.
print("Logging in: host={0}, org={1}, user={2}".format(host, org, user))
client = Client(host,
                api_version='27.0',
                verify_ssl_certs=False,
                log_file='pyvcloud.log',
                log_requests=True,
                log_headers=True,
                log_bodies=True)
client.set_credentials(BasicLoginCredentials(user, org, password))
print(client._uri)
vdc_href = Client.get_uriobject_uuid(client, vdc_uuid, UriObjectType.VDC.value)
vapp = VApp.instantiate_vapp(client, vdc_href, cfg)

#task_complete = _TaskMonitor.wait_for_success(client, vapp)
#self.client.get_task_monitor().wait_for_success(task)
print("Task Status :" + vapp)
