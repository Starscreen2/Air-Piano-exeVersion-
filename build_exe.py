#!/usr/bin/env python3
"""
Build script for Air-Piano executable
This script creates an executable (.exe) file from the Air-Piano Python application
"""

import os
import sys
import subprocess
import shutil

def main():
    print("🔨 Building Air-Piano Executable")
    print("=" * 50)
    
    # Check if PyInstaller is installed
    try:
        import PyInstaller
        print(f"✅ PyInstaller {PyInstaller.__version__} found")
    except ImportError:
        print("❌ PyInstaller not found. Installing...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print("✅ PyInstaller installed")
    
    # Clean previous builds
    if os.path.exists("build"):
        shutil.rmtree("build")
        print("🧹 Cleaned build directory")
    
    if os.path.exists("dist"):
        shutil.rmtree("dist")
        print("🧹 Cleaned dist directory")
      # Build command
    build_cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",                    # Create single executable
        "--windowed",                   # Hide console window
        "--name=Air-Piano",             # Name of executable
        "--icon=piano.ico",             # Icon (if exists)
        "--add-data=requirements.txt;.", # Include requirements
        "--hidden-import=cv2",          # Ensure OpenCV is included
        "--hidden-import=mediapipe",    # Ensure MediaPipe is included
        "--hidden-import=pygame",       # Ensure Pygame is included
        "--hidden-import=numpy",        # Ensure NumPy is included
        "--collect-all=mediapipe",      # Collect all MediaPipe files
        "--collect-all=cv2",            # Collect all OpenCV files
        "air_piano_main.py"
    ]
      # Remove icon parameter if icon doesn't exist
    if not os.path.exists("piano.ico"):
        # Remove both the --icon flag and its value
        if "--icon=piano.ico" in build_cmd:
            build_cmd.remove("--icon=piano.ico")
        print("⚠️ No icon file found, building without icon")
    
    print("🔧 Building executable...")
    print(f"Command: {' '.join(build_cmd)}")
    
    try:
        result = subprocess.run(build_cmd, check=True, capture_output=True, text=True)
        print("✅ Build completed successfully!")
        
        # Check if executable was created
        exe_path = os.path.join("dist", "Air-Piano.exe")
        if os.path.exists(exe_path):
            size_mb = os.path.getsize(exe_path) / (1024 * 1024)
            print(f"📦 Executable created: {exe_path}")
            print(f"📏 Size: {size_mb:.1f} MB")
            
            # Create a batch file for easy running
            batch_content = f"""@echo off
echo Starting Air-Piano...
echo Press 'q' in the camera window to quit
"{exe_path}"
pause
"""
            with open("Run-Air-Piano.bat", "w") as f:
                f.write(batch_content)
            print("✅ Created Run-Air-Piano.bat for easy launching")
            
        else:
            print("❌ Executable not found in dist folder")
    
    except subprocess.CalledProcessError as e:
        print(f"❌ Build failed: {e}")
        print("STDOUT:", e.stdout)
        print("STDERR:", e.stderr)
        return False
    
    print("\n🎹 Air-Piano Build Complete!")
    print("📁 Files created:")
    print("   - dist/Air-Piano.exe (main executable)")
    print("   - Run-Air-Piano.bat (launcher script)")
    print("\n💡 To run: Double-click Run-Air-Piano.bat or Air-Piano.exe")
    print("🎯 Make sure your camera is connected and working!")
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)
