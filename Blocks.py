__author__ = 'deathowl'

import pyglet

class Registry( object ):
    colors = ['rock', 'lava','weed', 'ghost', 'blood', ]

    ROCK, LAVA, WEED, GHOST, BLOOD = range( len(colors) )

    images = [pyglet.resource.image('block_%s.png' % color) for color in colors ]

