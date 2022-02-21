// Copyright 2016-2019, Pulumi Corporation.  All rights reserved.

import * as pulumi from "@pulumi/pulumi";
import * as k8sjs from "./k8sjs";
import * as k8s from "@pulumi/kubernetes";

const config = new pulumi.Config();
const name_space = "media";

// Create a Kubernetes Namespace
const ns = new k8s.core.v1.Namespace(name_space, {}, {});

// Export the Namespace name
export const namespaceName = ns.metadata.name;

const emby = new k8sjs.ServiceDeployment("emby", {
    image: "lscr.io/linuxserver/emby",
    ports: [8096],
    resources: { requests: { cpu: "100m", memory: "100Mi" }, limits: { cpu: "500m", memory: "500Mi" } },
    // env:{ name: "PUID", value: "1000" },  //Need to figure out how to get this to work with more than 1 arg
    // namespace: "media",
});

// const sonarr = new k8sjs.ServiceDeployment("sonarr", {
//     image: "lscr.io/linuxserver/sonarr",
//     ports: [8989],
//     namespace: "media",
// });

// const jackett = new k8sjs.ServiceDeployment("jackett", {
//     image: "lscr.io/linuxserver/jackett",
//     ports: [9117],
//     namespace: "media",
// });

// const radarr = new k8sjs.ServiceDeployment("radarr", {
//     image: "lscr.io/linuxserver/radarr",
//     ports: [7878],
//     namespace: "media",
// });

// const ombi = new k8sjs.ServiceDeployment("ombi", {
//     image: "lscr.io/linuxserver/ombi",
//     ports: [3579],
//     namespace: "media",
// });

// const transmission = new k8sjs.ServiceDeployment("transmission", {
//     image: "lscr.io/linuxserver/transmission",
//     ports: [9091],
//     namespace: "media",
// });

// const jellyfin  = new k8sjs.ServiceDeployment("jellyfin", {
//     image: "lscr.io/linuxserver/jellyfin",
//     ports: [8096],
//     namespace: "media",
// });

// const lidarr  = new k8sjs.ServiceDeployment("lidarr", {
//     image: "lscr.io/linuxserver/lidarr",
//     ports: [8686],
//     namespace: "media",
// });

// const overseerr  = new k8sjs.ServiceDeployment("overseerr", {
//     image: "lscr.io/linuxserver/overseerr",
//     ports: [5055],
//     namespace: "media",
// });

// const organizr  = new k8sjs.ServiceDeployment("organizr", {
//     image: "organizr/organizr",
//     ports: [80],
//     namespace: "media",
// });

// const radarr = new k8sjs.ServiceDeployment("radarr", {
//     //replicas: 1,
//     image: "lscr.io/linuxserver/radarr",
//     ports: [7878],
//     //allocateIpAddress: true,
//     //isMinikube: true, //config.getBoolean("isMinikube"),
// });

//export let frontendIp = frontend.ipAddress;
