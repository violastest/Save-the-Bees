# Viola Dube
# Save the Bees Arcade Game
# Touch flowers to get points, avoid the bug spray cans


from tkinter import *
import random
import time

#variables
move_direction = 0
flower_list = [] # list containing all flowers generated, empty at start
bugSpray_list = [] # list containing all the bug spray cans generated, empty at start
bugSpray_speed = 2 # initial speed of falling bug spray


#functions

    
# function to generate flowers at random places
def generate_flowers():
    global level

    # pick a random x position
    xPosition = random.randint(1, 400)
    yPosition = random.randint(1,400)
   
    #create a flower at random position          
    flower = canvas.create_image(xPosition, yPosition, image = flower_image)

    #add flower to list
    flower_list.append(flower)
    
    #schedule this function to generate more flowers
    if level == 2:
        window.after(2000, generate_flowers)
    elif level == 3:
        window.after(3000, generate_flowers)
    else:
        window.after(1000, generate_flowers)


# function to generate bug spray cans
def generate_bugSpray():
    global level

    # pick a random x position
    xPosition = random.randint(1, 400)
   
    #create bug spray at random position          
    bugSpray = canvas.create_image(xPosition, 0, image = bugSpray_image)

    #add bugSpray to list
    bugSpray_list.append(bugSpray)
    
    #schedule this function to generate more flowers
    if level == 2:
        window.after(2000, generate_bugSpray)
    elif level == 3:
        window.after(1000, generate_bugSpray)
    else:
        window.after(3000, generate_bugSpray)


# function to move bugSpray downwards, and schedules call to move_bugSpray
def move_bugSpray():
    #loop through list of bugSpray and change y position
    for bugSpray  in bugSpray_list:
        canvas.move(bugSpray, 0, bugSpray_speed)
          
    #schedule this function to move yarn down again
    window.after(50, move_bugSpray)


# function updates score, level bug spray speed
def update_score_level():
    #use of global since variables are changed
    global score, level,bugSpray_speed
    score = score + 5
    score_display.config(text = "Score:" + str(score))
    #determine if level needs to change
    #update level and yarn_speed
    if score > 50 and score <= 100 :
        bugSpray_speed = bugSpray_speed +1
        level = 2
        level_display.config(text="Level: " + str(level))
    elif score > 100:
        bugSpray_speed = bugSpray_speed +1
        level = 3
        level_display.config(text="Level: " + str(level))

# function to check distance between 2 objects - return true if they touch
def collision(item1, item2, distance):
    xDistance = abs(canvas.coords(item1)[0] - canvas.coords(item2)[0])
    yDistance = abs(canvas.coords(item1)[1] - canvas.coords(item2)[1])
    overlap = xDistance < distance and yDistance < distance
    return overlap

# function checks if bee hits flower, update score and level and remove list,
# check if bee hits bug spray. If bug hits bug spray Game Over
def check_hits():
    # check if bee hit yarn
    for flower in flower_list:
        if collision(playerBee, flower, 30):
            canvas.delete(flower) # remove from canvas
            #find where in list and remove and update score
            flower_list.remove(flower)
            update_score_level()

    #check if bee hit bug spray
    for bugSpray in bugSpray_list:
        if collision(playerBee, bugSpray, 30):
            game_over = canvas.create_text(200,200, text ="Game Over", \
                    fill = "red", font = ("Helvetica",30))
            
            window.after(2000, end_game_over)
                
    #schedule check hits again
    window.after(100, check_hits)

# function handles when user first pressses arrow keys
def check_input(event):
    global move_direction
    key = event.keysym
    if key == "Right":
        move_direction = "Right"
    elif key == "Left":
        move_direction = "Left"
    elif key == "Up":
        move_direction = "Up"
    elif key == "Down":
        move_direction = "Down"


#function handles when user stops pressing arrow keys
def end_input(event):
    global move_direction
    move_direction = "None"

    
# function checks if not on edge and updates x coordinatesbased on right\left
def move_bee():
    if move_direction == "Right" and canvas.coords(playerBee)[0] < 400:
        canvas.move(playerBee, 10, 0)
    if move_direction == "Left" and canvas.coords(playerBee)[0] > 0:
        canvas.move(playerBee, -10, 0)
    if move_direction == "Up" and canvas.coords(playerBee)[1] > 0 :
        canvas.move(playerBee, 0, -10)
    if move_direction == "Down" and canvas.coords(playerBee)[1] < 400:
        canvas.move(playerBee, 0, 10)
        
    window.after(16, move_bee) # move the bee at 60 frames per second


# function called to end game - destroys window
def end_game_over():
    window.destroy()

# function to clear the instructions on the screen
def end_title():
    time.sleep(5)               # sleep for 5 seconds to give player chance to read screen
    canvas.delete(title)        # remove title
    canvas.delete(directions1)  # remove directions
    canvas.delete(directions2)  # remove directions
    canvas.delete(bee_info1)    # remove bee info
    canvas.delete(bee_info2)
    canvas.delete(bee_info3)


#make a window
window = Tk()
window.title("Save the Bees Game")

#create a canvas to put objects on the screen
canvas = Canvas(window, width=400, height=400, bg='white')
canvas.pack()

#set up welcome screen with title and directions
title = canvas.create_text(200,200, text = 'Save the Bees', fill = 'black', \
    font = ("Helvetica", 30))
directions1 = canvas.create_text(200, 370, \
    text ="Get points by touching flowers. Avoid the bugspray", \
    fill='black', font = ('Helvetica', 10))
directions2 =canvas.create_text(200, 390, \
    text ="Use the arrow keys to move the bee.",
    fill ='black', font = ('Helvetica', 10))

#diplay info about bees
bee_info1 = canvas.create_text(200, 50, text = "Bees are essential for the health of people and the planet.", fill = "black", \
    font = ("Helvetica", 10))
bee_info2 =canvas.create_text(200, 75, text = "Honey and other products have medicinal properties, and the ", fill = "black", \
    font = ("Helvetica", 10))                              
bee_info3 = canvas.create_text(200, 100, text = "role of bees as pollinators makes them vital for food supplies.", fill = "black", \
    font = ("Helvetica", 10))

#set up score display using label widget
score = 0
score_display = Label(window, text="Score: " + str(score))
score_display.pack()

#set up level display using label widget
level =1
level_display = Label(window, text="Level: " + str(level))
level_display.pack()

#create an image object using the bee gif file
player_image = PhotoImage(file="bee.gif")
#use image object to create a character at position
playerBee = canvas.create_image(200, 300, image = player_image)

flower_image = PhotoImage(file="flower.gif")

bugSpray_image = PhotoImage(file="bugSpray.gif")

# start game loop by scheduling all the functions
window.after(1000, end_title)       # clear title and instructions
window.after(1000,generate_flowers)  # start making flowers
window.after(3000, generate_bugSpray) # start making bugSpray
window.after(1000, move_bugSpray)
window.after(1000,check_hits)       # check if bee hit a flower
window.after(1000,move_bee)         # handle keyboard controls

# bind the keys to the cat
canvas.bind_all('<KeyPress>', check_input) # bind key press
canvas.bind_all('<KeyRelease>', end_input) # bind all keys to circle

window.mainloop() #last line GUI main event loop
