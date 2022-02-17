#import pulumi
import pulumi_kubernetes as kubernetes

namespace = "media"

#----------namespace----------
# media_namespace = kubernetes.core.v1.Namespace("media-Namespace",
#     api_version="v1",
#     kind="Namespace",
#     metadata=kubernetes.meta.v1.ObjectMetaArgs(
#         name=namespace,
#     ))

#----------jackett----------
jackett_labels = {"app": "jackett"}
jackett_config_persistent_volume_claim = kubernetes.core.v1.PersistentVolumeClaim("jackett-conf-pvc",
    api_version="v1",
    kind="PersistentVolumeClaim",
    metadata=kubernetes.meta.v1.ObjectMetaArgs(
        labels=jackett_labels,
        name="jackett-conf-pvc",
        namespace=namespace,
    ),
    spec=kubernetes.core.v1.PersistentVolumeClaimSpecArgs(
        access_modes=["ReadWriteOnce"],
        storage_class_name="longhorn",
        resources=kubernetes.core.v1.ResourceRequirementsArgs(
            requests={
                "storage": "1Gi",
            },
        ),
    ))

jackett = kubernetes.apps.v1.Deployment(
	"jackett",
    metadata=kubernetes.meta.v1.ObjectMetaArgs(
        labels=jackett_labels,
        name="jackett",
        namespace=namespace,
    ),
	spec=kubernetes.apps.v1.DeploymentSpecArgs(
		replicas=1,
		selector=kubernetes.meta.v1.LabelSelectorArgs(
			match_labels=jackett_labels,
		),
		template=kubernetes.core.v1.PodTemplateSpecArgs(
			metadata=kubernetes.meta.v1.ObjectMetaArgs(
				labels=jackett_labels,
			),
			spec=kubernetes.core.v1.PodSpecArgs(
				containers=[kubernetes.core.v1.ContainerArgs(
					name="jackett",
					image="lscr.io/linuxserver/jackett",
					resources=kubernetes.core.v1.ResourceRequirementsArgs(
						requests={
							"cpu": "100m",
							"memory": "100Mi",
						},
					),
					env=[
                        kubernetes.core.v1.EnvVarArgs(						
                            name="PUID",
						    value="1000",
					    ),
                        kubernetes.core.v1.EnvVarArgs(						
                            name="PGID",
						    value="1000",
					    ),
                        #kubernetes.core.v1.EnvVarArgs(
                            #name="jackett_PublishedServerUrl",
						    #value="192.168.0.5" #optional
					    #),
                        kubernetes.core.v1.EnvVarArgs(						
                            name="TZ",
						    value="Europe/London",
					    )
                    ],
                    volume_mounts=[{
                        "mount_path": "/config",
                        "name": "jackett-conf-pvc",
                    }],
					ports=[kubernetes.core.v1.ContainerPortArgs(
						container_port=9117,
					)],
				)],
                volumes=[kubernetes.core.v1.VolumeArgs(
                    name="jackett-conf-pvc",
                    persistent_volume_claim={
                        "claim_name": "jackett-conf-pvc",
                    },
                )],
			),
		),
	))

jackett_service = kubernetes.core.v1.Service(
	"jackett",
	metadata=kubernetes.meta.v1.ObjectMetaArgs(
		name="jackett",
		labels=jackett_labels,
        namespace=namespace,
	),
	spec=kubernetes.core.v1.ServiceSpecArgs(
		type="ClusterIP",
		ports=[kubernetes.core.v1.ServicePortArgs(
			port=9117,
			#target_port=9117,
		)],
		selector=jackett_labels,
	))