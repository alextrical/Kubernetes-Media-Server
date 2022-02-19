import pulumi
import pulumi_kubernetes as kubernetes

domain_name = "test.example.com"

application_data =	[
					["application","port",	"namespace"	],
					["transmission",9091,	"media"		],
					["jackett",		9117,	"media"		],
					["jellyfin",	8096,	"media"		],
					["lidarr",		8686,	"media"		],
					["ombi",		3579,	"media"		],
					["overseerr",	5055,	"media"		],
					["radarr",		7878,	"media"		],
					["sonarr",		8989,	"media"		]]


							#kubernetes.core.v1.EnvVarArgs(name="JELLYFIN_PublishedServerUrl",value="192.168.0.5"),



for row in application_data[1:]:        # iterate through application_data, skipping the header row

		# ----------namespace----------
	media_namespace = kubernetes.core.v1.Namespace("media-Namespace",
		api_version="v1",
		kind="Namespace",
		metadata=kubernetes.meta.v1.ObjectMetaArgs(
			name=namespace,
		))

	# ----------application----------
	application = row[0]
	port = row[1]
	namespace = row[2]

	application_config_persistent_volume_claim = kubernetes.core.v1.PersistentVolumeClaim(application+"-conf-pvc",
		api_version="v1",
		kind="PersistentVolumeClaim",
		metadata=kubernetes.meta.v1.ObjectMetaArgs(
			labels={"app": application},
			name=application+"-conf-pvc",
			namespace=namespace,
		),
		spec=kubernetes.core.v1.PersistentVolumeClaimSpecArgs(
			access_modes=["ReadWriteOnce"],
			#storage_class_name="longhorn",
			resources=kubernetes.core.v1.ResourceRequirementsArgs(
				requests={
					"storage": "1Gi",
				},
			),
		))
	
	application_deployment = kubernetes.apps.v1.Deployment(
		application,
		metadata=kubernetes.meta.v1.ObjectMetaArgs(
			labels={"app": application},
			name=application,
			namespace=namespace,
		),
		spec=kubernetes.apps.v1.DeploymentSpecArgs(
			replicas=1,
			selector=kubernetes.meta.v1.LabelSelectorArgs(
				match_labels={"app": application},
			),
			template=kubernetes.core.v1.PodTemplateSpecArgs(
				metadata=kubernetes.meta.v1.ObjectMetaArgs(
					labels={"app": application},
				),
				spec=kubernetes.core.v1.PodSpecArgs(
					containers=[kubernetes.core.v1.ContainerArgs(
						name=application,
						image="lscr.io/linuxserver/"+application,
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
							kubernetes.core.v1.EnvVarArgs(
								name="TZ",
								value="Europe/London",
							),
							
						],
						volume_mounts=[{
							"mount_path": "/config",
							"name": application+"-conf-pvc",
						}],
						ports=[kubernetes.core.v1.ContainerPortArgs(
							container_port=port,
						)],
					)],
					volumes=[kubernetes.core.v1.VolumeArgs(
						name=application+"-conf-pvc",
						persistent_volume_claim={
							"claim_name": application+"-conf-pvc",
						},
					)],
				),
			),
		))
	
	application_service = kubernetes.core.v1.Service(
		application,
		metadata=kubernetes.meta.v1.ObjectMetaArgs(
			name=application,
			labels={"app": application},
			namespace=namespace,
		),
		spec=kubernetes.core.v1.ServiceSpecArgs(
			type="ClusterIP",
			ports=[kubernetes.core.v1.ServicePortArgs(
				port=port,
			)],
			selector={"app": application},
		))