#import pulumi
import pulumi_kubernetes as kubernetes

namespace = "media"

#----------namespace----------
media_namespace = kubernetes.core.v1.Namespace("media-Namespace",
    api_version="v1",
    kind="Namespace",
    metadata=kubernetes.meta.v1.ObjectMetaArgs(
        name=namespace,
    ))

#----------jellyfin----------
jellyfin_labels = {"app": "jellyfin"}
jellyfin_config_persistent_volume_claim = kubernetes.core.v1.PersistentVolumeClaim("jellyfin-conf-pvc",
    api_version="v1",
    kind="PersistentVolumeClaim",
    metadata=kubernetes.meta.v1.ObjectMetaArgs(
        labels=jellyfin_labels,
        name="jellyfin-conf-pvc",
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

jellyfin = kubernetes.apps.v1.Deployment(
	"jellyfin",
    metadata=kubernetes.meta.v1.ObjectMetaArgs(
        labels=jellyfin_labels,
        name="jellyfin",
        namespace=namespace,
    ),
	spec=kubernetes.apps.v1.DeploymentSpecArgs(
		replicas=1,
		selector=kubernetes.meta.v1.LabelSelectorArgs(
			match_labels=jellyfin_labels,
		),
		template=kubernetes.core.v1.PodTemplateSpecArgs(
			metadata=kubernetes.meta.v1.ObjectMetaArgs(
				labels=jellyfin_labels,
			),
			spec=kubernetes.core.v1.PodSpecArgs(
				containers=[kubernetes.core.v1.ContainerArgs(
					name="jellyfin",
					image="lscr.io/linuxserver/jellyfin",
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
                            #name="JELLYFIN_PublishedServerUrl",
						    #value="192.168.0.5" #optional
					    #),
                        kubernetes.core.v1.EnvVarArgs(						
                            name="TZ",
						    value="Europe/London",
					    )
                    ],
                    volume_mounts=[{
                        "mount_path": "/config",
                        "name": "jellyfin-conf-pvc",
                    }],
					ports=[kubernetes.core.v1.ContainerPortArgs(
						container_port=8096,
					)],
				)],
                volumes=[kubernetes.core.v1.VolumeArgs(
                    name="jellyfin-conf-pvc",
                    persistent_volume_claim={
                        "claim_name": "jellyfin-conf-pvc",
                    },
                )],
			),
		),
	))

jellyfin_service = kubernetes.core.v1.Service(
	"jellyfin",
	metadata=kubernetes.meta.v1.ObjectMetaArgs(
		name="jellyfin",
		labels=jellyfin_labels,
        namespace=namespace,
	),
	spec=kubernetes.core.v1.ServiceSpecArgs(
		type="ClusterIP",
		ports=[kubernetes.core.v1.ServicePortArgs(
			port=8096,
			#target_port=8096,
		)],
		selector=jellyfin_labels,
	))