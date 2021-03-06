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
"""`gcloud tasks queues update-pull-queue` command."""

from googlecloudsdk.api_lib.tasks import queues
from googlecloudsdk.calliope import base
from googlecloudsdk.command_lib.tasks import constants
from googlecloudsdk.command_lib.tasks import parsers
from googlecloudsdk.core import log


class UpdatePull(base.UpdateCommand):
  """Update a pull queue.

  The flags available to this command represent the fields of a pull queue
  that are mutable. Attempting to use this command on a different type of queue
  will result in an error.
  """

  @staticmethod
  def Args(parser):
    parsers.AddQueueResourceArg(parser, 'to update')
    parsers.AddPullQueueFlags(parser)

  def Run(self, args):
    queues_client = queues.Queues()
    queue_ref = parsers.ParseQueue(args.queue)
    configs = parsers.ParseCreateOrUpdateQueueArgs(
        args, constants.PULL_QUEUE, queues_client.api.messages)
    update_response = queues_client.Patch(queue_ref, *configs)
    log.status.Print('Updated queue [{}].'.format(queue_ref.Name()))
    return update_response
