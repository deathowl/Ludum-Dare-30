from __future__ import division, print_function, unicode_literals

# This code is so you can run the samples without installing the package
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

# stdlib
import copy
import random
import weakref

# pyglet related
import pyglet

# cocos2d related
from cocos.euclid import Point2

from constants import *
from status import status
import levels

__all__ = ['GameModel']

#
# Model (of the MVC pattern)
#

class GameModel( pyglet.event.EventDispatcher ):

    def __init__(self):
        super(GameModel,self).__init__()

        self.init()

        # grid
        self.map = {}

        status.reset()


        # phony level
        status.level = levels.levels[0]

    def start( self ):
        self.set_next_level()

    def set_controller( self, ctrl ):
        self.ctrl = weakref.ref( ctrl )

    def init_map(self):
        '''creates a map'''
        self.map= {}
        for i in range(GRIDX):
            for j in range(GRIDY):
                self.map[ (i,j) ] = 0

    def check_map(self):
        '''checks if the line is complete'''
        lines = []
        #Check map for possible events.

        lines.reverse()

        effects = []
        for j in GRIDX:
            for i in range(GRIDY):
                e = self.map[(i,j)]
                effects.append( e )

        if effects:
            self.process_effects( effects )
            #HANDLE WIN SCENARIO
           # self.ctrl().pause_controller()
           # self.dispatch_event("on_win")
           # else:
           # self.dispatch_event("on_level_complete")

    def init( self ):
        status.lines = 0
        self.init_map()

    def set_next_level( self ):
        self.ctrl().resume_controller()

        if status.level_idx is None:
            status.level_idx = 0
        else:
            status.level_idx += 1


        l = levels.levels[status.level_idx]

        self.init()
        status.level = l()
        self.dispatch_event("on_new_level")


    def process_effects( self, effects ):
        d = {}
        elements = set(effects)
        for e in elements:
            d[ e ] = effects.count(e)

        self.dispatch_event("on_special_effect", d )


    def are_valid_movements(self):
        '''check wheter there are any left valid movement'''
        for i in range(self.block.x):
            for j in range(self.block.x):
                if self.block.get(i,j):
                    if j + self.block.pos.y == 0:
                        return False
                    if self.map.get( (i + self.block.pos.x,j + self.block.pos.y -1), False ):
                        return False
        return True

    def block_right( self ):
        '''moves right the block 1 square'''
        self.block.backup()
        self.block.pos.x += 1
        if not self.is_valid_block():
            self.block.restore()
        else:
            self.dispatch_event("on_move_block")

    def block_left( self ):
        '''moves left the block 1 square'''
        self.block.backup()
        self.block.pos.x -= 1
        if not self.is_valid_block():
            self.block.restore()
        else:
            self.dispatch_event("on_move_block")

    def block_down( self, sound=True ):
        '''moves down the block 1 square'''
        self.block.backup()
        self.block.pos.y -= 1
        if not self.is_valid_block():
            self.block.restore()
            self.next_block()
        else:
            if sound:
                self.dispatch_event("on_move_block")


    def is_valid_block( self ):
        '''check wheter the block is valid in the current position'''
        #IF player tries to push block out of the map, we should cry for help. Or return false. Rather return false.
        return True


class Block( object ):
    '''Base class for all blocks'''
    def __init__(self):
        super( Block, self).__init__()

        self.pos = Point2( COLUMNS//2-1, ROWS )
        self.rot = 0

        for x in range( len(self._shape) ):
            for y in range( len( self._shape[x]) ):
                if self._shape[x][y]:
                    r = random.random()
                    if r < status.level.prob:
                        color = random.choice( status.level.blocks )
                    else:
                        color = self.color
                    self._shape[x][y] = color

    def draw( self ):
        '''draw the block'''
        for i in range(self.x):
            for j in range(self.x):
                c = self.get(i,j)
                if c:
                    Block.images[c].blit((i + self.pos.x) * BLOCK_DIMENSION, (j + self.pos.y) * BLOCK_DIMENSION)

    def backup( self ):
        '''saves a copy of the block'''
        self.save_pos = copy.copy( self.pos )
        self.save_rot = self.rot

    def restore( self ):
        '''restore a copy of the block'''
        self.pos = self.save_pos
        self.rot = self.save_rot

    def get(self,x,y):
        '''get position x,y of the block'''
        if self.rot == 0:
            i,j = x,y
        elif self.rot == 1:
            i,j = y,(self.x -x -1 )
        elif self.rot == 2:
            i,j = (self.x - x -1), (self.x -y -1)
        elif self.rot == 3:
            i,j = (self.x - y -1 ), x

        return self._shape[i][j]




GameModel.register_event_type('on_special_effect')
GameModel.register_event_type('on_line_complete')
GameModel.register_event_type('on_level_complete')
GameModel.register_event_type('on_new_level')
GameModel.register_event_type('on_game_over')
GameModel.register_event_type('on_move_block')
GameModel.register_event_type('on_drop_block')
GameModel.register_event_type('on_win')
