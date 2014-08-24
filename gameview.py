from __future__ import division, print_function, unicode_literals
#pyglet
from pyglet.gl import *

# cocos2d related
from cocos.layer import Layer, ColorLayer
from cocos.scene import Scene
from cocos.director import director
from cocos.actions import *


from gamectrl import *
from gamemodel import *
import levels
import gameover
from constants import *
import soundex
from HUD import *



__all__ = ['get_newgame']

class GameView( Layer ):

    def __init__(self, model, hud ):
        super(GameView,self).__init__()

        width, height = director.get_window_size()

        aspect = width / float(height)
        self.grid_size = ( int(20 *aspect),20)
        self.duration = 8

        self.position = ( width//2 - GRIDY * BLOCK_DIMENSION // 2, 0 )
        self.transform_anchor = ( GRIDY*BLOCK_DIMENSION //2, GRIDX * BLOCK_DIMENSION//2)

        # background layer to delimit the pieces visually
        cl = ColorLayer( 112,66,20,50, width = GRIDX * BLOCK_DIMENSION, height=GRIDY * BLOCK_DIMENSION )
        self.add( cl, z=-1)

        self.model = model
        self.hud = hud

        self.model.push_handlers(   self.on_special_effect, \
                                    self.on_game_over, \
                                    self.on_level_complete, \
                                    self.on_move_block, \
                                    self.on_new_level, \
                                    self.on_win, \
                                    )

        self.hud.show_message( 'GET READY', self.model.start )

    def on_enter(self):
        super(GameView,self).on_enter()

        soundex.set_music('main.mp3')
        soundex.play_music()

    def on_exit(self):
        super(GameView,self).on_exit()
        soundex.stop_music()

    def on_move_block(self ):
        soundex.play('move.mp3')
        self.parent.add( gameover.GameOver(win=False), z=10 )
        return True

    def on_player_move(self):
        soundex.play('move.mp3')
        return True

    def on_level_complete( self ):
        soundex.play('level_complete.mp3')
        self.hud.show_message('Level complete', self.model.set_next_level)
        return True

    def on_new_level( self ):
        soundex.play('go.mp3')
        self.stop()
        self.do(StopGrid())
        self.rotation = 0
        self.scale = 1
        return True

    def on_game_over( self ):
        self.parent.add( gameover.GameOver(win=False), z=10 )
        return True

    def on_win( self ):
        self.parent.add( gameover.GameOver(win=True), z=10 )
        return True

    def on_special_effect( self, effects ):
        for e in effects:
            action = self.get_action(e, effects[e])
            self.do( action )

    def get_action( self, e, times=1 ):
        '''returns the actions for a specific effects'''

        w, h= director.get_window_size()
        center = (w/2.0, (GRIDY * BLOCK_DIMENSION) / 2.0  )

        # basic actions


        raise Exception("Effect not implemented: %s" % str(e) )
        return a

    def draw( self ):
        '''draw the map and the block'''

        glPushMatrix()
        self.transform()
        ##DRAW HERE.


        glPopMatrix()


def get_newgame():
    '''returns the game scene'''
    scene = Scene()

    # model
    model = GameModel()

    # controller
    ctrl = GameCtrl( model )

    # view
    hud = HUD()
    view = GameView( model, hud )

    # set controller in model
    model.set_controller( ctrl )

    # add controller
    scene.add( ctrl, z=1, name="controller" )

    # add view
    scene.add( hud, z=3, name="hud" )
    scene.add( BackgroundLayer(), z=0, name="background" )
    scene.add( view, z=2, name="view" )

    return scene
