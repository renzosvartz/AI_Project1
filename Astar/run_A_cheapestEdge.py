import os
import re
import subprocess
import glob

for size in range(5, 155, 5):

    input_files = glob.glob(f"Graphs/Astar/graph_size{size}_*.txt")

    def extract_number(filename):
        
        base_name = os.path.basename(filename)
        
        match = re.search(r'_(\d+)', base_name)

        return int(match.group(1)) if match else 0

    input_files = sorted(input_files, key=extract_number)

    for input_file in input_files:

        with open(input_file, 'r') as file:

            process = subprocess.Popen(['python', 'Astar/A_cheapestEdge.py'], stdin=file, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            stdout, stderr = process.communicate()

            print(f"Running with {input_file}")
            print(f"Output:\n{stdout.decode()}")

            if stderr:
                print(f"Errors:\n{stderr.decode()}")