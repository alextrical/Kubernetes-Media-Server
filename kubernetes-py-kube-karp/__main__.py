import pulumi
import pulumi_kubernetes as k8s

"""kube-karp container, replicated 1 time."""
app_name = "kube-karp"
app_labels = { "app": app_name }

kube_karp = k8s.apps.v1.Deployment(
            app_name,
            spec=k8s.apps.v1.DeploymentSpecArgs(
                replicas=1,
                selector=k8s.meta.v1.LabelSelectorArgs(match_labels=app_labels),
                template=k8s.core.v1.PodTemplateSpecArgs(
                    metadata=k8s.meta.v1.ObjectMetaArgs(labels=app_labels),
                    spec=k8s.core.v1.PodSpecArgs(
                        containers=[k8s.core.v1.ContainerArgs(
                                name=app_name,
                                image="immanuelfodor/kube-karp",
                                # resources=k8s.core.v1.ResourceRequirementsArgs(
                                #     requests={
                                #         "cpu": "100m",
                                #         "memory": "100Mi",
                                #     },
                                # ),
                                env=[k8s.core.v1.EnvVarArgs(
                                    name="virtualIp",
                                    value="10.10.1.100",
                                ), #Im hoping theres a cleaner way to define additional env vars than this?
                                k8s.core.v1.EnvVarArgs(
                                    name="interface",
                                    value="enp1s0",
                                )],
                            ),
                        ]
                    ),
                ),
            )
		)