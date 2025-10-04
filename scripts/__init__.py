from modules import script_callbacks
import api

print("[QAiRT NPU API] scripts/__init__.py loaded")  # debug
# Start API after WebUI finishes loading
script_callbacks.on_app_started(api.start_api)