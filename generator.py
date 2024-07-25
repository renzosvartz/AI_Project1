import random

for n in range(5, 155, 5):
            
    with open(f"graph{(int) (n/5)}.txt", "w") as file:
            
        #write size
        file.write(f"{n}\n")

        #write n x n matrix

        #for n rows, write n random numbers, diagonals

        for row in range(n):

            for col in range(n):

                if row == col:
                    file.write("0 ")
                    
                else:
                    file.write(f"{random.randint(10, 99)} ")

            if row != n - 1:
                file.write("\n")