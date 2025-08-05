#!/usr/bin/env python3
"""
Python Cache Cleanup Utility
============================

This script cleans up all __pycache__ directories and .pyc files
from the project to ensure fresh imports after code modifications.

Usage:
    python cleanup_pycache.py

Features:
- Removes all __pycache__ directories recursively  
- Removes individual .pyc files
- Safe error handling for locked files
- Verbose output showing what was cleaned
"""

import os
import shutil
import sys
from pathlib import Path


def cleanup_pycache(root_dir="."):
    """
    Clean up all Python cache files and directories.
    
    Args:
        root_dir (str): Root directory to start cleanup from
    """
    root_path = Path(root_dir).resolve()
    cleaned_dirs = []
    cleaned_files = []
    errors = []
    
    print(f"🧹 Starting Python cache cleanup in: {root_path}")
    print("-" * 50)
    
    # Remove __pycache__ directories
    for pycache_dir in root_path.rglob("__pycache__"):
        try:
            shutil.rmtree(pycache_dir)
            cleaned_dirs.append(str(pycache_dir))
            print(f"✅ Removed directory: {pycache_dir}")
        except Exception as e:
            errors.append(f"❌ Failed to remove {pycache_dir}: {e}")
            print(f"❌ Failed to remove {pycache_dir}: {e}")
    
    # Remove individual .pyc files
    for pyc_file in root_path.rglob("*.pyc"):
        try:
            pyc_file.unlink()
            cleaned_files.append(str(pyc_file))
            print(f"✅ Removed file: {pyc_file}")
        except Exception as e:
            errors.append(f"❌ Failed to remove {pyc_file}: {e}")
            print(f"❌ Failed to remove {pyc_file}: {e}")
    
    # Summary
    print("\n" + "=" * 50)
    print("🎯 CLEANUP SUMMARY")
    print("=" * 50)
    print(f"📁 Directories removed: {len(cleaned_dirs)}")
    print(f"📄 Files removed: {len(cleaned_files)}")
    print(f"⚠️  Errors: {len(errors)}")
    
    if errors:
        print("\n🚨 ERRORS ENCOUNTERED:")
        for error in errors:
            print(f"   {error}")
    
    if cleaned_dirs or cleaned_files:
        print("\n✨ Cache cleanup completed successfully!")
        print("💡 You can now restart your Python application.")
    else:
        print("\n🔍 No cache files found to clean.")
    
    return len(cleaned_dirs) + len(cleaned_files), len(errors)


if __name__ == "__main__":
    try:
        # Get the directory where this script is located
        script_dir = Path(__file__).parent
        
        # Cleanup from the project root
        cleaned_count, error_count = cleanup_pycache(script_dir)
        
        # Exit with appropriate code
        sys.exit(0 if error_count == 0 else 1)
        
    except KeyboardInterrupt:
        print("\n\n⏹️  Cleanup interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n💥 Unexpected error: {e}")
        sys.exit(1)
