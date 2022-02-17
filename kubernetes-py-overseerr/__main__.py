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

#----------overseerr----------
overseerr_labels = {"app": "overseerr"}
overseerr_config_persistent_volume_claim = kubernetes.core.v1.PersistentVolumeClaim("overseerr-conf-pvc",
    api_version="v1",
    kind="PersistentVolumeClaim",
    metadata=kubernetes.meta.v1.ObjectMetaArgs(
        labels=overseerr_labels,
        name="overseerr-conf-pvc",
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

overseerr = kubernetes.apps.v1.Deployment(
	"overseerr",
    metadata=kubernetes.meta.v1.ObjectMetaArgs(
        labels=overseerr_labels,
        name="overseerr",
        namespace=namespace,
    ),
	spec=kubernetes.apps.v1.DeploymentSpecArgs(
		replicas=1,
		selector=kubernetes.meta.v1.LabelSelectorArgs(
			match_labels=overseerr_labels,
		),
		template=kubernetes.core.v1.PodTemplateSpecArgs(
			metadata=kubernetes.meta.v1.ObjectMetaArgs(
				labels=overseerr_labels,
			),
			spec=kubernetes.core.v1.PodSpecArgs(
				containers=[kubernetes.core.v1.ContainerArgs(
					name="overseerr",
					image="lscr.io/linuxserver/overseerr",
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
                            #name="overseerr_PublishedServerUrl",
						    #value="192.168.0.5" #optional
					    #),
                        kubernetes.core.v1.EnvVarArgs(						
                            name="TZ",
						    value="Europe/London",
					    )
                    ],
                    volume_mounts=[{
                        "mount_path": "/config",
                        "name": "overseerr-conf-pvc",
                    }],
					ports=[kubernetes.core.v1.ContainerPortArgs(
						container_port=5055,
					)],
				)],
                volumes=[kubernetes.core.v1.VolumeArgs(
                    name="overseerr-conf-pvc",
                    persistent_volume_claim={
                        "claim_name": "overseerr-conf-pvc",
                    },
                )],
			),
		),
	))

overseerr_service = kubernetes.core.v1.Service(
	"overseerr",
	metadata=kubernetes.meta.v1.ObjectMetaArgs(
		name="overseerr",
		labels=overseerr_labels,
        namespace=namespace,
	),
	spec=kubernetes.core.v1.ServiceSpecArgs(
		type="ClusterIP",
		ports=[kubernetes.core.v1.ServicePortArgs(
			port=5055,
			#target_port=5055,
		)],
		selector=overseerr_labels,
	))