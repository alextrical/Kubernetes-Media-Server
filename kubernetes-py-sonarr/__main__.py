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

#----------sonarr----------
sonarr_labels = {"app": "sonarr"}
sonarr_config_persistent_volume_claim = kubernetes.core.v1.PersistentVolumeClaim("sonarr-conf-pvc",
    api_version="v1",
    kind="PersistentVolumeClaim",
    metadata=kubernetes.meta.v1.ObjectMetaArgs(
        labels=sonarr_labels,
        name="sonarr-conf-pvc",
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

sonarr = kubernetes.apps.v1.Deployment(
	"sonarr",
    metadata=kubernetes.meta.v1.ObjectMetaArgs(
        labels=sonarr_labels,
        name="sonarr",
        namespace=namespace,
    ),
	spec=kubernetes.apps.v1.DeploymentSpecArgs(
		replicas=1,
		selector=kubernetes.meta.v1.LabelSelectorArgs(
			match_labels=sonarr_labels,
		),
		template=kubernetes.core.v1.PodTemplateSpecArgs(
			metadata=kubernetes.meta.v1.ObjectMetaArgs(
				labels=sonarr_labels,
			),
			spec=kubernetes.core.v1.PodSpecArgs(
				containers=[kubernetes.core.v1.ContainerArgs(
					name="sonarr",
					image="lscr.io/linuxserver/sonarr",
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
                            #name="sonarr_PublishedServerUrl",
						    #value="192.168.0.5" #optional
					    #),
                        kubernetes.core.v1.EnvVarArgs(						
                            name="TZ",
						    value="Europe/London",
					    )
                    ],
                    volume_mounts=[{
                        "mount_path": "/config",
                        "name": "sonarr-conf-pvc",
                    }],
					ports=[kubernetes.core.v1.ContainerPortArgs(
						container_port=8989,
					)],
				)],
                volumes=[kubernetes.core.v1.VolumeArgs(
                    name="sonarr-conf-pvc",
                    persistent_volume_claim={
                        "claim_name": "sonarr-conf-pvc",
                    },
                )],
			),
		),
	))

sonarr_service = kubernetes.core.v1.Service(
	"sonarr",
	metadata=kubernetes.meta.v1.ObjectMetaArgs(
		name="sonarr",
		labels=sonarr_labels,
        namespace=namespace,
	),
	spec=kubernetes.core.v1.ServiceSpecArgs(
		type="ClusterIP",
		ports=[kubernetes.core.v1.ServicePortArgs(
			port=8989,
			#target_port=8989,
		)],
		selector=sonarr_labels,
	))