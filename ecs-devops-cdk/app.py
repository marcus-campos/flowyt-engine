#!/usr/bin/env python3

from aws_cdk import core

from ecs_devops_cdk.ecs_devops_cdk_stack import EcsDevopsEngineCdkStack


app = core.App()
EcsDevopsEngineCdkStack(app, "ecs-devops-cdk")

app.synth()
