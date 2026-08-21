import argparse
import subprocess
import sys

def main():
    parser = argparse.ArgumentParser(
        description=""
    )
    
    #parser.add_value = parser.add_argument(
    #    "-- script"
    #)
    
    args = parser.parse_args()
    
    if args.__sizeof__ == 0:
        res = subprocess.run(
            [sys.executable, "process-metro-data"],
            capture_output=True,
            text=True
        )
        
        print(res)

if __name__ == '__main__':
    main()