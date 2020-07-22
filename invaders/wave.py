"""
Subcontroller module for Alien Invaders

This module contains the subcontroller to manage a single level or wave in
the Alien Invaders game.  Instances of Wave represent a single wave. Whenever
you move to a new level, you are expected to make a new instance of the class.

The subcontroller Wave manages the ship, the aliens and any laser bolts on
screen. These are model objects.  Their classes are defined in models.py.

Most of your work on this assignment will be in either this module or
models.py. Whether a helper method belongs in this module or models.py is
often a complicated issue.  If you do not know, ask on Piazza and we will
answer.

# James Pendergast Net ID: jcp327
  Josue Garcia Net ID: jg2287
# 12/12/19
"""
from game2d import *
from consts import *
from models import *
import random


# PRIMARY RULE: Wave can only access attributes in models.py via getters/setters
# Wave is NOT allowed to access anything in app.py (Subcontrollers are not
# permitted to access anything in their parent. To see why, take CS 3152)


class Wave(object):
    """
    This class controls a single level or wave of Alien Invaders.

    This subcontroller has a reference to the ship, aliens, and any laser bolts
    on screen. It animates the laser bolts, removing any aliens as necessary.
    It also marches the aliens back and forth across the screen until they are
    all destroyed or they reach the defense line (at which point the player
    loses). When the wave is complete, you  should create a NEW instance of
    Wave (in Invaders) if you want to make a new wave of aliens.

    If you want to pause the game, tell this controller to draw, but do not
    update.  See subcontrollers.py from Lecture 24 for an example.  This
    class will be similar to than one in how it interacts with the main class
    Invaders.

    All of the attributes of this class ar to be hidden. You may find that
    you want to access an attribute in class Invaders. It is okay if you do,
    but you MAY NOT ACCESS THE ATTRIBUTES DIRECTLY. You must use a getter
    and/or setter for any attribute that you need to access in Invaders.
    Only add the getters and setters that you need for Invaders. You can keep
    everything else hidden.

    """
    # HIDDEN ATTRIBUTES:
    # Attribute _ship: the player ship to control
    # Invariant: _ship is a Ship object or None
    #
    # Attribute _aliens: the 2d list of aliens in the wave
    # Invariant: _aliens is a rectangular 2d list containing Alien objects or
    #None
    #
    # Attribute _bolts: the laser bolts currently on screen
    # Invariant: _bolts is a list of Bolt objects, possibly empty
    #
    # Attribute _dline: the defensive line being protected
    # Invariant : _dline is a GPath object
    #
    # Attribute _lives: the number of lives left
    # Invariant: _lives is an int >= 0
    #
    # Attribute _time: the amount of time since the last Alien "step"
    # Invariant: _time is a float >= 0s
    #
    # Attribute _time: the amount of time since the last Alien "step"
    # Invariant: _time is a float >= 0s
    #
    # You may change any attribute above, as long as you update the invariant
    # You may also add any new attributes as long as you document them.

    # LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    # Attribute _down: the amount of times the aliens should move down
    # Invariant: _down is a int and it is >= 0

    # Attribute _numsteps: the amount of steps when an alien fires a bolt
    #Invariant: _numsteps is an int >= 1

    #Attribute _dives:boolean that says if the alien touched the defensive line
    #Invariant: _dives is boolean True or False

    #Attribute _pew:boolean that says if sound is on or off
    #Invariant: _pew is boolean True or False

    #Attribute _pewsound:object of sound class
    #Invariant: _pewsound is a sound object

    #Attribute _blast: object of sound class
    #Invariant: _blast is a sound object

    #Attribute _popthree: object of sound class
    #Invariant: _popthree is a sound object

    #Attribute _pewSound2: object of sound class
    #Invariant: _pewSound2 is a sound object

    #Attribute _alienspeed: speed of the alien wave
    #Invariant: _alienspeed is an int >=1


    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getPaused(self):
        """return the attribute paused"""
        return self._paused

    def setPaused(self,value):
        """set the paused attribute to a value
           Precondition: value is a int >=0"""
        self._paused = value

    def getLives(self):
            """return the number of lives"""
            return self._lives

    def getAliens(self):
            """get the number of aliens that have turned to None"""
            x = 0
            for row in range(len(self._aliens)):
                for col in range(len(self._aliens[row])):
                  if self._aliens[row][col] == None:
                      x +=1
            return x

    def getAlienssum(self):
            """get the number of aliens"""
            x = 0
            for row in range(len(self._aliens)):
                for col in range(len(self._aliens[row])):
                      x +=1
            return x
    def getAlienSpeed(self):
            """return the number of lives"""
            return self._alienspeed

    def setAlienSpeed(self,value):
            """return the number of lives"""
            self._alienspeed = self._alienspeed/(value)


    # INITIALIZER (standard form) TO CREATE SHIP AND ALIENS
    def __init__(self):
        """INITIALIZER (standard form) TO CREATE SHIP AND ALIENS"""
        self.AlienObjects()
        self.ShipObjects()
        self._time = 0
        self._down = 0
        self._lives = 3
        self._paused = 0
        self._bolts = []
        self._alienspeed = ALIEN_SPEED
        self._dive = False
        self._alien_bp = False
        self._pew = True
        self._numsteps=random.randint(1,BOLT_RATE)
        self._pewSound=Sound('pew1.wav')
        self._blast=Sound('blast1.wav')
        self._popthree=Sound('pop1.wav')
        self._pewSound2=Sound('pew2.wav')
        self._alienspeed=ALIEN_SPEED


    def AlienObjects(self):
        """Creates an Alien by creating a list for the attribute self._aliens
        and appending a list full of aliens to it. the list full of aliens
        contains the width height and image of the aliens. Additionally it has
        the spacing between the aliens"""
        self._aliens = []
        x = (ALIEN_H_SEP+(ALIEN_WIDTH//2))
        y = GAME_HEIGHT-(ALIEN_CEILING+(ALIEN_HEIGHT//2)) -(((ALIEN_ROWS-1)*\
        ALIEN_V_SEP)+(ALIEN_ROWS*ALIEN_HEIGHT))
        width = ALIEN_WIDTH
        height = ALIEN_HEIGHT
        n= 0
        source = ALIEN_IMAGES[0]
        for row in range(ALIEN_ROWS):
            nest = []
            if row != 0:
             y+=(ALIEN_V_SEP + ALIEN_HEIGHT)
            if row == 0:
                source = ALIEN_IMAGES[n]
            elif (row) % 2 != 0 and n < 2:
                source = ALIEN_IMAGES[n]
            elif (row) % 2 != 0 and n == 2:
                source = ALIEN_IMAGES[n]
            elif (row) % 2 == 0 and n < 2:
                n += 1
                source = ALIEN_IMAGES[n]
            elif (row) % 2 == 0 and n >= 2:
                n = 0
                source = ALIEN_IMAGES[n]
            x = 0
            for col in range(ALIENS_IN_ROW):
                x+=(ALIEN_H_SEP +ALIEN_WIDTH)
                nest.append(Alien(x,y,width,height,source))
            self._aliens.append(nest)

    def ShipObjects(self):
        """"this creates one ship with the image by assigning the self._ships
        attribute to the class SHIP"""
        x = GAME_WIDTH//2
        y = SHIP_BOTTOM
        width = SHIP_WIDTH
        height = SHIP_HEIGHT
        source = "ship.png"
        self._ships = Ship(x,y,width,height,source)



    # UPDATE METHOD TO MOVE THE SHIP, ALIENS, AND LASER BOLTS
    def update(self,input,dt):
        """ Causees the animation of the ship, bolt, and aliens
        Parameter input: thw users input when they click a button to make
         the ship move or shoot
        Precondition input: an object from GInput
        Parameter dt: the time since the last animation
        Precondition dt: it is a float which is >0"""
        self._time += dt
        if self._down == 0:
            self._MoveAliensRight(dt)
        if self._down != 0:
            self._MoveAliensLeft(dt)
        if input.is_key_down('left'):
            if self._ships != None:
             self._ships.x -=SHIP_MOVEMENT
             self._restrict_ship()
        if input.is_key_down('right'):
            if self._ships != None:
             self._ships.x +=SHIP_MOVEMENT
             self._restrict_ship()
        if input.is_key_down('up') and self._alien_bp == False:
            self._CreateShipBolt()
            if self._pew == True:
             self._pewSound.play()
        if input.is_key_down('m'):
                self._pew = False
        if input.is_key_down('u'):
                self._pew = True
        if self._time%self._numsteps == 0:
            self._CreateAlienbolt()
            self._numsteps=random.randint(1,BOLT_RATE)
        self._alientouched()
        self._Gameend()
        self._moveBolt()
        self._moveBoltAlien()
        self._COLLISIONAlien()
        self._COLLISIONShip()
        self._deleteBolt()

    def _restrict_ship(self):
        """check if the x postion of ship is less than the constant
        (SHIP_WIDTH*.5)
         or greater than (GAME_WIDTH- (SHIP_WIDTH*.5)). if x postion of ship is
          less
        thann the x position gets SHIP_WIDTH*0.5 and greater x position becomes
        (GAME_WIDTH- (SHIP_WIDTH*.5))"""
        if self._ships.x < (SHIP_WIDTH*.5):
            self._ships.x= SHIP_WIDTH*0.5
        if self._ships.x > (GAME_WIDTH- (SHIP_WIDTH*.5)):
            self._ships.x=(GAME_WIDTH- (SHIP_WIDTH*.5))

    def _CreateShipBolt(self):
       """ this method creates a ship bolt"""
       if self._ships !=None:
        x=self._ships.x
        y=SHIP_BOTTOM+SHIP_HEIGHT
        width=BOLT_WIDTH
        height=BOLT_HEIGHT
        fillcolor='blue'
        t= 0
        if self._alien_bp ==False:
            d = Bolt(x,y,width,height,fillcolor)
            d.setVelocity(BOLT_SPEED)
            self._bolts.append(d)
            self._alien_bp = True

    def _deleteBolt(self):
        """this method deleteBolt"""
        i = 0
        while i < len(self._bolts):
            if self._bolts[i] != None:
                if self._bolts[i].y >= (GAME_HEIGHT+(BOLT_HEIGHT//2)):
                    del self._bolts[i]
                    self._alien_bp = False
                elif self._bolts[i].y <= 0:
                    del self._bolts[i]
                else:
                    i+=1

    def _moveBolt(self):
        """this method move the bolt"""
        for bolt in self._bolts:
            if bolt != None:
                if bolt.isPlayerBolt() == True:
                    bolt.y += bolt.getVelocity()
                if bolt.isPlayerBolt()== False:
                    bolt.y += bolt.getVelocity()

    def _moveBoltAlien(self):
        """this method move the  alien bolt """
        for bolt in self._bolts:
            if bolt != None:
                if bolt.getVelocity()== -BOLT_SPEED:
                    bolt.y += bolt.getVelocity()

    def _CreateAlienbolt(self):
        """this method create an alien bolt"""
        randcol=random.randint(0,len(self._aliens[0])-1)
        checker = False
        for n in range(len(self._aliens)):
         if self._aliens[n] != None:
                if checker == False:
                    if(self._aliens[n][randcol]!=None):
                        checker = True
                        obj=self._aliens[n][randcol]
                        x=obj.x
                        y=(obj.y)-(ALIEN_HEIGHT//2)-(BOLT_HEIGHT//2)
                        width=BOLT_WIDTH
                        height=BOLT_HEIGHT
                        fillcolor='blue'
                        g = Bolt(x,y,width,height,fillcolor)
                        g.setVelocity(-BOLT_SPEED)
                        t= 0
                        self._bolts.append(g)
                        if self._pew==True:
                            self._pewSound2.play()

    def _vwalk(self):
     """this method moves the aliens down"""
     for row in range(len(self._aliens)):
       for col in range(len(self._aliens[row])):
        if self._aliens[row][col] != None:
         self._aliens[row][col].y -= ALIEN_V_WALK

    def _MoveAliensRight(self,dt):
        """Moves the aliens to the right and once the alien hits the right wall
           all the aliens move down by ALIEN_V_WALK constant.And if the alien
           hits the left wall all the aliens move down by ALIEN_V_WALK constant.
            parameter dt: is the amount of take that has pass since
            the last animation
            Precondition: dt is a float which is greater than 0"""
        if self._time >= self._alienspeed:
            boundary = False
            walked = False
            for row in range(len(self._aliens)):
                for col in range(len(self._aliens[row])):
                    if self._aliens[row][col] is not None:
                        if(walked == False):
                            if self._aliens[row][col].x> GAME_WIDTH-\
                            (ALIEN_H_SEP+(0.5*ALIEN_WIDTH)):
                                boundary = True
            if boundary:
                walked = True
                self._vwalk()
                self._down +=1
            else:
                for row in self._aliens:
                    for alien in row:
                        if alien is not None:
                            alien.x += ALIEN_H_WALK
            self._time = 0

    def _MoveAliensLeft(self,dt):
        """Moves the aliens to the right and once the alien hits the right wall
            all the aliens move down by ALIEN_V_WALK constant.And if the alien
            hits the left wall all the aliens move down by ALIEN_V_WALK
            constant.
            parameter dt: is the amount of take that has pass since
            the last animation
            Precondition: dt is a float which is greater than 0"""
        if self._time >= self._alienspeed:
            boundary = False
            walked = False
            for row in range(len(self._aliens)):
                for col in range(len(self._aliens[row])):
                    if self._aliens[row][col] is not None:
                        if(walked == False):
                            if self._aliens[row][col].x < (ALIEN_H_SEP+0.5*\
                            ALIEN_WIDTH):
                                boundary = True
            if boundary:
                walked = True
                self._vwalk()
                self._down =0
            else:
                for row in self._aliens:
                    for alien in row:
                        if alien is not None:
                            alien.x -= ALIEN_H_WALK
            self._time = 0

    def _Gameend(self):
        """This ends the game"""
        if self._lives == 0:
            self._ships = None
            self._dive == True
        if len(self._aliens)== 0:
            self._dive == True

    def _alientouched(self):
        """check to see if any alien touched the defense line"""
        for row in range(len(self._aliens)):
            for col in range(len(self._aliens[row])):
              if self._aliens[row][col] != None:
                  if (self._aliens[row][col].y\
                  -(ALIEN_HEIGHT/2)) <= DEFENSE_LINE:
                   self._lives = 0

    # DRAW METHOD TO DRAW THE SHIP, ALIENS, DEFENSIVE LINE AND BOLTS
    def draw(self,view):
        """this method draws the methods"""
        self._DisplayTheAlien(view)
        self._DisplayTheShip(view)
        self._displayTheDLine(view)
        self._DisplayTheBolt(view)

    def _DisplayTheAlien(self,view):
        """this method displays the all the aliens with the right amount of row
        and column in the screen"""
        for row in range(len(self._aliens)):
          for col in range(len(self._aliens[row])):
           if self._aliens[row][col] is not None:
               alien = self._aliens[row][col]
               alien.draw(view)

    def _displayTheDLine(self,view):
        """This method draws a defense line with the color black and
        width of 3"""
        self._dline = GPath(points=[0,DEFENSE_LINE,GAME_WIDTH,DEFENSE_LINE],\
        linecolor = 'black',linewidth=3)
        self._dline.draw(view)

    def _DisplayTheShip(self,view):
        """This displays/draws the ship"""
        if self._ships is not None:
         self._ships.draw(view)

    def _DisplayTheBolt(self,view):
        """This displays/draws the bolt"""
        for bolt in self._bolts:
            bolt.draw(view)

    # HELPER METHODS FOR COLLISION DETECTION
    def _COLLISIONAlien(self):
        """this method tells you when the alien collides with the bolt"""
        for bolt in self._bolts:
          for aliens in range(len(self._aliens)):
              for alien in range(len(self._aliens[aliens])):
                 if bolt != None:
                  if bolt.isPlayerBolt() == True:
                      if self._aliens[aliens][alien] != None:
                          if self._aliens[aliens][alien].collides(bolt) == True:
                              self._aliens[aliens][alien] = None
                              if bolt in self._bolts:
                                  self._bolts.remove(bolt)
                              self._alien_bp = False
                              if self._pew == True:
                               self._popthree.play()

    def _COLLISIONShip(self):
        """this method tells you when the bolt collides with the ship"""
        for bolt in self._bolts:
                  if self._ships != None:
                      if self._ships.collides(bolt) == True:
                          self._bolts.remove(bolt)
                          self._lives -= 1
                          self._paused = 1
                          if self._pew == True:
                            self._blast.play()
