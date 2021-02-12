###############################################################
# Program:
#     Milestone 10, Asteroids
#     Brother Cook, CS165
# Author:
#     Jordan Jarvis
# Summary:
#     Put your summary code here... 
# Above and Beyond
#     When you submit your final project (not for milestones),
#     list anything here that you did to go above and beyond
#     the base requirements for your project.
###############################################################

LFLAGS = `pkg-config --cflags --libs opencv` -fopenmp -lpthread
IDIR =-I /usr/local/include/opencv4
###############################################################
# Build the main game
###############################################################
a.out: Program.o FindNumbers.o
	g++ Program.o FindNumbers.o $(LFLAGS)

###############################################################
# Individual files
#    uiDraw.o       Draw polygons on the screen and do all OpenGL graphics
#    uiInteract.o   Handles input events
#    point.o        The position on the screen
#    game.o         Handles the game interaction
#    velocity.o     Velocity (speed and direction)
#    flyingObject.o Base class for all flying objects
#    ship.o         The player's ship
#    bullet.o       The bullets fired from the ship
#    rocks.o        Contains all of the Rock classes
###############################################################
FindNumbers.o: FindNumbers.cpp FindNumbers.h
	g++ $(IDIR) -c FindNumbers.cpp

Program.o: Program.cpp
	g++ -c Program.cpp $(LFLAGS) -fopenmp -lpthread

###############################################################
# General rules
###############################################################
clean:
	rm a.out *.o





##g++ Program.cpp `pkg-config --cflags --libs opencv` -fopenmp -lpthread