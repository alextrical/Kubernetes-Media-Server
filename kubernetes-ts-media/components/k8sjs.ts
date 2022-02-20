// Copyright 2016-2019, Pulumi Corporation.  All rights reserved.

import * as k8s from "@pulumi/kubernetes";
import * as k8stypes from "@pulumi/kubernetes/types/input";
import * as pulumi from "@pulumi/pulumi";

/**
 * ServiceDeployment is an example abstraction that uses a class to fold together the common pattern of a
 * Kubernetes Deployment and its associated Service object.
 */
export class ServiceDeployment extends pulumi.ComponentResource {
    public readonly deployment: k8s.apps.v1.Deployment;
    public readonly service: k8s.core.v1.Service;
    public readonly customResource: k8s.apiextensions.CustomResource;
    public readonly ipAddress?: pulumi.Output<string>;
    public readonly namespace?: string;

    constructor(name: string, args: ServiceDeploymentArgs, opts?: pulumi.ComponentResourceOptions) {
        super("k8sjs:service:ServiceDeployment", name, {}, opts);

        const labels = { app: name };
        const container: k8stypes.core.v1.Container = {
            name,
            image: args.image,
            resources: args.resources || { requests: { cpu: "100m", memory: "100Mi" } },
            env: [args.env || { name: "GET_HOSTS_FROM", value: "dns" },{name: "PGID", value: "1000"},{name: "PUID", value: "1000"},{name: "TZ", value: "Europe/London"},],
            ports: args.ports && args.ports.map(p => ({ containerPort: p })),
            //namespace: args.namespace,
        };
        this.deployment = new k8s.apps.v1.Deployment(name, {
            spec: {
                selector: { matchLabels: labels },
                replicas: args.replicas || 1,
                template: {
                    metadata: { 
                        labels: labels, 
                        namespace: args.namespace },
                    spec: { containers: [ container ] },
                },
            },
        }, { parent: this });

        this.service = new k8s.core.v1.Service(name, {
            metadata: {
                name: name,
                labels: this.deployment.metadata.labels,
                namespace: args.namespace,
            },
            spec: {
                ports: args.ports && args.ports.map(p => ({ port: p, targetPort: p })),
                selector: this.deployment.spec.template.metadata.labels,
                // Minikube does not implement services of type `LoadBalancer`; require the user to specify if we're
                // running on minikube, and if so, create only services of type ClusterIP.
                //type: args.allocateIpAddress ? (args.isMinikube ? "ClusterIP" : "LoadBalancer") : undefined,
            },
        }, { parent: this });
        



        // this.customResource = new k8s.apiextensions.CustomResource(name, {
        //     apiVersion: 'traefik.containo.us/v1alpha1',
        //     kind: 'IngressRoute',
        //     metadata: {
        //         name: name,
        //         labels: this.deployment.metadata.labels,
        //         namespace: args.namespace,
        //     },
        //     spec: {
        //         entryPoints: ['websecure'],
        //         routes: [{
        //             match: `PathPrefix(\``+name+`\`)`,
        //             kind: 'Rule',
        //             middlewares: [
        //                 // {name: trailingSlashMiddleware.metadata.name},
        //                 // {name: stripPrefixMiddleware.metadata.name},
        //             ],
        //             services: [{
        //                 //name: pulumi.output(args.service).metadata.name,
        //                 //port: pulumi.output(args.service).spec.ports[0].port,
        //                 name: name,
        //                 port: args.ports,
        //             }],
        //         }]
        //     },
        // }, { parent: this });





        // if (args.allocateIpAddress) {
        //     this.ipAddress = args.isMinikube ?
        //         this.service.spec.clusterIP :
        //         this.service.status.loadBalancer.ingress[0].ip;
        // }
    }
}

export interface ServiceDeploymentArgs {
    image: string;
    resources?: k8stypes.core.v1.ResourceRequirements;
    env?: k8stypes.core.v1.EnvVar;
    replicas?: number;
    ports?: number[];
    //allocateIpAddress?: boolean;
    //isMinikube?: boolean;

    namespace?: string;
    //prefix?: pulumi.Input<string>;
    //service?: pulumi.Input<k8s.core.v1.Service>;
}
