'''
Lloyd Black
2295968
lblack@chapman.edu
CPSC 230-07
PigGameCLI.py

This program defines a few functions that allow for a game of Pig to be played then consolidates them in a main playPig function.
'''

import random as ran
import time as ti

def p_turn():
    print("\tYour turn!")
    ti.sleep(.5)
    turn_score = ran.randint(1,6)
    if turn_score == 1:
        print("\tOof. Your first roll was a 1. The dice gods have gazed disfavorably upon you this day.\n\n")
        return 0
    else:
        print("\tYour first roll was a {}.".format(turn_score))
        ti.sleep(1.2)
    again = input("\tWould you like to roll or hold? (enter 'r' or 'h')\n\t\t").lower()
    while again == "r":
        temp_roll = ran.randint(1,6)
        if temp_roll == 1:
            print("\n\tOop, rolled a 1. Sucks to be you.\n\n")
            return 0
        else:
            print("\n\tYou've just rolled a {}.".format(temp_roll))
            ti.sleep(1.2)
            turn_score += temp_roll
            print("\tYour total so far for this turn is {}.".format(turn_score))
            ti.sleep(1.3)
            again = input("\tWould you like to roll once more or hold? ('r' or 'h')\n\t\t").lower()
    else:
        return turn_score

def c_turn():
    print("\n\n\tMy turn!")
    ti.sleep(1)
    turn_score = ran.randint(1,6)
    if turn_score == 1:
        print("\tWell, I didn't make it one roll without rolling a 1.")
        return 0
    else:
        print("\tMy first roll was a {}.".format(turn_score))
        ti.sleep(1.2)
    while turn_score < 20:
        print("\tThat seems a bit low. I'm gonna roll again.\n")
        ti.sleep(1.6)
        temp_roll = ran.randint(1,6)
        if temp_roll == 1:
            print("\tWell drat, that's a 1.")
            return 0
        else:
            turn_score += temp_roll
            print("\tI've just rolled a {} which puts me at a turn total of {}.".format(temp_roll,turn_score))
            ti.sleep(1.2)
    else:
        mad_lad = ran.randint(1,100)
        if mad_lad == 100:
            ti.sleep(1.2)
            print("\tSo the assignment that describes how I'm meant to function says I'm meant to just hold when my score is 20 or more.\n")
            ti.sleep(3)
            print("\tBUT GO BIG OR GO HOME #YOLO\n")
            mad_roll = ran.randint(1,6)
            if mad_roll == 1:
                ti.sleep(1.3)
                print("\t...\n")
                ti.sleep(1)
                print("\t...\n")
                ti.sleep(1)
                print("\t...\n")
                ti.sleep(2)
                print("\tWell that was a 1. Whoopsie-doodles. Your turn.")
                return 0
            else:
                turn_score += mad_roll
                ti.sleep(1)
                print("\tMagnificent, I just rolled a {} putting my total at {}.".format(mad_roll,turn_score))
                ti.sleep(1)
                print("\tAlright, enough madness. I'm gonna hold now.")
                return turn_score
        else:
            ti.sleep(1)
            print("\tI'm satisfied with a {}. I'm gonna hold.".format(turn_score))
            return turn_score

def RPS():
    print("Ro...")
    ti.sleep(1)
    print("Sham...")
    ti.sleep(1)
    print("Bo!\n")

    player = input().title()

    x = ["Rock", "Paper", "Scissors"]
    comp = ran.choice(x)
    print("{}!".format(comp))
    while True:
        if comp == player:
            print("A tie! We must go again!")
            ti.sleep(1.5)
            print()
            print("Ro...")
            ti.sleep(1)
            print("Sham...")
            ti.sleep(1)
            print("Bo!\n")
            player = input().title()
            comp = ran.choice(x)
            print("{}!".format(comp))
        elif comp == "Rock":
            if player == "Scissors":
                return False #Note: For the sake of determining outcome, win by player = True and loss by player = False
            else:
                return True
        elif comp == "Scissors":
            if player == "Paper":
                return False
            else:
                return True
        elif comp == "Paper":
            if player == "Rock":
                return False
            else:
                return True

def playPig():
    p_score = 0
    c_score = 0
    print("The rules are simple: roll a six sided die, collect points, hold whenever you please.\nRoll a one, your points are cancelled and your turn ends.\nFirst to 100 points wins.\n\n")
    ti.sleep(3)
    while True:
        p_score += p_turn()
        c_score += c_turn()
        print("\nThe results of the round are as follows:")
        if p_score > c_score:
            print("You are in the lead with {} points, while I trail with {}.\n".format(p_score, c_score))
        elif p_score < c_score:
            print("I am in the lead with {} points, while you are behind with a paltry {} points.\n".format(c_score, p_score))
        elif p_score == c_score:
            print("We are dead even at {} points! What a contest!\n".format(p_score))
            if p_score == 0:
                print("Man, we suck.\n")
        ti.sleep(2.5)
        if p_score >= 100 and c_score >= 100:
            print("Well, it seems that we have both won. Let's call it an amicable draw and go our separate way as friends.\n")
            ti.sleep(4)
            print("PSYCH! I SHALL NEVER ACCEPT A TIE. I CHALLENGE YOU TO ROCK, PAPER, SCISSORS!\n")
            ti.sleep(2)
            tiebreak = RPS()
            if tiebreak == True:
                c_score = 0
            elif tiebreak == False:
                p_score = 0
        if p_score >= 100:
            print("Well, I suppose that means I must cede you the victory. Well fought, opponent.")
            ti.sleep(3)
            break
        elif c_score >= 100:
            print("Haha! I claim victory! Still, you were a worthy adversary. Well fought.")
            ti.sleep(3)
            break
        else:
            pass
    else:
        pass
