// Copyright 2016-2018, Pulumi Corporation.  All rights reserved.

import * as k8s from "@pulumi/kubernetes";
import * as pulumi from "@pulumi/pulumi";

// Minikube does not implement services of type `LoadBalancer`; require the user to specify if we're
// running on minikube, and if so, create only services of type ClusterIP.
const config = new pulumi.Config();
const isMinikube = config.getBoolean("isMinikube");

//
// REDIS LEADER.
//

const jackettLabels = { app: "jackett" };
const jackettDeployment = new k8s.apps.v1.Deployment("jackett", {
    spec: {
        selector: { matchLabels: jackettLabels },
        template: {
            metadata: { labels: jackettLabels },
            spec: {
                containers: [
                    {
                        name: "jackett",
                        image: "lscr.io/linuxserver/jackett",
                        resources: { requests: { cpu: "100m", memory: "100Mi" } },
                        ports: [{ containerPort: 9117 }],
                    },
                ],
            },
        },
    },
});
const jackettService = new k8s.core.v1.Service("jackett", {
    metadata: {
        name: "jackett",
        labels: jackettDeployment.metadata.labels,
    },
    spec: {
        ports: [{ port: 6379, targetPort: 6379 }],
        selector: jackettDeployment.spec.template.metadata.labels,
    },
});

const jackettIngress = new k8s.apiextensions.CustomResource(`jackett-ingress-route`, {
    apiVersion: 'traefik.containo.us/v1alpha1',
    kind: 'IngressRoute',
    metadata: {
        //namespace: args.namespace
        labels: jackettDeployment.metadata.labels,
    },
    spec: {
        entryPoints: ['websecure'],
        routes: [{
            match: `PathPrefix(\`"jackett"\`)`,
            kind: 'Rule',
            middlewares: [
                // {name: trailingSlashMiddleware.metadata.name},
                // {name: stripPrefixMiddleware.metadata.name},
            ],
            services: [{
                name: pulumi.output(args.service).metadata.name,
                //port: pulumi.output(args.service).spec.ports[0].port,
            }],
        }]
    },
});

// new k8s.apiextensions.CustomResource(`${name}-ingress-route`, {
//     apiVersion: 'traefik.containo.us/v1alpha1',
//     kind: 'IngressRoute',
//     metadata: {namespace: args.namespace},
//     spec: {
//         entryPoints: ['web'],
//         routes: [{
//             match: `PathPrefix(\`${args.prefix}\`)`,
//             kind: 'Rule',
//             middlewares: [
//                 // {name: trailingSlashMiddleware.metadata.name},
//                 // {name: stripPrefixMiddleware.metadata.name},
//             ],
//             services: [{
//                 name: pulumi.output(args.service).metadata.name,
//                 port: pulumi.output(args.service).spec.ports[0].port,
//             }],
//         }]
//     },
// }, {provider: opts?.provider,});