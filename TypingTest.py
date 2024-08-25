#this is a WPM typing test
#first import these 

#curses is what allows you to style the terminal so like adding colors
import curses 
#this will let us initilaize the curses module and it will take over the terminal 
#once we finish with the module terminal will rmeove to normal
from curses import wrapper

#this is for knowing how much time has passed for wpm
import time

#this is for the random txt
import random


#we use stdscr becuase we need aceess to this to be able to write something onto the screen using the curses module
def start_screen(stdscr):
    stdscr.clear()
    stdscr.addstr("Welcome to the Typing Test")
    #this is so we can get onto the new line
    stdscr.addstr("\nPress any key to begin!")
    stdscr.refresh()
    #here we just need somone to press something to begin
    stdscr.getkey()


#this is to put the text over the target text
def display_text(stdscr, target, current, wpm=0):
    #here we display the target text
    stdscr.addstr(target)
    #so below our target we will hae our wpm
    #its one line down and zero from the left with wpm underneath our target
    stdscr.addstr(1, 0, f"WPM: {wpm}")


    #we loop through the current text
    #so i will be taking each letter one by one and char will equal to each one
    #so whatever character we are on according to their index we can use that to determine where we place them
    # i will keep getting incremented by 1 so we will start on character 0 which is the first one in the sentence so it will go directly on top of target text
    for i, char in enumerate(current):
        #so we have all the correct letters in the target text and then we will compare every character
        correct_char = target[i]
        #default color is green
        color = curses.color_pair(1)
        #if character isnt right then it will turn red
        if char != correct_char:
            color = curses.color_pair(2)
        #here it will then do everything when we type
        stdscr.addstr(0 ,i, char , color)

#this is for the different txts
def load_text():
    file_path = "/Users/ameshajid/Documents/VisualStudioCode/Small Projects/TypingTest/lines.txt"
    with open(file_path, "r") as f:
        lines = f.readlines()
        #this is so we can pcik any random line and get rid of any trailing after the end
        return random.choice(lines).strip()


#now we need something to store what our target text is and then print the target text is and then tell user to tpye
def wpm_text(stdscr):
    #this is going to be the text we want to complete
    target_text = load_text()
    #this will be empty so we can track what the person will be typing
    current_text = []
    #our oringial
    wpm = 0
    #this is for storing the realtime data
    start_time = time.time()
    #do not delay waiting for a user to press a key
    stdscr.nodelay(True)


    #here we want to register the key presses and put it over the target text
    while True:
        #to calculate the real time so here we are getting the real time minus our start time to get this real
        #we used max and 1 because there is a potential zero diviosn error
        time_elapsed = max(time.time() - start_time, 1)
        #this is the wpm equation
        #screw explanation just know fr
        wpm = round((len(current_text) / (time_elapsed / 60)) / 5)
        #we have this first so we dont have to press a key twice
        stdscr.clear()

        #we have to call display text function
        display_text(stdscr, target_text, current_text, wpm)

        #refresh everytime
        stdscr.refresh()

        #this is for the ending of the game
        # we have to check if current text = target text
        #we have to convert the list to a string so it equals the target text
        #"" is the delimiter which combines every list with whatever is in there
        if "".join(current_text)  == target_text:
            #we do this so we can wait for them to hit a key to get rid of it 
            stdscr.nodelay(False)
            break

        #here we will get the keys pressed then add it to the current text

        #this wpm doesnt start until we get a key so what we will do is not to that we want time to start
        #we will get an exceptin becasue of this line so we need try except it might crash
        try:
            key = stdscr.getkey()
        except:
            #brings us back to the top and continue the code
            continue

        #here is the way to exit the loop basically exit code
        #if they hit the escape key this is the ASCII number
        if ord(key) == 27:
            break
        #right here we are going to make sure pressing backspace removes a letter
        #these are all the diff backspace representations including diff operating sustems
        if key in ("Key_BACKSPACE", "\b", "\x7f"):
            #if anytime its more than zero then it will remove the last letter added
            if len(current_text) > 0:
                current_text.pop()
        #here we will make sure we dont let people add more than what we have for the target 
        elif len(current_text) < len(target_text):
            current_text.append(key)


#stdscr = standard output screen
#std is the standard output the standard output is the terminal where we put stuff
#scr is a screen the puts it over the terminal
def main(stdscr):
    #so this is after everything below us, we are going to be sttyling the terminal 
    #we need a pairing of a foreground(the text) and the background
    #1 is the id which holds the colored pair
    #green is the text color and white is teh background color
    curses.init_pair(1, curses. COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)   
    #first we want to clear the entire terminal cause theres always stuff on it
    stdscr.clear()
    #now adding text to the screen
    #.addstr addds text
    #here we are going to refrence the colored pair for the text
    #stdscr.addstr("Hellow World", curses.color_pair(1))

    #the first number is how many space away from the top
    #the second number is how many psaces from the left
    stdscr.addstr(0, 0, "HelloWorld")
    #then we need to refresh the screeen
    stdscr.refresh()
    #now we need to get input from the user so this will wait for the user
    #we will make this equal a variable and then print it to see what key the person types in
    #key = stdscr.getkey()
    #print(key)

    #here we are calling the start screen from inside this function
    start_screen(stdscr)
    #this is so we can play again
    while True:
        wpm_text(stdscr)
        stdscr.addstr(2, 0, "You completed the text! Press any key to continue...")
        key = stdscr.getkey()
        #if key = escape then break if not continue
        if ord(key) == 27:
            break
#here now we are going to call the function and we need to using wrapper
wrapper(main)




