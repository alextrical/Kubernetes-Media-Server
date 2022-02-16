import pulumi
from pulumi_kubernetes.apps.v1 import Deployment, DeploymentSpecArgs
from pulumi_kubernetes.core.v1 import (
	ContainerArgs,
	ContainerPortArgs,
	EnvVarArgs,
	PodSpecArgs,
	PodTemplateSpecArgs,
	ResourceRequirementsArgs,
	Service,
	ServicePortArgs,
	ServiceSpecArgs,
)
from pulumi_kubernetes.meta.v1 import LabelSelectorArgs, ObjectMetaArgs

# jellyfin
jellyfin_labels = {
	"app": "jellyfin",
}

jellyfin_deployment = Deployment(
	"jellyfin",
	spec=DeploymentSpecArgs(
		selector=LabelSelectorArgs(
			match_labels=jellyfin_labels,
		),
		replicas=1,
		template=PodTemplateSpecArgs(
			metadata=ObjectMetaArgs(
				labels=jellyfin_labels,
			),
			spec=PodSpecArgs(
				containers=[ContainerArgs(
					name="jellyfin",
					image="lscr.io/linuxserver/jellyfin",
					resources=ResourceRequirementsArgs(
						requests={
							"cpu": "100m",
							"memory": "100Mi",
						},
					),
					env=[EnvVarArgs(						
                        name="PUID",
						value="1000",
					),EnvVarArgs(						
                        name="PGID",
						value="1000",
					),
                    #EnvVarArgs(
                        #name="JELLYFIN_PublishedServerUrl",
						#value="192.168.0.5" #optional
					#),
                    EnvVarArgs(						
                        name="TZ",
						value="Europe/London",
					)],
					ports=[ContainerPortArgs(
						container_port=8096,
					)],
				)],
			),
		),
	))

jellyfin_service = Service(
	"jellyfin",
	metadata=ObjectMetaArgs(
		name="jellyfin",
		labels=jellyfin_labels,
	),
	spec=ServiceSpecArgs(
		type="ClusterIP",
		ports=[ServicePortArgs(
			port=80,
			target_port=8096,
		)],
		selector=jellyfin_labels,
	))