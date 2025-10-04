# QAirT NPU API Extension for Stable Diffusion WebUI

This extension enables NPU inference on Qualcomm processors using the QAirT API for Stable Diffusion WebUI, enabling faster image generation and processing.

Note: The qairt_accelerate extension is not supported in the official Stable Diffusion WebUI API. This extension provides a solution to enable NPU acceleration through the QAirT API.

## Features

- NPU-accelerated image generation
- Seamless integration with Stable Diffusion WebUI
- Optimized performance for supported hardware

## Installation

1. Ensure you have the Stable Diffusion WebUI installed and running.
2. Place this extension folder in the `extensions` directory of your Stable Diffusion WebUI installation.
3. Run the installation script:
   ```bash
   python install.py
   ```
4. Restart the Stable Diffusion WebUI.

## Requirements

- Python 3.8+
- Stable Diffusion WebUI
- Qualcomm processors with NPU support (check QAirT documentation for supported devices)
- qairt_accelerate extension (dependency)

## Usage

After installation, the extension will automatically be available in the WebUI.

### API Usage

The extension provides a REST API for programmatic image generation. The API server runs on port 7861.

Example curl command:

```bash
curl -X POST http://localhost:7861/txt2img \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "a beautiful landscape",
    "negative_prompt": "",
    "steps": 20,
    "width": 512,
    "height": 512,
    "cfg_scale": 7.5,
    "sampler": "DPM++ 3M SDE",
    "seed": -1,
    "model": "Stable-Diffusion-2.1"
  }'
```

## API

The extension provides an API interface through `api.py` for programmatic access to NPU-accelerated features.

## Scripts

- `scripts/qairt_npu_api.py`: Main extension script
- `install.py`: Installation and setup script

## Configuration

Edit `manifest.json` to configure extension parameters if needed.

## Troubleshooting

If you encounter issues:

1. Ensure all requirements are met
2. Check the WebUI logs for error messages
3. Verify NPU hardware compatibility
