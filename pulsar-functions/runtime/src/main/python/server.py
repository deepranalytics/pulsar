#!/usr/bin/env python
#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#

# -*- encoding: utf-8 -*-

# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#
"""python_instance.py: Python Instance for running python functions
"""
from concurrent import futures
from log import Log
import grpc

import InstanceCommunication_pb2
import InstanceCommunication_pb2_grpc

class InstanceCommunicationServicer(InstanceCommunication_pb2_grpc.InstanceControlServicer):
  """Provides methods that implement functionality of route guide server."""

  def __init__(self, pyinstance):
    self.pyinstance = pyinstance

  def GetFunctionStatus(self, request, context):
    Log.info("Came in GetFunctionStatus")
    return self.pyinstance.get_function_status()

  def GetAndResetMetrics(self, request, context):
    Log.info("Came in GetAndResetMetrics")
    return self.pyinstance.get_and_reset_metrics()


def serve(port, pyinstance):
  server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
  InstanceCommunication_pb2_grpc.add_InstanceControlServicer_to_server(
    InstanceCommunicationServicer(pyinstance), server)
  server.add_insecure_port('[::]:%d' % port)
  Log.info("Serving InstanceCommunication on port %d" % int(port))
  server.start()
  return server
