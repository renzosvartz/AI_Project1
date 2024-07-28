import os
import re
import subprocess
import glob

input_files = glob.glob("Graphs/Local Search Algorithms/graph*.txt")

def extract_number(filename):
    
    base_name = os.path.basename(filename)
    
    match = re.search(r'(\d+)', base_name)

    return int(match.group(1)) if match else 0

input_files = sorted(input_files, key=extract_number)

for input_file in input_files:

    with open(input_file, 'r') as file:

        process = subprocess.Popen(['python', 'Local Search Algorithms/genetic.py'], stdin=file, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        stdout, stderr = process.communicate()

        print(f"Running with {input_file}")
        print(f"Output:\n{stdout.decode()}")

        if stderr:
            print(f"Errors:\n{stderr.decode()}")