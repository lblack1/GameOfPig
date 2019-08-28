'''
Lloyd Black
2295968
lblack@chapman.edu
CPSC 230-07
PigGameGUI.pyw

This program defines a GUI that allows for one or two player play of a game of Pig, and includes such features as keeping track of players' names,
playing little victory sounds upon victory, playing a sad trombone upon defeat, and a bunch of little popup windows for turn starts or victory or loss.
'''

import tkinter as tk
from tkinter import ttk
import random as ran
import PigGUIHelpers as PGH


class DiceBeforeSwineApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.iconbitmap(self, "Pig_Icon.ico")

        # Text/Image/Audio variable bank
        global title_image
        title_image = tk.PhotoImage(file = "Title_Image.png").subsample(2)
        global game_title
        game_title = tk.PhotoImage(file = "Title_Image.png").subsample(3)
        global roll_button_image
        roll_button_image = tk.PhotoImage(file = "Dice_button_picture.png").subsample(11)
        global rules_text
        rules_text = "The rules are simple: roll a six sided die, collect points, hold whenever you please.\nRoll a one, your points are cancelled and your turn ends.\nFirst to 100 points wins."
        global victory_fanfare
        victory_fanfare = "Victory_Fanfare.wav"
        global sad_trombone
        sad_trombone = "Sad_Trombone.wav"

        container = tk.Frame(self)
        container.pack(side = "top", fill = "both", expand = True)
        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)

        PGH.popAndLoc(self, 1000, 400) # This function's arguments are the window you wish to size/center, the width, and the height, respectively

        self.frames = {}

        for F in (IntroPage, SPNameEnter, SPGame, SPTieFrame, TPNameEnter, TPGame):

            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row = 0, column = 0, sticky = "nsew")

        self.show_frame(IntroPage)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()


class IntroPage(tk.Frame, DiceBeforeSwineApp):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        intro_title = tk.Label(self, image = title_image).pack(pady = 20)
        intro_choice = tk.Label(self, text = "Choose your game mode", font = "36").pack()

        single_player_button = tk.Button(self, text = "SINGLE PLAYER", cursor = "hand2", font = "20",
                        command = lambda: controller.show_frame(SPNameEnter))
        single_player_button.pack(pady = 5)

        two_player_button = tk.Button(self, text = "TWO PLAYER", cursor = "hand2", font = "20",
                        command = lambda: controller.show_frame(TPNameEnter))
        two_player_button.pack(pady = 5)

