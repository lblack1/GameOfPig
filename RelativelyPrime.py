'''
Lloyd Black
2295968
lblack@chapman.edu
CPSC 230-07
RelativelyPrime.py

This program prompts the user for two integers and then defines a functions using the inputted integers as parameters to determine whether or not
they are relatively prime.
'''

int1 = int(input("Enter an integer\n\t"))
int2 = int(input("Enter a second integer\n\t"))

def relPrime(a, b):
    if a < b:
        for test_factor in range(2, a + 1):
            if a % test_factor == 0 and b % test_factor == 0:
                return False    # returning False means they are not relatively prime, while True means they are
            else:
                pass
        return True
    elif a > b:
        for test_factor in range(2, b + 1):
            if a % test_factor == 0 and b % test_factor == 0:
                return False
            else:
                pass
        return True
    elif a == b:
        print("Well see you've just entered the same number twice, of course they're not relatively prime.")
        return False

print(relPrime(int1,int2))
