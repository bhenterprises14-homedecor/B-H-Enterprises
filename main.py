"""Development server runner for both FastAPI and Streamlit."""

import subprocess
import sys
import time
import os

if __name__ == "__main__":
    # Set environment
    os.environ["ENVIRONMENT"] = "development"
    os.environ["DEBUG"] = "True"
    
    print("Starting B H Enterprises Application...")
    print("-" * 50)
    
    # Start FastAPI server in background
    print("Starting FastAPI server on http://localhost:8000...")
    fastapi_process = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "src.app:app", "--reload", "--host", "0.0.0.0", "--port", "8000"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    
    # Wait for FastAPI to start
    time.sleep(3)
    
    # Start Streamlit
    print("Starting Streamlit frontend on http://localhost:8501...")
    streamlit_process = subprocess.Popen(
        [sys.executable, "-m", "streamlit", "run", "streamlit_app.py", "--logger.level=info"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    
    print("-" * 50)
    print("✅ Application started!")
    print("📊 Dashboard: http://localhost:8501")
    print("🔌 API: http://localhost:8000")
    print("📚 API Docs: http://localhost:8000/docs")
    print("-" * 50)
    
    try:
        # Keep processes running
        fastapi_process.wait()
        streamlit_process.wait()
    except KeyboardInterrupt:
        print("\nShutting down...")
        fastapi_process.terminate()
        streamlit_process.terminate()
        sys.exit(0)
