import os
import sys

# append parent path so we have access to the app
# when this file is run as a script from within
# this directory
parent_dir = os.path.abspath(os.path.join(os.getcwd(), "."))
sys.path.append(parent_dir)


if __name__ == '__main__':
    from src.database import seed_database
    seed_database()
