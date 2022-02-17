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

#----------lidarr----------
lidarr_labels = {"app": "lidarr"}
lidarr_config_persistent_volume_claim = kubernetes.core.v1.PersistentVolumeClaim("lidarr-conf-pvc",
    api_version="v1",
    kind="PersistentVolumeClaim",
    metadata=kubernetes.meta.v1.ObjectMetaArgs(
        labels=lidarr_labels,
        name="lidarr-conf-pvc",
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

lidarr = kubernetes.apps.v1.Deployment(
	"lidarr",
    metadata=kubernetes.meta.v1.ObjectMetaArgs(
        labels=lidarr_labels,
        name="lidarr",
        namespace=namespace,
    ),
	spec=kubernetes.apps.v1.DeploymentSpecArgs(
		replicas=1,
		selector=kubernetes.meta.v1.LabelSelectorArgs(
			match_labels=lidarr_labels,
		),
		template=kubernetes.core.v1.PodTemplateSpecArgs(
			metadata=kubernetes.meta.v1.ObjectMetaArgs(
				labels=lidarr_labels,
			),
			spec=kubernetes.core.v1.PodSpecArgs(
				containers=[kubernetes.core.v1.ContainerArgs(
					name="lidarr",
					image="lscr.io/linuxserver/lidarr",
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
                            #name="lidarr_PublishedServerUrl",
						    #value="192.168.0.5" #optional
					    #),
                        kubernetes.core.v1.EnvVarArgs(						
                            name="TZ",
						    value="Europe/London",
					    )
                    ],
                    volume_mounts=[{
                        "mount_path": "/config",
                        "name": "lidarr-conf-pvc",
                    }],
					ports=[kubernetes.core.v1.ContainerPortArgs(
						container_port=8686,
					)],
				)],
                volumes=[kubernetes.core.v1.VolumeArgs(
                    name="lidarr-conf-pvc",
                    persistent_volume_claim={
                        "claim_name": "lidarr-conf-pvc",
                    },
                )],
			),
		),
	))

lidarr_service = kubernetes.core.v1.Service(
	"lidarr",
	metadata=kubernetes.meta.v1.ObjectMetaArgs(
		name="lidarr",
		labels=lidarr_labels,
        namespace=namespace,
	),
	spec=kubernetes.core.v1.ServiceSpecArgs(
		type="ClusterIP",
		ports=[kubernetes.core.v1.ServicePortArgs(
			port=8686,
			#target_port=8686,
		)],
		selector=lidarr_labels,
	))