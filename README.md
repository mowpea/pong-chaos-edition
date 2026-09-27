# PONG - CHAOS EDITION

This Project was created for CS50X. It is temporarily public for an application process with game company.

## Video Demo
Link: https://youtu.be/oYNCjxtInwc?si=n5PJ8Mc6D7AgDwJJ

## Project Description

### Overview

*Pong - Chaos Edition* is *Pong* with more game features and more questionable game design. 

It starts as classic *Pong*, but descends into chaos by adding new gameplay elements on top of the gameplay loop of its retro counterpart; additions that anyone with any regard for game design would deem offensive. That offence might however be forgiven, as it served no purpose other than to enrich the programming process with additional programming challenges.

### Game Features

The game starts with classic *Pong's* gameplay. As both player and opponent score points, things change: everything speeds up, a laser unlocks, a second laser unlocks, and finally, a second game of pong appears.

1. **Start Screen**
	The game starts on the start screen. While not a fully fledged main menu, it displays all controls and signals to press 'Enter' to start the game.
		---
2. **Audio / Music**
	Starting the game starts the music, which consists of two separate files. The first one plays once and ends. As it ends, the second file starts and loops until the end of the game. As the second file is the last segment of the first, it creates an illusion of a full music track that plays and loops its last part without interruptions. I composed and produced the music myself; hence my artist's name *mowpea* in the filename.

	Pressing '1' or '2' increases or lowers the volume.

	I also designed a whole batch of sound effects for the game, but could not implement them due to a game-breaking bug (s. below)
		---
3.	**Classic Pong Gameplay Loop**
	After exiting the start screen, a screen similar to classic *Pong* appears, with one paddle on each side. The player controls the left paddle: 'W' moves it up, 'S' moves it down. 
	
	A ball spawns at the screen center and moves either to the left or right. The ball bounces off the paddles and the top and bottom of the screen, but leaves the screen to the left and right. If it leaves to one side, the opposing side score a point. The scores are displayed at the screen center. A new ball spawns, but waits briefly before it moves again, giving both player and opponent time to reposition themselves.

	The ball increases speed slightly after each bounce. I added this feature so that the game progresses slightly, even if a ball exchange drags out.
		---
4. **Level Progression and Abilities**
	The game unlocks new abilities as the total score increases. The progression works as follows:

	**Total Score < 3**
	Level 1. The player's base speed is higher than the opponent's. The player can activate a temporary speed boost by pressing 'SPACE'. The opponent does not have that ability.

	**Total Score >= 3**
	Level 2. Base speed of all entities (player, opponent, ball) increases. Both player and opponent can shoot red lasers. Destroying a ball with a red laser scores the shooter +1 point. Red lasers bounce off other paddles allowing them to fly back and forth.

	**Total Score >= 6**
	Level 3. Base speed of all entities increases again. The opponent's base speed is now higher than the player's. Both player and opponent can shoot blue-ish lasers. These slow down the other paddle and the ball upon impact. It flies much faster than the red laser, making it a viable strategy to slow down the ball and destroy it with the red laser.

	**Total Score >= 9**
	End game. A new set of paddles and ball appear. 
	
	The player can control a new paddle at the bottom of the screen: 'LEFT ARROW' moves it to the left, 'RIGHT ARROW' moves it to the right. A second opponent is at the top of the screen. 
	
	A new ball, previously thought to be part of the playing field, moves and (re)spawns. It bounces off all paddles and the left and right of the screen, and leaves through the top and bottom. It also counts towards the scores and can be destroyed and slowed down like the first ball.

	Chaos ensues, but the game remains playable and winnable.
		---
5. **Opponent AI**
	The opponent on the right follows the first, the opponent at the top the second ball. Both update their positions in relation to their respective balls. Both have `self.acceleration` variables controlling how fast they change directions. It's designed to give their paddles a feeling of inertia. The player has that too, but less pronounced. Having the opponents not move with linear speed gives them a more organic feel. It also makes them more prone to mistakes.
		---
6. **Pause Screen**
	Pressing 'Enter' during gameplay pauses the gameplay and the music.
		---
7. **End Screen**
	If either player or opponent reaches 30 points, the gameplay loop ends with the end screen. It has two different messages depending on the outcome. The music fades out.
		---
