from livekit.agents import WorkerOptions
import inspect

# Print all parameters of the WorkerOptions class
print(inspect.signature(WorkerOptions.__init__))

# Print the docstring if available
print(WorkerOptions.__init__.__doc__)

# Create an instance with max_concurrent_jobs and print its attributes
options = WorkerOptions(
    entrypoint_fnc=lambda x: None,
    agent_name="test",
    max_concurrent_jobs=10
)
print(vars(options))