#Henceforth, SP = Single Player, TP = Two Player
class SPNameEnter(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        global player_name
        player_name = tk.StringVar()

        name_enter_lab = tk.Label(self, text = "Enter your name below", font = "Times 18", fg = "green")
        name_enter_lab.pack()

        name_entry = ttk.Entry(self, textvariable = player_name)
        name_entry.pack(pady = 25)

        def SP_game_start(event):
            global p_name
            p_name = player_name.get()

            if p_name == "":
                p_name = "Player"

            controller.show_frame(SPGame)

        name_entry.bind('<Return>', SP_game_start)

        def SP_game_start_butt():
            SP_game_start(event = '<Return>')

        cont_button = ttk.Button(self, text = "Continue", command = SP_game_start_butt)
        cont_button.pack()


class SPGame(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        intro_title = tk.Label(self, image = game_title).pack()
        rules_widg = tk.Label(self, text = rules_text, fg = "blue", font = "Times 14").pack()

        def begin():
            begin_button.destroy()
            game()
        begin_button = tk.Button(self, text = "BEGIN", font = "Times 18", cursor = "hand2", command = begin)
        begin_button.pack(pady = 7)

        def game():
            global p_score, c_score, round_no, p_name
            p_score, c_score, round_no = 0, 0, 1
            global score_widg
            score_widg = tk.Label(self, text = "{}: {}          Computer: {}\nRound {}".format(p_name, p_score, c_score, round_no), font = "Times 12", relief = tk.SUNKEN)
            score_widg.pack()

            def game_end():
                if p_score >= 100 and c_score >= 100:
                    controller.show_frame(SPTieFrame)

                elif p_score >= 100:
                    win_popup = tk.Toplevel()
                    win_popup.overrideredirect(1)
                    PGH.winCenter(win_popup)

                    win_lab = tk.Label(win_popup, text = "Congratulations!\nYou've won!\nHuzzah!\n*confetti*", fg = "green", font = "Impact 20").pack(side = tk.TOP)
                    global victory_fanfare
                    PGH.playAudioFile(victory_fanfare)

                    exit_button = tk.Button(win_popup, text = "Exit", font = "14", command = app.destroy).pack(side = tk.BOTTOM)

                elif c_score >= 100:
                    lose_popup = tk.Toplevel()
                    lose_popup.overrideredirect(1)
                    PGH.winCenter(lose_popup)

                    lose_lab = tk.Label(lose_popup, text = "Well, everyone faces defeat once in a while.\nBetter luck next time.", font = "Times 14", fg = "red").pack()
                    global sad_trombone
                    PGH.playAudioFile(sad_trombone)

                    def kill_everything():
                        lose_popup.destroy()
                        app.destroy()

                    exit_button = tk.Button(lose_popup, text = "Exit", font = "16", command = kill_everything).pack(pady = 10)


            def p_popup():

                if p_score >= 100 or c_score >= 100:
                    game_end()
                    return 0

                global p_pop
                p_pop = tk.Toplevel()
                p_pop.overrideredirect(1)
                PGH.winCenter(p_pop)

                lab = tk.Label(p_pop, text = "Your turn, {}!".format(p_name), font = "14").pack()

                def p_turn():

                    global p_pop
                    p_pop.destroy()

                    p_frame = tk.Frame(self)
                    p_frame.pack()
                    global turn_score, p_name
                    turn_score = ran.randint(1,6)
                    if turn_score == 1:
                        if p_name == "Kobayashi":
                            p_turn()
                        else:
                            p_frame.destroy()
                            bad_luck = tk.Toplevel()
                            bad_luck.overrideredirect(1)
                            PGH.winCenter(bad_luck)
                            BL_lab = tk.Label(bad_luck, text = "Oof, a one on your first roll.\nThat's a shame.", fg = "red").pack()
                            def bad_luck_end():
                                bad_luck.destroy()
                                c_turn()
                            BL_butt = ttk.Button(bad_luck, text = "Continue", cursor = "hand2", command = bad_luck_end).pack()
                            return 0 #return used to break out of function cleanly

                    turn_score_widg = tk.Label(p_frame, text = "Turn score: {}".format(turn_score), font = "14", fg = "green")
                    turn_score_widg.pack(pady = 12)
                    last_roll_disp = tk.Label(p_frame, text = "{}".format(turn_score), font = "Georgia 24", fg = "blue")
                    last_roll_disp.pack()

                    butt_frame = tk.Frame(p_frame)
                    butt_frame.pack(pady = 10)

                    def roll():
                        global turn_score, p_name
                        temp_roll = ran.randint(1,6)
                        last_roll_disp.config(text = "{}".format(temp_roll))

                        if temp_roll == 1:
                            if p_name == "Kobayashi":
                                roll()
                            else:
                                p_frame.destroy()
                                roll_one = tk.Toplevel()
                                roll_one.overrideredirect(1)
                                PGH.winCenter(roll_one)
                                RO_lab = tk.Label(roll_one, text = "You've rolled a one.\nEnd of turn.", fg = "red").pack()
                                def roll_one_end():
                                    roll_one.destroy()
                                    c_turn()
                                RO_butt = ttk.Button(roll_one, text = "Continue", cursor = "hand2", command = roll_one_end).pack()
                                return 0

                        elif temp_roll != 1:
                            turn_score += temp_roll
                            turn_score_widg.config(text = "Turn score: {}".format(turn_score))

                    roll_butt = tk.Button(butt_frame, image = roll_button_image, cursor = "hand2", command = roll)
                    roll_butt.grid(padx = 5)

                    def hold():
                        global p_score, c_score, round_no, turn_score, p_name
                        p_score += turn_score
                        p_frame.destroy()
                        score_widg.config(text = "{}: {}          Computer: {}\nRound {}".format(p_name, p_score, c_score, round_no))
                        c_turn()

                    hold_butt = tk.Button(butt_frame, text = "Hold", font = "18", cursor = "hand2", command = hold)
                    hold_butt.grid(row = 0, column = 1, padx = 5)



                butt = tk.Button(p_pop, text = "Begin", cursor = "hand2", command = p_turn).pack()



            def c_turn():

                c_pop = tk.Toplevel()
                c_pop.overrideredirect(1)
                PGH.winCenter(c_pop)


                lab = tk.Label(c_pop, text = "Computer's turn", font = "14").pack()
                c_pop.after(2500, c_pop.destroy)

                c_frame = tk.Frame(self)
                c_frame.pack()

                def c_roll_one_end():
                    c_roll_one = tk.Toplevel()
                    PGH.winCenter(c_roll_one)
                    c_roll_one.overrideredirect(1)

                    CRO_lab = tk.Label(c_roll_one, text = "Computer has\nrolled a one.", font = "14").pack()

                    def c_kill_func():
                        c_roll_one.destroy()
                        c_frame.destroy()
                        p_popup()

                    c_roll_one.after(2500, c_kill_func)

                    global round_no, p_name
                    round_no += 1

                    score_widg.config(text = "{}: {}          Computer: {}\nRound {}".format(p_name, p_score, c_score, round_no))


                def c_roll():
                    global c_turn_score
                    c_temp_roll = ran.randint(1,6)

                    if c_temp_roll == 1:
                        c_roll_one_end()
                        return 0

                    elif c_temp_roll != 1:
                        c_last_roll_disp.config(text = "{}".format(c_temp_roll))
                        c_turn_score += c_temp_roll
                        c_turn_score_widg.config(text = "Turn score: {}".format(c_turn_score))

                        if c_turn_score < 20:
                            c_frame.after(1500, c_roll)

                        elif c_turn_score >= 20:
                            def c_hold():
                                global p_score, c_score, round_no, turn_score, p_name
                                c_score += c_turn_score
                                c_frame.destroy()
                                round_no += 1
                                score_widg.config(text = "{}: {}          Computer: {}\nRound {}".format(p_name, p_score, c_score, round_no))
                                p_popup()

                            c_frame.after(2000, c_hold)

                global c_turn_score
                c_turn_score = 0
                c_frame.after(2500, c_roll)

                c_turn_score_widg = tk.Label(c_frame, text = "Turn score: {}".format(c_turn_score), font = "14", fg = "green")
                c_turn_score_widg.pack(pady = 12)
                c_last_roll_disp = tk.Label(c_frame, text = "{}".format(c_turn_score), font = "Georgia 24", fg = "blue")
                c_last_roll_disp.pack()




            p_popup()



class SPTieFrame(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        tie_lab = tk.Label(self, text = "A Tie! Prepare to engage in tie-breaking Rock, Paper, Scissors!", font = "Times 24")
        tie_lab.pack()

        def rock_paper_scissors():
            tie_lab.destroy()

            RPS_lab = tk.Label(self, text = "At your leisure.", font = "Times 20")
            RPS_lab.pack(pady = 15)

            p_choice = 0  # 1 = rock, 2 = paper, 3 = scissors

            def after_button():
                global p_choice, c_choice

                def p_victory():
                    win_popup = tk.Toplevel()
                    win_popup.overrideredirect(1)
                    PGH.winCenter(win_popup)

                    win_lab = tk.Label(win_popup, text = "Congratulations!\nYou've won!\nHuzzah!\n*confetti*", fg = "green", font = "Impact 20").pack(side = tk.TOP)
                    global victory_fanfare
                    PGH.playAudioFile(victory_fanfare)

                    def kill_everything_w():
                        win_popup.destroy()
                        app.destroy()

                    exit_button = tk.Button(win_popup, text = "Exit", font = "14", command = kill_everything_w).pack(side = tk.BOTTOM)

                def p_loss():
                    lose_popup = tk.Toplevel()
                    lose_popup.overrideredirect(1)
                    PGH.winCenter(lose_popup)

                    lose_lab = tk.Label(lose_popup, text = "Well, everyone faces defeat once in a while.\nBetter luck next time.", font = "Times 14", fg = "red").pack()
                    global sad_trombone
                    PGH.playAudioFile(sad_trombone)

                    def kill_everything_l():
                        lose_popup.destroy()
                        app.destroy()

                    exit_button = tk.Button(lose_popup, text = "Exit", font = "16", command = kill_everything_l).pack(pady = 10)

                if p_choice == c_choice:
                    rock_button.destroy()
                    paper_button.destroy()
                    scissors_button.destroy()

                    def tooManyGodDamnFunctions():
                        another_tie_lab = tk.Label(self, text = "Another tie. Another round is required.", font = "Times 24")
                        another_tie_lab.pack(pady = 15)
                        def likeSeriously():
                            another_tie_lab.destroy()
                            RPS_lab.destroy()
                            rock_paper_scissors()

                        self.after(3000, likeSeriously)

                    if p_choice == 1:
                        RPS_lab.config(text = "Comp: Rock!", fg = "red")
                        self.after(2000, tooManyGodDamnFunctions)

                    elif p_choice == 2:
                        RPS_lab.config(text = "Comp: Paper!", fg = "red")
                        self.after(2000, tooManyGodDamnFunctions)

                    elif p_choice == 3:
                        RPS_lab.config(text = "Comp: Scissors!", fg = "red")
                        self.after(2000, tooManyGodDamnFunctions)

                elif p_choice == 1:
                    if c_choice == 2:
                        RPS_lab.config(text = "Comp: Paper!", fg = "red")
                        self.after(900, p_loss)
                    elif c_choice == 3:
                        RPS_lab.config(text = "Comp: Scissors!", fg = "red")
                        self.after(900, p_victory)

                elif p_choice == 2:
                    if c_choice == 3:
                        RPS_lab.config(text = "Comp: Scissors!", fg = "red")
                        self.after(900, p_loss)
                    elif c_choice == 1:
                        RPS_lab.config(text = "Comp: Rock!", fg = "red")
                        self.after(900, p_victory)

                elif p_choice == 3:
                    if c_choice == 1:
                        RPS_lab.config(text = "Comp: Rock!", fg = "red")
                        self.after(900, p_loss)
                    elif c_choice == 2:
                        RPS_lab.config(text = "Comp: Paper!", fg = "red")
                        self.after(900, p_victory)

            def choose_rock():
                global p_choice, c_choice
                p_choice = 1
                c_choice = ran.randint(1,3)
                after_button()

            rock_button = tk.Button(self, text = "Rock!", font = "18", command = choose_rock)
            rock_button.pack(pady = 10)

            def choose_paper():
                global p_choice, c_choice
                p_choice = 2
                c_choice = ran.randint(1,3)
                after_button()

            paper_button = tk.Button(self, text = "Paper!", font = "18", command = choose_paper)
            paper_button.pack(pady = 10)

            def choose_scissors():
                global p_choice, c_choice
                p_choice = 3
                c_choice = ran.randint(1,3)
                after_button()

            scissors_button = tk.Button(self, text = "Scissors!", font = "18", command = choose_scissors)
            scissors_button.pack(pady = 10)

        self.after(9000, rock_paper_scissors)



class TPNameEnter(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        global player1_name, player2_name
        player1_name = tk.StringVar()
        player2_name = tk.StringVar()

        name_enter_lab = tk.Label(self, text = "Enter your names below", font = "Times 18", fg = "green")
        name_enter_lab.pack()

        p1_name_frame = tk.Frame(self)
        p1_name_frame.pack(pady = 25)
        name1_lab = tk.Label(p1_name_frame, text = "Player 1", font = "Times 16").pack(pady = 10)
        name1_entry = ttk.Entry(p1_name_frame, textvariable = player1_name)
        name1_entry.pack()

        p2_name_frame = tk.Frame(self)
        p2_name_frame.pack(pady = 25)
        name2_lab = tk.Label(p2_name_frame, text = "Player 2", font = "Times 16").pack(pady = 10)
        name2_entry = ttk.Entry(p2_name_frame, textvariable = player2_name)
        name2_entry.pack()

        def TP_game_start(event):
            global p1_name, p2_name
            p1_name = player1_name.get()
            p2_name = player2_name.get()

            if p1_name == "":
                p1_name = "Player 1"

            if p2_name == "":
                p2_name = "Player 2"

            controller.show_frame(TPGame)

        name1_entry.bind('<Return>', TP_game_start)
        name2_entry.bind('<Return>', TP_game_start)

        def TP_game_start_butt():
            TP_game_start(event = '<Return>')

        cont_button = ttk.Button(self, text = "Continue", command = TP_game_start_butt)
        cont_button.pack()



class TPGame(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        intro_title = tk.Label(self, image = game_title).pack()
        rules_widg = tk.Label(self, text = rules_text, fg = "blue", font = "Times 14").pack()

        def begin():
            begin_button.destroy()
            game()
        begin_button = tk.Button(self, text = "BEGIN", font = "Times 18", cursor = "hand2", command = begin)
        begin_button.pack(pady = 7)

        def game():
            global p1_score, p2_score, round_no, p1_name, p2_name
            p1_score, p2_score, round_no = 0, 0, 1
            global score_widg
            score_widg = tk.Label(self, text = "{}: {}          {}: {}\nRound {}".format(p1_name, p1_score, p2_name, p2_score, round_no), font = "Times 12", relief = tk.SUNKEN)
            score_widg.pack()

            def game_end():
                global p1_name, p2_name

                if p1_score >= 100 and p2_score >= 100:
                    TP_tie_popup = tk.Toplevel()
                    TP_tie_popup.overrideredirect(1)
                    PGH.winCenter(TP_tie_popup)

                    tie_lab = tk.Label(TP_tie_popup, text = "Well, you tied.\nI'll let you duke\nit out yourselves.", font = "Times 16").pack(side = tk.TOP)

                    def kill_everything_tie():
                        TP_tie_popup.destroy()
                        app.destroy()

                    exit_button = tk.Button(TP_tie_popup, text = "Exit", font = "14", command = kill_everything_tie).pack(side = tk.BOTTOM)


                elif p1_score >= 100:
                    win_popup = tk.Toplevel()
                    win_popup.overrideredirect(1)
                    PGH.winCenter(win_popup)

                    win_lab = tk.Label(win_popup, text = "Congratulations,\n{}!\nYou've won!\n*confetti*".format(p1_name), fg = "green", font = "Impact 20").pack(side = tk.TOP)
                    global victory_fanfare
                    PGH.playAudioFile(victory_fanfare)

                    def kill_everything_p1():
                        win_popup.destroy()
                        app.destroy()

                    exit_button = tk.Button(win_popup, text = "Exit", font = "14", command = kill_everything_p1).pack(side = tk.BOTTOM)

                elif p2_score >= 100:
                    win_popup = tk.Toplevel()
                    win_popup.overrideredirect(1)
                    PGH.winCenter(win_popup)

                    win_lab = tk.Label(win_popup, text = "Congratulations,\n{}!\nYou've won!\n*confetti*".format(p2_name), fg = "red", font = "Impact 20").pack(side = tk.TOP)
                    PGH.playAudioFile(victory_fanfare)

                    def kill_everything_p2():
                        win_popup.destroy()
                        app.destroy()

                    exit_button = tk.Button(win_popup, text = "Exit", font = "14", command = kill_everything_p2).pack(side = tk.BOTTOM)


            def p1_popup():

                if p1_score >= 100 or p2_score >= 100:
                    game_end()
                    return 0

                global p1_pop
                p1_pop = tk.Toplevel()
                p1_pop.overrideredirect(1)
                PGH.winCenter(p1_pop)

                global p1_name
                lab = tk.Label(p1_pop, text = "Your turn, {}!".format(p1_name), font = "14").pack()

                def p1_turn():

                    global p1_pop, p1_name
                    p1_pop.destroy()

                    p1_frame = tk.Frame(self)
                    p1_frame.pack()
                    global p1_turn_score
                    p1_turn_score = ran.randint(1,6)

                    if p1_turn_score == 1:
                        if p1_name == "Kobayashi":
                            p1_turn()
                        else:
                            p1_frame.destroy()
                            bad_luck = tk.Toplevel()
                            bad_luck.overrideredirect(1)
                            bad_luck()
                            PGH.winCenter(bad_luck)
                            BL_lab = tk.Label(bad_luck, text = "Oof, a one on your first roll.\nThat's a shame, {}.".format(p1_name)).pack()
                            def bad_luck_end():
                                bad_luck.destroy()
                                p2_popup()
                            BL_butt = ttk.Button(bad_luck, text = "Continue", cursor = "hand2", command = bad_luck_end).pack()
                            return 0 #return used to break out of function cleanly

                    p1_turn_score_widg = tk.Label(p1_frame, text = "Turn score: {}".format(p1_turn_score), font = "14", fg = "green")
                    p1_turn_score_widg.pack(pady = 12)
                    last_roll_disp = tk.Label(p1_frame, text = "{}".format(p1_turn_score), font = "Georgia 24", fg = "blue")
                    last_roll_disp.pack()

                    butt_frame = tk.Frame(p1_frame)
                    butt_frame.pack(pady = 10)

                    def roll():
                        global p1_turn_score, p1_name
                        temp_roll = ran.randint(1,6)
                        last_roll_disp.config(text = "{}".format(temp_roll))

                        if temp_roll == 1:
                            if p2_name == "Kobayashi":
                                roll()
                            else:
                                p1_frame.destroy()
                                roll_one = tk.Toplevel()
                                roll_one.overrideredirect(1)
                                PGH.winCenter(roll_one)
                                RO_lab = tk.Label(roll_one, text = "You've rolled a one.\nEnd of turn.", fg = "red").pack()
                                def roll_one_end():
                                    roll_one.destroy()
                                    p2_popup()
                                RO_butt = ttk.Button(roll_one, text = "Continue", cursor = "hand2", command = roll_one_end).pack()
                                return 0

                        elif temp_roll != 1:
                            p1_turn_score += temp_roll
                            p1_turn_score_widg.config(text = "Turn score: {}".format(p1_turn_score))

                    roll_butt = tk.Button(butt_frame, image = roll_button_image, cursor = "hand2", command = roll)
                    roll_butt.grid(padx = 5)

                    def hold():
                        global p1_score, p2_score, round_no, p1_turn_score, p1_name, p2_name
                        p1_score += p1_turn_score
                        p1_frame.destroy()
                        score_widg.config(text = "{}: {}          {}: {}\nRound {}".format(p1_name, p1_score, p2_name, p2_score, round_no))
                        p2_popup()

                    hold_butt = tk.Button(butt_frame, text = "Hold", font = "18", cursor = "hand2", command = hold)
                    hold_butt.grid(row = 0, column = 1, padx = 5)



                butt = tk.Button(p1_pop, text = "Begin", cursor = "hand2", command = p1_turn).pack()



            def p2_popup():

                global p2_pop
                p2_pop = tk.Toplevel()
                p2_pop.overrideredirect(1)
                PGH.winCenter(p2_pop)

                global p2_name
                lab = tk.Label(p2_pop, text = "Your turn, {}!".format(p2_name), font = "14").pack()

                def p2_turn():

                    global p2_pop, p2_name
                    p2_pop.destroy()

                    p2_frame = tk.Frame(self)
                    p2_frame.pack()
                    global p2_turn_score
                    p2_turn_score = ran.randint(1,6)
                    if p2_turn_score == 1:
                        if p2_name == "Kobayashi":
                            p2_turn()
                        else:
                            p2_frame.destroy()
                            bad_luck = tk.Toplevel()
                            bad_luck.overrideredirect(1)
                            PGH.winCenter(bad_luck)
                            BL_lab = tk.Label(bad_luck, text = "Oof, a one on your first roll.\nThat's a shame, {}.".format(p2_name)).pack()
                            def bad_luck_end():
                                bad_luck.destroy()
                                global round_no, p1_name, p2_name
                                round_no += 1
                                score_widg.config(text = "{}: {}          {}: {}\nRound {}".format(p1_name, p1_score, p2_name, p2_score, round_no))
                                p1_popup()
                            BL_butt = ttk.Button(bad_luck, text = "Continue", cursor = "hand2", command = bad_luck_end).pack()
                            return 0 #return used to break out of function cleanly

                    p2_turn_score_widg = tk.Label(p2_frame, text = "Turn score: {}".format(p2_turn_score), font = "14", fg = "red")
                    p2_turn_score_widg.pack(pady = 12)
                    last_roll_disp = tk.Label(p2_frame, text = "{}".format(p2_turn_score), font = "Georgia 24", fg = "purple")
                    last_roll_disp.pack()

                    butt_frame = tk.Frame(p2_frame)
                    butt_frame.pack(pady = 10)

                    def roll():
                        global p2_turn_score, p2_name
                        temp_roll = ran.randint(1,6)
                        last_roll_disp.config(text = "{}".format(temp_roll))

                        if temp_roll == 1:
                            if p2_name == "Kobayashi":
                                roll()
                            else:
                                p2_frame.destroy()
                                roll_one = tk.Toplevel()
                                roll_one.overrideredirect(1)
                                PGH.winCenter(roll_one)
                                RO_lab = tk.Label(roll_one, text = "You've rolled a one.\nEnd of turn.", fg = "red").pack()
                                def roll_one_end():
                                    roll_one.destroy()
                                    global round_no, p1_name, p2_name
                                    round_no += 1
                                    score_widg.config(text = "{}: {}          {}: {}\nRound {}".format(p1_name, p1_score, p2_name, p2_score, round_no))
                                    p1_popup()
                                RO_butt = ttk.Button(roll_one, text = "Continue", cursor = "hand2", command = roll_one_end).pack()
                                return 0

                        elif temp_roll != 1:
                            p2_turn_score += temp_roll
                            p2_turn_score_widg.config(text = "Turn score: {}".format(p2_turn_score))

                    roll_butt = tk.Button(butt_frame, image = roll_button_image, cursor = "hand2", command = roll)
                    roll_butt.grid(padx = 5)

                    def hold():
                        global p1_score, p2_score, round_no, p2_turn_score, p1_name, p2_name
                        p2_score += p2_turn_score
                        p2_frame.destroy()
                        round_no += 1
                        score_widg.config(text = "{}: {}          {}: {}\nRound {}".format(p1_name, p1_score, p2_name, p2_score, round_no))
                        p1_popup()

                    hold_butt = tk.Button(butt_frame, text = "Hold", font = "18", cursor = "hand2", command = hold)
                    hold_butt.grid(row = 0, column = 1, padx = 5)



                butt = tk.Button(p2_pop, text = "Begin", cursor = "hand2", command = p2_turn).pack()




            p1_popup()



app = DiceBeforeSwineApp()
app.title("Dice Before Swine")
app.mainloop()
