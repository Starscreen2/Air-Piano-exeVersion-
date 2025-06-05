"""
Quick Build Script for Air-Piano Executable
Run this to create a standalone .exe file
"""

import subprocess
import sys
import os

def quick_build():
    print("🚀 Quick Build: Air-Piano Executable")
    print("=" * 40)
      # Simple one-line build command
    cmd = [
        sys.executable, "-m", "PyInstaller", 
        "--onefile", 
        "--windowed",
        "--name=Air-Piano",
        "--distpath=./",  # Put exe in current directory
        "air_piano_main.py"
    ]
    
    print("Building executable...")
    try:
        result = subprocess.run(cmd, check=True)
        print("✅ Build successful!")
        print("📦 Air-Piano.exe created in current directory")
        print("🎹 Double-click Air-Piano.exe to run!")
        
        # Clean up build files
        import shutil
        if os.path.exists("build"):
            shutil.rmtree("build")
        if os.path.exists("Air-Piano.spec"):
            os.remove("Air-Piano.spec")
        print("🧹 Cleaned up temporary files")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Build failed: {e}")
        return False
    
    return True

if __name__ == "__main__":
    quick_build()
