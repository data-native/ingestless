from manager import __app_name__
from manager.cli import cli

def main():
    cli.app(prog_name=__app_name__)

if __name__ == "__main__":
    main()