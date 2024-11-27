## Run Instructions
1. Install pip if not already installed
2. Run: pip install .
    - Sometimes this might give this error: externally-managed-environment
    - To circumvent this we can create a virtual env and run it. Here are the steps to do that:
      - Install venv
      - python3 -m venv <location-to-your-venv>
      - source .<location-to-your-venv>/bin/activate
      - From the root of this project run: python3 -m pip install .
3. This should install pyls in our venv and to run it simply run: pyls [optional arguments]


## Usage
This project simulates the ls unix command.  Here are a few examples on how to run it after installation:
1. pyls: should output the file and directory names
2. pyls -A: should also output the hidden files starting with a dot
3. plys -l: should print a verbose format
4. similarly there are other options like -r for reversed, -h for human readable format of sizes, -t for sort based on timestamp, and so on.  We can also mix these arguments.


## TODO
- Check and implement if the arguments should be case-insensitive
- Create 2 classes: FileFilterer and OutputFormatter and put the filter and print logic inside those files.
- Include pytest
- Move the hardcoded strings to a constants.py file