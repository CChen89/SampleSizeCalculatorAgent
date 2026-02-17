#!/usr/bin/env python3
"""
Startup script for the Chainlit Sample Size Calculator App
Handles installation and launching of the web application
"""

import subprocess
import sys
import os
from pathlib import Path


def check_and_install_chainlit():
    """Check if chainlit is installed, install if not"""
    try:
        import chainlit

        print("✅ Chainlit is already installed")
        return True
    except ImportError:
        print("🔄 Chainlit not found. Installing...")
        try:
            # Use conda to install chainlit
            subprocess.check_call(
                ["conda", "install", "-c", "conda-forge", "chainlit", "-y"],
                env=os.environ,
            )
            print("✅ Chainlit installed successfully via conda")
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            try:
                # Fallback to pip install
                subprocess.check_call(
                    [sys.executable, "-m", "pip", "install", "chainlit"]
                )
                print("✅ Chainlit installed successfully via pip")
                return True
            except subprocess.CalledProcessError as e:
                print(f"❌ Failed to install chainlit: {e}")
                return False


def check_environment():
    """Check if the environment is properly set up"""
    print("🔍 Checking environment...")

    # Check if we're in the right directory
    current_dir = Path.cwd()
    required_files = ["SampleSizeMultiAgent.py", "chainlit_sample_size_app.py", ".env"]

    missing_files = []
    for file in required_files:
        if not (current_dir / file).exists():
            missing_files.append(file)

    if missing_files:
        print(f"❌ Missing required files: {', '.join(missing_files)}")
        print(f"   Please run this script from the RAG directory")
        return False

    # Check environment variables
    try:
        from dotenv import load_dotenv

        load_dotenv()

        required_env = ["ILIAD_API_KEY", "ILIAD_URL_BASE"]
        missing_env = []

        for env_var in required_env:
            if not os.getenv(env_var):
                missing_env.append(env_var)

        if missing_env:
            print(f"⚠️ Missing environment variables: {', '.join(missing_env)}")
            print("   App will still work but with limited functionality")
        else:
            print("✅ Environment variables configured")

    except ImportError:
        print("⚠️ python-dotenv not found, skipping environment check")

    return True


def check_r_server():
    """Check if R MCP server is running"""
    try:
        import requests

        response = requests.get("http://127.0.0.1:9291", timeout=2)
        print("✅ R MCP server is running (full functionality)")
        return True
    except:
        print("⚠️ R MCP server not detected (fallback mode will be used)")
        return False


def launch_chainlit_app():
    """Launch the chainlit application"""
    print("🚀 Launching Chainlit Sample Size Calculator...")
    print("📍 The app will be available at: http://localhost:8000")
    print("🔄 Starting server...")

    try:
        # Change to the directory containing the app
        os.chdir(Path(__file__).parent)

        # Launch chainlit
        subprocess.run(
            [
                "chainlit",
                "run",
                "chainlit_sample_size_app.py",
                "--host",
                "0.0.0.0",
                "--port",
                "8000",
            ]
        )

    except KeyboardInterrupt:
        print("\n🛑 Application stopped by user")
    except Exception as e:
        print(f"❌ Failed to start application: {e}")


def main():
    """Main startup function"""
    print("🧮 Clinical Trial Sample Size Calculator - Chainlit App")
    print("=" * 60)

    # Check and install chainlit
    if not check_and_install_chainlit():
        print("❌ Cannot proceed without chainlit. Please install manually:")
        print("   conda install -c conda-forge chainlit")
        print("   or")
        print("   pip install chainlit")
        return

    # Check environment setup
    if not check_environment():
        print("❌ Environment check failed. Please fix the issues above.")
        return

    # Check R server (optional)
    check_r_server()

    # Launch the app
    print("\n🎯 All systems ready!")
    print("🌐 Starting web application...")

    launch_chainlit_app()


if __name__ == "__main__":
    main()
