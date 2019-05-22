#!/usr/bin/env python3
# Pyvcloud Examples
#
# Copyright (c) 2018 VMware, Inc. All Rights Reserved.
#
# This product is licensed to you under the
# Apache License, Version 2.0 (the "License").
# You may not use this product except in compliance with the License.
#
# This product may include a number of subcomponents with
# separate copyright notices and license terms. Your use of the source
# code for the these subcomponents is subject to the terms and
# conditions of the subcomponent's license, as noted in the LICENSE file.
#
# Illustrates how to create, revert and remove snapshot from the VM in vApp.
#

import sys
from pyvcloud.vcd.client import BasicLoginCredentials
from pyvcloud.vcd.client import Client
from pyvcloud.vcd.client import UriObjectType
from pyvcloud.vcd.vm import VM
import requests

# Collect arguments.
if len(sys.argv) != 6:
    print("Usage: python3 {0} host org user password vmuuid".format(sys.argv[0]))
    sys.exit(1)
host = sys.argv[1]
org = sys.argv[2]
user = sys.argv[3]
password = sys.argv[4]
vmuuid = sys.argv[5]

# Disable warnings from self-signed certificates.
requests.packages.urllib3.disable_warnings()

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
task_monitor = client.get_task_monitor()

print("Fetching VM...")
vmhref = client.get_uriobject_uuid(vmuuid, UriObjectType.VM.value)
vm_resource = VM(client, href=vmhref)

print("Creating Snapshot...")
snaphot_resource = vm_resource.snapshot_create(memory=False, quiesce=False)
print("Waiting for Snapshot finish...")
task_monitor.wait_for_success(snaphot_resource)

print("Revert Back To Current Snapshot...")
vm_resource.reload()
snaphot_resource = vm_resource.snapshot_revert_to_current()
print("Waiting for Revert finish...")
task_monitor.wait_for_success(snaphot_resource)

print("Remove All Snapshot...")
snaphot_resource = vm_resource.snapshot_remove_all()
print("Waiting for Revert finish...")
task_monitor.wait_for_success(snaphot_resource)

# Log out.
print("Logging out")
client.logout()
