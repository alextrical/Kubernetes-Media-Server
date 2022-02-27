# import pulumi
# from pulumi import Output
from pulumi_kubernetes.core.v1 import Namespace
from pulumi_kubernetes.helm.v3 import Release, ReleaseArgs, RepositoryOptsArgs
from pulumi_kubernetes.meta.v1 import ObjectMetaArgs

longhorn_ns = Namespace(
    "longhorn-system",
    metadata=ObjectMetaArgs(
        name="longhorn-system",
        labels={"name":"metallb-system"},
    )
)

# Deploy the longhorn chart.
longhorn = Release(
    "longhorn",
    ReleaseArgs(
		name="longhorn",
        chart="longhorn",
		namespace= "longhorn-system",
        repository_opts=RepositoryOptsArgs(
            repo="https://charts.longhorn.io",
        ),
    ),
)