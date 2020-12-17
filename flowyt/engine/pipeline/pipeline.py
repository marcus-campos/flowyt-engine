import copy
import json
import os
import time

from engine.settings import WORKSPACE_STORAGE_MODE
from engine.utils.asyncio_pool import AsyncioPool

from .context import Context
from .debug import PipelineDebug
from .flow import Flow
from .workspace import Workspace


class Pipeline:
    def __init__(self, workspace_data, flow):
        self.start_pipeline_time = time.time()
        self.flow = flow
        self.workspace_data = workspace_data
        self.workspace_class = Workspace(self.workspace_data["config"]["settings"])
        self.execution_error = False
        self.context = None

    def start(self, input_data=None, debug=False):
        # Config context
        pipeline_debug = True if self.workspace_class.debug and debug else False
        local_context = {}

        if WORKSPACE_STORAGE_MODE == "local":
            local_context = {"os": {"env": os.environ}}

        # Set context
        self.context = Context(
            public={
                "workspace_info": {
                    "id": self.workspace_class.id,
                    "name": self.workspace_class.name,
                    "debug": self.workspace_class.debug,
                    "release": self.workspace_class.release,
                    "safe_mode": self.workspace_class.safe_mode,
                },
                "env": self.workspace_class.env,
                "workspace": {},
                "input": input_data,
                "function": self.workspace_data["functions"],
                "response": {},
                **local_context,
            },
            private={
                "integrations": self.workspace_class.integrations,
                "development_language": self.workspace_class.development_language,
            },
            pipeline={
                "logs": PipelineDebug(),
                "debug": pipeline_debug,
                "self_class": self,
                "async_pool": AsyncioPool(),
            },
        )

        # Process
        result = self.process()
        logs = self.context.pipeline["logs"].get()

        return result, logs

    def process(self):
        # Get start process time
        start_time = time.time()

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
            self.context.pipeline["logs"].flow(
                flow_id=flow_class.id, flow_name=flow_class.name, flow_elapsed_time=(time.time() - start_time)
            )

            # Execute actions
            pipeline_actions = PipelineActions(current_flow, flow_class, self.context)
            pipeline_response = pipeline_actions.process(start_time)

            # Updates
            self.context = pipeline_actions.context
            process_pipeline = pipeline_actions.process_pipeline
            current_flow = pipeline_actions.current_flow
            self.execution_error = pipeline_actions.execution_error

            # Execute async pool
            self.context.pipeline["async_pool"].run()
            self.context.pipeline["logs"].append()

        self.context.pipeline["logs"].workspace(
            self.workspace_class.id, self.workspace_class.name, time.time() - start_time
        )

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
        self.safe_mode = context.public["workspace_info"]["safe_mode"]

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

            # Remove action response if exists
            self.clean_action_response()

            # Jump flow
            self.jump_flow()

            # Debug logs
            if self.context.pipeline["debug"]:
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
            action = self.actions.next_action(self.context.pipeline)

            if not action:
                response = self.context.pipeline.get("response")
                next_flow = self.context.pipeline.get("next_flow")

                if not response and not next_flow:
                    self.has_actions = False
                    self.process_pipeline = False

                return None

            # Execute action
            if action.execute_async:
                self.context.pipeline["async_pool"].add(action.action.start_async(self.context))
            else:
                self.context = action.action.start(self.context)
        except Exception as e:
            self.process_pipeline = False
            self.has_actions = False
            self.execution_error = True

            self.pipeline_response["exception"] = {
                "message": e.message if hasattr(e, "message") else str(e),
                "action": {"id": action.id, "name": action.action_name, "data": action.data},
            }
            
            if self.context.pipeline["debug"]:
                raise e
                    

        return action

    def contexted_action_vars(self):
        self.context.public["response"] = self.action_response

    def clean_action_response(self):
        # Remove action response if exists
        if self.action_response == self.context.public["response"]:
            self.action_response = {}
            self.context.public["response"] = {}
        else:
            self.action_response = self.context.public["response"]

    def debug_log(self, action, start_time):
        if not action:
            return

        try:
            data = copy.deepcopy(action.action.action_data)
        except:
            data = "<non-serializable: {0}>".format(type(action.action.action_data))

        # if self.context.pipeline["extra"]:
        #     if "extra_logs" in self.context.pipeline["extra"]:
        #         data = {**data, **self.context.pipeline["extra"]["extra_logs"]}

        self.context.pipeline["logs"].action(action.id, action.action_name, data, time.time() - start_time)

    def jump_flow(self):
        if self.context.pipeline.get("next_flow"):
            self.has_actions = False
            self.current_flow = self.context.pipeline.get("next_flow")

            # Clear context vars
            self.action_response = {}
            self.context.public.response = {}

    def stop_pipeline(self):
        # Stop pipeline if get response
        if self.context.pipeline.get("response"):
            self.process_pipeline = False
            self.has_actions = False
            self.pipeline_response = self.context.pipeline.get("response")
            return True

        if self.context.pipeline.get("end"):
            self.process_pipeline = False
            self.has_actions = False
            return True

        return False
