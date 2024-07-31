import random

for size in range(5, 155, 5):
            
    for num in range(1, 31):

        #write n x n matrix
        matrix = [[0] * size for _ in range(size)]
        
        for row in range(size):
            for col in range(row + 1, size):
                weight = random.randint(10, 99)
                matrix[row][col] = weight
                matrix[col][row] = weight

        #for n rows, write n random numbers, diagonals

        with open(f"graph_size{size}_{num}.txt", "w") as file:
            file.write(f"{size}\n")
            for row in range(size):
                file.write(" ".join(map(str, matrix[row])))
                if row != size - 1:
                    file.write("\n")