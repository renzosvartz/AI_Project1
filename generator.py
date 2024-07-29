import random

for n in range(1, 31):
            
    with open(f"graph{n}.txt", "w") as file:
            
        #write size
        file.write(f"{10}\n")

        #write n x n matrix

        #for n rows, write n random numbers, diagonals

        for row in range(10):

            for col in range(10):

                if row == col:
                    file.write("0 ")
                    
                else:
                    file.write(f"{random.randint(10, 99)} ")

            if row != 10 - 1:
                file.write("\n")