import argparse
from .app import run_app

def main():
    parser = argparse.ArgumentParser(description="Country Picker GUI")
    parser.add_argument("--select", type=str, help="Pre-select country name")
    args = parser.parse_args()

    run_app(preselect_country=args.select or "")
#entrypoint 
if __name__ == "__main__":
    main()
