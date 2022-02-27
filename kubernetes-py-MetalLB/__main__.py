# import pulumi
# from pulumi import Output
# from pulumi_kubernetes.core.v1 import Service
from pulumi_kubernetes.helm.v3 import Release, ReleaseArgs, RepositoryOptsArgs

# Deploy the metallb/metallb chart.
metallb = Release(
    "metallb",
    ReleaseArgs(
		name="metallb",
        chart="metallb",
		namespace= "kube-system",
        repository_opts=RepositoryOptsArgs(
            repo="https://metallb.github.io/metallb",
        ),		
        values={
            "configInline": {
				"address-pools": {
					"name":"default",
					"protocal":"layer2",
					"addresses": "10.10.1.110-10.10.1.115",
				},
            },
        },
    ),
)