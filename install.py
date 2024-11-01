import subprocess
import sys

def install(package):
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])

def main():
    packages = [
        'requests',
        'aiohttp',
        'colorama'
    ]
    
    for package in packages:
        install(package)

if __name__ == "__main__":
    main()