8. **Graphical Features**
	The game's graphics mainly feature simple shapes. There are two kinds of animations:

	Whenever a collision occurs, a graphical element in the game flashes in a brighter color, indicating to the player that something important has happened. The paddles' outer rectangles flash, when balls or lasers bounce off them. The sides of the playing field flash, when balls travel through them, but not when balls bounce off them, since the latter does score points.

	When a red laser hits a ball, the ball explodes and the laser vanishes. The explosion is created using multiple surfaces played in a timed sequenced, similar to animations using sprites. This animation serves as a visual reward, since shooting a ball is fairly challenging.

	Apart from the animations, the colors of all entities change with progressing levels from a brighter to a more darker, saturated tone. The two temporary status effects, boost and frozen, are also accompanied by temporary color changes.

	The center line of the playing field disappears with the introduction of the second pong game. The circle shape in the center turns out to be the second ball.

	The graphics are kept simple and animations are used only for critical visual cues.

### Programming Process and Design

#### Learning Pygame

I learned pygame through two major resources: pygame's documentation and youtube tutorials from the channel 'Clear Code' run by Christian Koch. He has a comprehensive tutorial series on pygame and in one video, he recreates classic *Pong*. I worked through that tutorial and based my code on some code snippets shown in it. All in all, I used a fair amount of high-level concepts from his videos to build a basic game loop. All code quotations are indicated in my code.

#### Challenges

Adding features beyond the classic *Pong* gameplay proved to be a valuable challenge. I didn't use any tutorials for my own gameplay ideas. In fact, I never felt like I needed to consult any resource other than the pygame documentation. I had all the tools I needed to make basic games, even if the code wouldn't always be efficient or elegant - or pythonic.

The biggest challenge was writing efficient code. As my game's code grew, I struggled with keeping everything modular and reusable. The code works and looking back at it, I understand every line. However, I am sure that a lot of code could have been condensed in fewer lines. A lot of functionality could have been bundled together and put into classes to be inherited by other classes. 

A prime suspect for possibly inefficient code is my code section where I drew lines and shapes and displayed text on screen; in the start screen and for the playing field during gameplay. I tried to come up with for-loops to avoid repeating lines of code with small changes, but wasn't able to make something within a reasonable time. So I opted to write more code for the sake of readability.

As the game evolved, readability became my priority. I created a lot of variables and short functions just to improve code readability. I also opted to write out keyword arguments over multiple lines. This took up large amounts of space, but again helped with code readability.

At some point, I simply needed to implement my desired features and finish the game. It took me roughly 75 hours to design and program this version of *Pong*. I will move on to other game projects and keep learning. This project needed to come to an appropriate end; meaning that it needed to work. And that it does.

An unrelated challenge stemmed from CS50P's requirement to have three functions that can be tested with `pytest`. I couldn't come up with a sensible way to create functions that were vital to the gameplay and that returned value suitable for `pytest`. In the end, I added `return` to three smaller functions. It feels like an unsatisfying and artificial solution, but for me, it was preferable to asking for more complex solutions on the internet.

Another challenge that didn't come up during any of CS50P's problem sets was dealing with an indefinite `while` loop. Making anything happen just once during the gameplay loop wasn't as simple and I ended up writing a lot of small functions and variables to achieve that.

#### Using pygame's `draw` module

As mentioned above, the most verbose sections of my code dealt with drawing of shapes. I could have simplified everything by importing free art assets as surfaces. However, I wanted to challenge myself by drawing anything I needed with pygame's `draw` module. It required a bit of math and a lot of testing, but resulted in a better understanding of graphics. After this, I will surely appreciate more sophisticated functionalities of actual game engines like Godot, which is where I will go to after this.

#### Audio Issue

Since I'm a Sound Designer, I created a batch of sound effects to supplement my game with auditive feedback. I created Sound objects for all of them and organized those in a dictionary at the top of my code. However, as I called `play()` on these Sound objects during gameplay, the game froze without error messages.

After a numerous tests, I can rule out typical pygame audio issues such as wrong audio format, lack of channels, etc. I could play and re-trigger multiple sound effects in the start screen without fail. However, during gameplay, the game froze at seemingly random points. My suspicion is that my gameplay loop is too heavy and/or inefficiently coded which causes pygame to freeze when sounds are being played on top.

Changing this seemed to require an overhaul of my code's design. As I am unfamiliar with code optimisation beyond the very basics, this seemed beyond the scope of my project. The lack of sound effects it painful, but then again, I needed to finish this project. I left the audio files and the code sections concerning them in the project for future reference.

#### Learnings

This was an invaluable and satisfying learning experience. I walk away with joy for object-oriented-programming, which will come in handy in my next game project.
