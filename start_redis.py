
import subprocess
import sys
import os

def start_redis():
    """Start Redis server for development"""
    try:
        # Check if Redis is already running
        result = subprocess.run(['redis-cli', 'ping'], capture_output=True, text=True)
        if result.returncode == 0:
            print("Redis is already running!")
            return
    except FileNotFoundError:
        print("Redis CLI not found. Installing Redis...")
        
    # Try to start Redis server
    try:
        print("Starting Redis server...")
        subprocess.Popen(['redis-server', '--daemonize', 'yes'])
        print("Redis server started successfully!")
    except FileNotFoundError:
        print("Redis server not found. Please install Redis:")
        print("Ubuntu/Debian: sudo apt-get install redis-server")
        print("macOS: brew install redis")
        print("Or use the in-memory channel layer for development")

if __name__ == "__main__":
    start_redis()
