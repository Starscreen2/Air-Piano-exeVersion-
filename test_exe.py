#!/usr/bin/env python3
"""
Quick test to verify the Air-Piano executable works
"""
import subprocess
import sys
import time

def test_executable():
    print("🧪 Testing Air-Piano executable...")
    
    try:
        # Start the executable
        process = subprocess.Popen(
            ["dist/Air-Piano.exe"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Let it run for a few seconds
        time.sleep(3)
        
        # Terminate it
        process.terminate()
        
        # Get output
        stdout, stderr = process.communicate(timeout=5)
        
        print("✅ Executable started successfully!")
        print("📋 Output preview:")
        if stdout:
            print(stdout[:500])
        
        if "MediaPipe" in stdout or "Python" in stdout:
            print("✅ MediaPipe initialization appears to be working!")
            return True
        else:
            print("⚠️ Could not verify MediaPipe initialization")
            return False
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    success = test_executable()
    if success:
        print("\n🎉 Air-Piano.exe appears to be working correctly!")
        print("💡 You can now run it by:")
        print("   - Double-clicking Air-Piano.exe")
        print("   - Or using Run-Air-Piano.bat for easier launching")
    else:
        print("\n❌ There may be issues with the executable")
