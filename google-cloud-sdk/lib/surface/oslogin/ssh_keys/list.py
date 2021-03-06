# Copyright 2017 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Implements command to remove an SSH Public Key from the OS Login Profile."""

from googlecloudsdk.api_lib.oslogin import client
from googlecloudsdk.calliope import base
from googlecloudsdk.command_lib.oslogin import oslogin_utils
from googlecloudsdk.core import properties


def _TransformExpiry(resource, undefined=None):
  display = None
  value = resource.get('value')
  if value:
    display = oslogin_utils.ConvertUsecToRfc3339(
        value.get('expirationTimeUsec'))

  return display or undefined


@base.ReleaseTracks(base.ReleaseTrack.ALPHA)
class List(base.ListCommand):
  """List the SSH Public Keys from an OS Login Profile."""

  def __init__(self, *args, **kwargs):
    super(List, self).__init__(*args, **kwargs)

  @staticmethod
  def Args(parser):
    base.URI_FLAG.RemoveFromParser(parser)
    parser.display_info.AddFormat("""
          table(
            key:label=FINGERPRINT,
            expiry():label=EXPIRY
          )
        """)

    parser.display_info.AddTransforms({
        'expiry': _TransformExpiry
    })

  def Run(self, args):
    """See ssh_utils.BaseSSHCLICommand.Run."""

    oslogin_client = client.OsloginClient(self.ReleaseTrack())
    user_email = properties.VALUES.core.account.Get()

    keys = oslogin_utils.GetKeysFromProfile(user_email, oslogin_client)
    return keys

List.detailed_help = {
    'brief': 'List SSH Public Keys from an OS Login Profile.',
}

