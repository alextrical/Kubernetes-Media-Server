#  Copyright 2016-2020, Pulumi Corporation.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import pulumi
from service_deployment import ServiceDeployment

ServiceDeployment(
    "jackett",
    image="lscr.io/linuxserver/jackett",
    ports=[9117],
    resources= { "requests": { "cpu": "100m", "memory": "100Mi" }, "limits": { "cpu": "500m", "memory": "500Mi" } },
    namespace="media"
    )
# ServiceDeployment(
#     "sonarr",
#     image="lscr.io/linuxserver/sonarr",
#     ports=[8989])
# frontend = ServiceDeployment(
#     "frontend",
#     image="pulumi/guestbook-php-redis",
#     replicas=3,
#     ports=[80],
#     allocate_ip_address=True)

# pulumi.export("frontend_ip", frontend.ip_address)
