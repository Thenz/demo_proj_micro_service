#!/usr/bin/python
#
# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import random
import time
import json
import traceback
from concurrent import futures

import googleclouddebugger
import googlecloudprofiler
from google.auth.exceptions import DefaultCredentialsError
import grpc
from opencensus.trace.exporters import print_exporter
from opencensus.trace.exporters import stackdriver_exporter
from opencensus.trace.ext.grpc import server_interceptor
from opencensus.common.transports.async_ import AsyncTransport
from opencensus.trace.samplers import always_on

import demo_pb2
import demo_pb2_grpc
from grpc_health.v1 import health_pb2
from grpc_health.v1 import health_pb2_grpc

from logger import getJSONLogger
logger = getJSONLogger('reviewservice-server')

def initStackdriverProfiling():
  project_id = None
  try:
    project_id = os.environ["GCP_PROJECT_ID"]
  except KeyError:
    # Environment variable not set
    pass

  for retry in range(1,4):
    try:
      if project_id:
        googlecloudprofiler.start(service='review_server', service_version='1.0.0', verbose=0, project_id=project_id)
      else:
        googlecloudprofiler.start(service='review_server', service_version='1.0.0', verbose=0)
      logger.info("Successfully started Stackdriver Profiler.")
      return
    except (BaseException) as exc:
      logger.info("Unable to start Stackdriver Profiler Python agent. " + str(exc))
      if (retry < 4):
        logger.info("Sleeping %d seconds to retry Stackdriver Profiler agent initialization"%(retry*10))
        time.sleep (1)
      else:
        logger.warning("Could not initialize Stackdriver Profiler after retrying, giving up")
  return

class ReviewService(demo_pb2_grpc.ReviewServiceServicer):
    def ListReviews(self, request, context):

        # id of viewed product
        product_id = str(request.product_id[0])

        # log product id
        logger.info("[ListReviews product_id] product_id={}".format(product_id))

        # prepare response
        response = demo_pb2.ListReviewsResponse()

        # read reviews.json file
        if "reviews.json" in os.listdir():
            with open("reviews.json", "r") as f:
                reviews = json.loads(f.read())

            for product in reviews["products"]:

                if (product["id"] == product_id):
                    # build response
                    rev = response.reviews.add()
                    rev.id    = product["id"]
                    rev.name  = product["name"]
                    rev.user  = product["user"]
                    rev.stars = product["stars"]
                    rev.text  = product["review"]

                    # log product ids
                    logger.info("[product] product={}".format(product))

        # log review response
        logger.info("[ListReviews response] response={}".format(response))

        return response


    def Check(self, request, context):
        return health_pb2.HealthCheckResponse(
            status=health_pb2.HealthCheckResponse.SERVING)

    def Watch(self, request, context):
        return health_pb2.HealthCheckResponse(
            status=health_pb2.HealthCheckResponse.UNIMPLEMENTED)


if __name__ == "__main__":
    logger.info("initializing reviewservice")

    try:
      if "DISABLE_PROFILER" in os.environ:
        raise KeyError()
      else:
        logger.info("Profiler enabled.")
        initStackdriverProfiling()
    except KeyError:
        logger.info("Profiler disabled.")

    try:
      if "DISABLE_TRACING" in os.environ:
        raise KeyError()
      else:
        logger.info("Tracing enabled.")
        sampler = always_on.AlwaysOnSampler()
        exporter = stackdriver_exporter.StackdriverExporter(
          project_id=os.environ.get('GCP_PROJECT_ID'),
          transport=AsyncTransport)
        tracer_interceptor = server_interceptor.OpenCensusServerInterceptor(sampler, exporter)
    except (KeyError, DefaultCredentialsError):
        logger.info("Tracing disabled.")
        tracer_interceptor = server_interceptor.OpenCensusServerInterceptor()


    try:
      if "DISABLE_DEBUGGER" in os.environ:
        raise KeyError()
      else:
        logger.info("Debugger enabled.")
        try:
          googleclouddebugger.enable(
              module='reviewserver',
              version='1.0.0'
          )
        except (Exception, DefaultCredentialsError):
            logger.error("Could not enable debugger")
            logger.error(traceback.print_exc())
            pass
    except (Exception, DefaultCredentialsError):
        logger.info("Debugger disabled.")

    port = os.environ.get('PORT', "8080")

    # create gRPC server
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10),
                      interceptors=(tracer_interceptor,))

    # add class to gRPC server
    service = ReviewService()
    demo_pb2_grpc.add_ReviewServiceServicer_to_server(service, server)
    health_pb2_grpc.add_HealthServicer_to_server(service, server)

    # start server
    logger.info("listening on port: " + port)
    server.add_insecure_port('[::]:'+port)
    server.start()

    # keep alive
    try:
         while True:
            time.sleep(10000)
    except KeyboardInterrupt:
            server.stop(0)
