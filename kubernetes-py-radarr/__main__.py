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

#----------radarr----------
radarr_labels = {"app": "radarr"}
radarr_config_persistent_volume_claim = kubernetes.core.v1.PersistentVolumeClaim("radarr-conf-pvc",
    api_version="v1",
    kind="PersistentVolumeClaim",
    metadata=kubernetes.meta.v1.ObjectMetaArgs(
        labels=radarr_labels,
        name="radarr-conf-pvc",
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

radarr = kubernetes.apps.v1.Deployment(
	"radarr",
    metadata=kubernetes.meta.v1.ObjectMetaArgs(
        labels=radarr_labels,
        name="radarr",
        namespace=namespace,
    ),
	spec=kubernetes.apps.v1.DeploymentSpecArgs(
		replicas=1,
		selector=kubernetes.meta.v1.LabelSelectorArgs(
			match_labels=radarr_labels,
		),
		template=kubernetes.core.v1.PodTemplateSpecArgs(
			metadata=kubernetes.meta.v1.ObjectMetaArgs(
				labels=radarr_labels,
			),
			spec=kubernetes.core.v1.PodSpecArgs(
				containers=[kubernetes.core.v1.ContainerArgs(
					name="radarr",
					image="lscr.io/linuxserver/radarr",
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
                            #name="radarr_PublishedServerUrl",
						    #value="192.168.0.5" #optional
					    #),
                        kubernetes.core.v1.EnvVarArgs(						
                            name="TZ",
						    value="Europe/London",
					    )
                    ],
                    volume_mounts=[{
                        "mount_path": "/config",
                        "name": "radarr-conf-pvc",
                    }],
					ports=[kubernetes.core.v1.ContainerPortArgs(
						container_port=7878,
					)],
				)],
                volumes=[kubernetes.core.v1.VolumeArgs(
                    name="radarr-conf-pvc",
                    persistent_volume_claim={
                        "claim_name": "radarr-conf-pvc",
                    },
                )],
			),
		),
	))

radarr_service = kubernetes.core.v1.Service(
	"radarr",
	metadata=kubernetes.meta.v1.ObjectMetaArgs(
		name="radarr",
		labels=radarr_labels,
        namespace=namespace,
	),
	spec=kubernetes.core.v1.ServiceSpecArgs(
		type="ClusterIP",
		ports=[kubernetes.core.v1.ServicePortArgs(
			port=7878,
			#target_port=7878,
		)],
		selector=radarr_labels,
	))