import launch

if not launch.is_installed("fastapi"):
    launch.run_pip("install fastapi", "fastapi")
if not launch.is_installed("uvicorn"):
    launch.run_pip("install uvicorn[standard]", "uvicorn")
if not launch.is_installed("pydantic"):
    launch.run_pip("install pydantic", "pydantic")