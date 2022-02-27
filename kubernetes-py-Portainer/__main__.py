# import pulumi
# from pulumi import Output
# from pulumi_kubernetes.core.v1 import Service
# from pulumi_kubernetes.core.v1 import Namespace
from pulumi_kubernetes.helm.v3 import Release, ReleaseArgs, RepositoryOptsArgs
# from pulumi_kubernetes.meta.v1 import ObjectMetaArgs

# longhorn_ns = Namespace(
#     "portainer-system",
#     metadata=ObjectMetaArgs(
#         name="portainer-system",
#         labels={"name":"portainer-system"},
#     )
# )

# Deploy the portainer chart.
portainer = Release(
    "portainer",
    ReleaseArgs(
		name="portainer",
        chart="portainer",
		namespace= "kube-system",
        repository_opts=RepositoryOptsArgs(
            repo="https://portainer.github.io/k8s",
        ),		
        values={
            "service": {
                "httpPort": 80,
                #"type": "LoadBalancer",
            },
        },
    ),
)