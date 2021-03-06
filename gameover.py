from __future__ import division, print_function, unicode_literals

# pyglet realted
from pyglet.window import key

# cocos2d related
from cocos.layer import Layer, ColorLayer
from cocos.director import director
from cocos.text import Label
from cocos.actions import *

# tetrico related
import soundex
import status


class GameOver( ColorLayer ):
    is_event_handler = True #: enable pyglet's events

    def __init__( self, win = False):
        super(GameOver,self).__init__( 32,32,32,64)

        w,h = director.get_window_size()

        if win:
            soundex.play('win.mp3')
            msg = 'YOU WIN'
        else:
            soundex.play('fail.mp3')
            msg = 'GAME OVER'

        label = Label(msg,
                    font_name='Edit Undo Line BRK',
                    font_size=54,
                    anchor_y='center',
                    anchor_x='center' )
        label.position =  ( w/2.0, h/2.0 )

        self.add( label )

        angle = 5
        duration = 0.05
        accel = 2
        rot = Accelerate(Rotate( angle, duration//2 ), accel)
        rot2 = Accelerate(Rotate( -angle*2, duration), accel)
        effect = rot + (rot2 + Reverse(rot2)) * 4 + Reverse(rot)
        
        label.do( Repeat( Delay(5) + effect ) )


    def on_key_press( self, k, m ):
        if (k == key.ENTER or k == key.ESCAPE):
            director.pop()
            return True

        return False

    def on_text( self, t ):
        return False
