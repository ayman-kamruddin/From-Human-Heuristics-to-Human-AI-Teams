#!/usr/bin/env python
"""
Setup validation script for From Human Heuristics to Human-AI Teams
Run this script after downloading the repository and data to verify everything is set up correctly.

Usage: python check_setup.py
"""

import os
import sys
from pathlib import Path

def check_python_version():
    """Check if Python version is 3.x"""
    print("Checking Python version...")
    version = sys.version_info
    if version.major >= 3:
        print(f"✓ Python {version.major}.{version.minor}.{version.micro} detected")
        return True
    else:
        print(f"✗ Python {version.major}.{version.minor} detected. Python 3.x required.")
        return False

def check_dependencies():
    """Check if required Python packages are installed"""
    print("\nChecking Python dependencies...")
    required_packages = [
        'numpy', 'pandas', 'matplotlib', 'scipy',
        'pingouin', 'fastdtw', 'similaritymeasures', 'tqdm'
    ]

    missing_packages = []
    for package in required_packages:
        try:
            __import__(package)
            print(f"✓ {package} is installed")
        except ImportError:
            print(f"✗ {package} is NOT installed")
            missing_packages.append(package)

    if missing_packages:
        print(f"\nMissing packages: {', '.join(missing_packages)}")
        print("Install with: pip install -r requirements.txt")
        return False
    return True

def check_data_folders():
    """Check if required data folders exist"""
    print("\nChecking data folders...")
    script_dir = Path(__file__).resolve().parent

    required_folders = [
        ('RAW_EXPERIMENT_DATA', 'Main data folder'),
        ('RAW_EXPERIMENT_DATA/TWO-HUMAN_HAs', 'Experiment 1 (Human-Human) data'),
        ('RAW_EXPERIMENT_DATA/HUMAN-AA_TEAM', 'Experiment 2 (Human-AA) data'),
        ('OtherResults', 'Results output folder'),
        ('OtherResults/AA-AA_SimulationData', 'Simulation data'),
    ]

    all_exist = True
    for folder, description in required_folders:
        folder_path = script_dir / folder
        if folder_path.exists():
            print(f"✓ {description}: {folder}")
        else:
            print(f"✗ {description}: {folder} NOT FOUND")
            all_exist = False

    if not all_exist:
        print("\nSome data folders are missing.")
        print("Download data from: https://data.mendeley.com/datasets/kpxp5zkh5f/2")
        print("Extract to the root directory of this project.")
        return False
    return True

def check_scripts_folder():
    """Check if Scripts folder and key files exist"""
    print("\nChecking Scripts folder...")
    script_dir = Path(__file__).resolve().parent
    scripts_dir = script_dir / 'Scripts'

    if not scripts_dir.exists():
        print("✗ Scripts folder NOT FOUND")
        return False

    print(f"✓ Scripts folder exists")

    # Check for tools subdirectory
    tools_dir = scripts_dir / 'tools'
    if tools_dir.exists():
        print(f"✓ Scripts/tools folder exists")
    else:
        print(f"✗ Scripts/tools folder NOT FOUND")
        return False

    return True

def check_output_permissions():
    """Check if we can create output directories"""
    print("\nChecking write permissions...")
    script_dir = Path(__file__).resolve().parent

    test_dirs = [
        script_dir / 'OtherResults' / 'test_write_permission'
    ]

    can_write = True
    for test_dir in test_dirs:
        try:
            test_dir.mkdir(parents=True, exist_ok=True)
            test_file = test_dir / 'test.txt'
            test_file.write_text('test')
            test_file.unlink()
            test_dir.rmdir()
            print(f"✓ Can write to output directories")
        except Exception as e:
            print(f"✗ Cannot write to {test_dir.parent}: {e}")
            can_write = False

    return can_write

def main():
    print("=" * 60)
    print("Setup Validation for Human Heuristics to Human-AI Teams")
    print("=" * 60)

    checks = [
        check_python_version(),
        check_dependencies(),
        check_data_folders(),
        check_scripts_folder(),
        check_output_permissions()
    ]

    print("\n" + "=" * 60)
    if all(checks):
        print("✓ ALL CHECKS PASSED - You're ready to run the analysis!")
        print("=" * 60)
        print("\nNext steps:")
        print("1. Navigate to the Scripts folder")
        print("2. See Scripts/README.md for analysis workflow")
        return 0
    else:
        print("✗ SOME CHECKS FAILED - Please fix the issues above")
        print("=" * 60)
        return 1

if __name__ == "__main__":
    sys.exit(main())
