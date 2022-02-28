from pulumi_kubernetes.helm.v3 import Release, ReleaseArgs, RepositoryOptsArgs

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