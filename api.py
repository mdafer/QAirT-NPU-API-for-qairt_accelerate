# api.py
# FastAPI server for NPU-accelerated txt2img

import io
import threading
import base64
import sys
import os
from fastapi import FastAPI
from pydantic import BaseModel
from PIL import Image

from modules import shared
# from qairt_accelerate.accelerate import replace_model  # Not available

# Optional: allow dynamic model loading
from modules.sd_models import load_model

# Add qairt_accelerate to path for imports
extension_path = os.path.join(os.path.dirname(__file__), '..', 'qairt_accelerate')
sys.path.append(extension_path)

# Import QNN pipeline
from qairt_sd_pipeline import QnnStableDiffusionPipeline
from pipeline_utils import StableDiffusionInput
from pipeline_cache import PipelineCache

# ---------------------------
# Define request schema
# ---------------------------
class GenerationRequest(BaseModel):
    prompt: str
    negative_prompt: str = ""
    steps: int = 20
    width: int = 512
    height: int = 512
    cfg_scale: float = 7.5
    sampler: str = "DPM++ 3M SDE"  # default sampler
    seed: int = -1  # -1 for random
    model: str = "Stable-Diffusion-2.1"  # default model

# ---------------------------
# Initialize FastAPI
# ---------------------------
fastapi_app = FastAPI(title="NPU Accelerated SD API")

# ---------------------------
# Define txt2img endpoint
# ---------------------------
@fastapi_app.post("/txt2img")
def txt2img(req: GenerationRequest):
    try:
        # 1️⃣ Create QNN pipeline for the requested model
        print(f"[QAiRT NPU API] Creating pipeline for model: {req.model}")
        pipeline = QnnStableDiffusionPipeline(req.model)

        # 2️⃣ Handle seed
        if req.seed == -1:
            import random
            req.seed = random.randint(0, 2**32 - 1)
        print(f"[QAiRT NPU API] Using seed: {req.seed}")

        # 3️⃣ Create input for QNN pipeline
        sd_input = StableDiffusionInput(
            is_txt2img=True,
            prompt=req.prompt,
            un_prompt=req.negative_prompt,
            seed=req.seed,
            step=req.steps,
            text_guidance=req.cfg_scale,
            sampler_name=req.sampler,
            model_name=req.model,
        )

        # 4️⃣ Generate image using QNN
        def callback(result):
            pass  # No progress callback for API

        print("[QAiRT NPU API] Starting generation...")
        img = pipeline.model_execute(sd_input, callback, None)  # No upscaler
        print("[QAiRT NPU API] Generation completed")

        # 5️⃣ Convert to PNG bytes
        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)

        # 6️⃣ Encode to base64 for API response
        img_base64 = base64.b64encode(buffer.read()).decode("utf-8")

        return {"image": img_base64}
    except Exception as e:
        print(f"[QAiRT NPU API] Error: {str(e)}")
        return {"error": str(e)}

# ---------------------------
# Start API in a background thread
# ---------------------------
def start_api(demo=None, app=None):
    """
    Launch FastAPI server on port 7861 in a background thread.
    Works independently of WebUI API mode.
    """
    print("[QAiRT NPU API] Starting API server...")
    def run():
        try:
            import uvicorn
            print("[QAiRT NPU API] Uvicorn imported, starting server...")
            uvicorn.run(fastapi_app, host="0.0.0.0", port=7861)
        except Exception as e:
            print(f"[QAiRT NPU API] Error starting server: {e}")

    thread = threading.Thread(target=run)
    thread.daemon = True  # allows WebUI to exit cleanly
    thread.start()
    print("[QAiRT NPU API] Running at http://localhost:7861/txt2img")
