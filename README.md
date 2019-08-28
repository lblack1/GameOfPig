# GameOfPig

Lloyd Black
2295968
lblack@chapman.edu
CPSC 230-07
Game of Pig

1. Source Files - Main Files - PigGameCLI.py, PigGameGUI.pyw
	PigGameGUI.pyw ancillary files - Dice_button_picture.png, Pig_Icon.ico, PigGUIHelpers.py, Sad_Trombone.wav, Title_Image.png, Victory_Fanfare.wav

2. Issues -
	CLI -- no major issues
	GUI -- Gathering player names, hiding a console upon app start, figuring out delays in widget creation, positioning/formatting, Key binding in entry widgets, lots of wonky installation of modules/libraries, lots of minor "didn't destroy a widget" here and "missed a function invocation" here
	All resolved through globalizing variables, defining new procedures, redefining as a .pyw instead of .py other various solutions

3. Resources - youtube.com/user/sentdex, StackOverflow in mass,

4. Description of Program -
	PigGameCLI.py - This program defines a few functions that allow for a game of Pig to be played then consolidates them in a main playPig function.

	PigGameGUI.pyw - This program defines a GUI that allows for one or two player play of a game of Pig, and includes such features as keeping track of players' names,
		playing little victory sounds upon victory, playing a sad trombone upon defeat, and a bunch of little popup windows for turn starts or victory or loss.

5. Functions/Procedures -
	PigGameCLI.py - p_turn(): no parameters, allows player to roll until they hold or roll a one, returns appropriate turn score.
		c_turn(): no parameters, auto rolls until one or total > 20, returns appropriate turn score
		RPS(): defines a tie_breaker for if both c and p get above 100 on the same turn
		playPig(): consolidates other procedures and provides inter-round updates on scores, defines end game.

	PigGUIHelpers.py - popAndLoc(window, width, height): parameters window = tk.Tk() or tk.Toplevel() variable you wish to size/center, width = width of window, height = height of window
		winCenter(window): parameter window = tk.Tk() or tk.Toplevel() variable you want centered
		playAudioFile(audioFile): Parameter audioFile = name of audio file wav form you wish to be played in string form.

	PigGameGUI.pyw - Too many to count

6. Required Packages - tkinter, random, pyaudio, wave
