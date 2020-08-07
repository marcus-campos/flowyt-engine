import copy
import json
import os
import time

from dotmap import DotMap
from engine.debug import PipelineDebug
from engine.flow import Flow
from engine.workspace import Workspace

from .settings import WORKSPACE_STORAGE_MODE


class Pipeline:
    def __init__(self, workspace_data, flow):
        self.start_pipeline_time = time.time()
        self.flow = flow
        self.workspace_data = workspace_data
        self.workspace_class = Workspace(self.workspace_data["config"]["settings"])
        self.execution_error = False

    def start(self, request_data={}, input_data=None):
        # Get start workspace process time
        start_time = time.time()

        # Config context
        incoming_debug = request_data.get("debug") == "true" or input_data.get("debug") == "true"
        pipeline_debug = True if self.workspace_class.debug and incoming_debug else False
        local_context = {}


        if WORKSPACE_STORAGE_MODE == "local":
            local_context = {
                "os": {
                    "env": os.environ
                }
            }

        context = {
            "public": {
                "workspace_info": {
                    "id": self.workspace_class.id,
                    "name": self.workspace_class.name,
                    "debug": self.workspace_class.debug,
                    "release": self.workspace_class.release,
                    "safe_mode": self.workspace_class.safe_mode,
                },
                "env": self.workspace_class.env,
                "workspace": {},
                "request": request_data,
                "input": input_data,
                "function": self.workspace_data["functions"],
                "response": {},
                **local_context
            },
            "private": {
                "integrations": self.workspace_class.integrations,
                "development_language": self.workspace_class.development_language,
            },
            "pipeline_context": {"logs": PipelineDebug(), "debug": pipeline_debug, "self_class": self},
        }

        context["pipeline_context"]["logs"].workspace(
            self.workspace_class.id, self.workspace_class.name, time.time() - start_time
        )

        result = self.process(context)
        result["__debug__"] = context["pipeline_context"]["logs"].get()

        return result

    def process(self, context):
        # Current flow
        current_flow = self.flow
        pipeline_response = {}

        # While proccess vars
        process_pipeline = True
        while process_pipeline:
            # Get start flow process time
            start_time = time.time()

            # Load flow
            flow_class = Flow(self.workspace_data, current_flow)

            # Debug logs
            context["pipeline_context"]["logs"].flow(
                flow_id=flow_class.id, flow_name=flow_class.name, flow_elapsed_time=(time.time() - start_time)
            )

            # Execute actions
            pipeline_actions = PipelineActions(current_flow, flow_class, context)
            pipeline_response = pipeline_actions.process(start_time)

            # Updates
            context = pipeline_actions.context
            process_pipeline = pipeline_actions.process_pipeline
            current_flow = pipeline_actions.current_flow
            self.execution_error = pipeline_actions.execution_error

            context["pipeline_context"]["logs"].append()

        return pipeline_response


class PipelineActions:
    def __init__(self, current_flow, flow_class, context):
        # Update on finish
        self.context = context
        self.process_pipeline = True
        self.current_flow = current_flow
        self.execution_error = False
        # Not update on finish
        self.flow_class = flow_class
        self.actions = flow_class.pipeline
        self.has_actions = True
        self.action_response = {}
        self.pipeline_response = {}
        self.safe_mode = context["public"]["workspace_info"]["safe_mode"]

    def process(self, start_at):
        while self.has_actions:
            # Safe check
            if self.safe_mode["enable"]:
                self.safe_check(start_at)

            # Get start action process time
            start_time = time.time()

            # Contexted action vars
            self.contexted_action_vars()

            # Execute action
            action = self.execute_action()

            # Add flow vars
            self.flow_class.vars = self.context.public.flow

            # Remove action response if exists
            self.clean_action_response()

            # Jump flow
            self.jump_flow()

            # Debug logs
            if self.context.pipeline_context.debug:
                self.debug_log(action, start_time)

            # Stop pipeline
            self.stop_pipeline()

        return self.pipeline_response

    def safe_check(self, start_at):
        current_time = time.time()
        safe_time = self.safe_mode["safe_time"]
        need_abort = (current_time - start_at) >= safe_time

        if need_abort:
            self.pipeline_response["exception"] = {
                "message": "This flow took a long time to run and was aborted. The limit is {0} seconds and the flow took {1} seconds.".format(
                    safe_time, (current_time - start_at)
                )
            }
            self.process_pipeline = False
            self.has_actions = False
            self.execution_error = True

    def execute_action(self):
        action = None

        try:
            # Get next action
            action = self.actions.next_action(self.context.pipeline_context)

            if not action:
                response = self.context.pipeline_context.get("response")
                next_flow = self.context.pipeline_context.get("next_flow")

                if not response and not next_flow:
                    self.has_actions = False
                    self.process_pipeline = False

                return None

            # Execute action
            self.context = action.action.start(self.context)
        except Exception as e:
            self.process_pipeline = False
            self.has_actions = False
            self.execution_error = True

            if hasattr(e, "message"):
                self.pipeline_response = {"status": 500, "exception": {}}

                if self.context.pipeline_context.debug:
                    self.pipeline_response["exception"] = {
                        "message": e.message,
                        "action": {"id": action.id, "name": action.action_name, "data": action.data},
                    }
            else:
                self.pipeline_response = {"status": 500, "exception": {}}
                if self.context.pipeline_context.debug:
                    self.pipeline_response["exception"] = {
                        "message": str(e),
                        "action": {"id": action.id, "name": action.action_name, "data": action.data},
                    }

        return action

    def contexted_action_vars(self):
        self.context["public"]["flow"] = self.flow_class.vars
        self.context["public"]["response"] = self.action_response
        self.context = DotMap(self.context)

    def clean_action_response(self):
        # Remove action response if exists
        if self.action_response == self.context.public.response:
            self.action_response = {}
            self.context.public.response = {}
        else:
            self.action_response = self.context.public.response

    def debug_log(self, action, start_time):
        if not action:
            return

        self.context["pipeline_context"]["logs"].action(
            action.id, action.action_name, copy.deepcopy(action.data), time.time() - start_time
        )

    def jump_flow(self):
        if self.context.pipeline_context.get("next_flow"):
            self.has_actions = False
            self.current_flow = self.context.pipeline_context.get("next_flow")

            # Clear context vars
            self.action_response = {}
            self.context.public.response = {}

    def stop_pipeline(self):
        # Stop pipeline if get response
        if self.context.pipeline_context.get("response"):
            self.process_pipeline = False
            self.has_actions = False
            self.pipeline_response = self.context.pipeline_context.get("response")
            return True

        if self.context.pipeline_context.get("end"):
            self.process_pipeline = False
            self.has_actions = False
            return True

        return False
