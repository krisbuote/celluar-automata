'''
Adapted by Kristopher Buote from the blog https://jakevdp.github.io/blog/2013/08/07/conways-game-of-life/
'''
import numpy as np
# JSAnimation import available at https://github.com/jakevdp/JSAnimation
#from JSAnimation.IPython_display import display_animation, anim_to_html
from matplotlib import animation
from matplotlib import pyplot as plt


def life_step_1(X):
    """Game of life step using generator expressions"""
    nbrs_count = sum(np.roll(np.roll(X, i, 0), j, 1)
                     for i in (-1, 0, 1) for j in (-1, 0, 1)
                     if (i != 0 or j != 0))
    return (nbrs_count == 3) | (X & (nbrs_count == 2))

def life_step_2(X):
    """Game of life step using scipy tools"""
    from scipy.signal import convolve2d
    nbrs_count = convolve2d(X, np.ones((3, 3)), mode='same', boundary='wrap') - X
    return (nbrs_count == 3) | (X & (nbrs_count == 2))


life_step = life_step_1

#%pylab inline

def life_animation(X, dpi=10, frames=10, interval=500, mode='loop'):
    """Produce a Game of Life Animation

    Parameters
    ----------
    X : array_like
        a two-dimensional numpy array showing the game board
    dpi : integer
        the number of dots per inch in the resulting animation.
        This controls the size of the game board on the screen
    frames : integer
        The number of frames to compute for the animation
    interval : float
        The time interval (in milliseconds) between frames
    mode : string
        The default mode of the animation.  Options are ['loop'|'once'|'reflect']
    """
    X = np.asarray(X)
    assert X.ndim == 2
    X = X.astype(bool)

    X_blank = np.zeros_like(X)
    figsize = (X.shape[1] * 1. / dpi, X.shape[0] * 1. / dpi)

    fig = plt.figure(figsize=figsize, dpi=dpi*50) #dpi*50 to make figure larger
    ax = fig.add_axes([0, 0, 1, 1], xticks=[], yticks=[], frameon=False)
    im = ax.imshow(X, cmap=plt.cm.binary, interpolation='nearest')
    im.set_clim(-0.05, 1)  # Make background gray

    # initialization function: plot the background of each frame
    def init():
        im.set_data(X_blank)
        return (im,)

    # animation function.  This is called sequentially
    def animate(i):
        im.set_data(animate.X)
        animate.X = life_step(animate.X)
        return (im,)

    animate.X = X

    anim = animation.FuncAnimation(fig, animate, init_func=init,
                                   frames=frames, interval=interval)

    # print anim_to_html(anim)
    # return display_animation(anim, default_mode=mode)
    return anim

X = np.zeros((17, 17))
X[2, 4:7] = 1
X[4:7, 7] = 1
X += X.T
X += X[:, ::-1]
X += X[::-1, :]

plt.show(life_animation(X, frames=6))


### ALTERNATIVE INITIAL CONDITIONS ###

# diehard = [[0, 0, 0, 0, 0, 0, 1, 0],
#            [1, 1, 0, 0, 0, 0, 0, 0],
#            [0, 1, 0, 0, 0, 1, 1, 1]]

# boat = [[1, 1, 0],
#         [1, 0, 1],
#         [0, 1, 0]]
#
# r_pentomino = [[0, 1, 1],
#                [1, 1, 0],
#                [0, 1, 0]]
#
# beacon = [[0, 0, 1, 1],
#           [0, 0, 1, 1],
#           [1, 1, 0, 0],
#           [1, 1, 0, 0]]
#
# acorn = [[0, 1, 0, 0, 0, 0, 0],
#          [0, 0, 0, 1, 0, 0, 0],
#          [1, 1, 0, 0, 1, 1, 1]]
#
# spaceship = [[0, 0, 1, 1, 0],
#              [1, 1, 0, 1, 1],
#              [1, 1, 1, 1, 0],
#              [0, 1, 1, 0, 0]]
#
# block_switch_engine = [[0, 0, 0, 0, 0, 0, 1, 0],
#                        [0, 0, 0, 0, 1, 0, 1, 1],
#                        [0, 0, 0, 0, 1, 0, 1, 0],
#                        [0, 0, 0, 0, 1, 0, 0, 0],
#                        [0, 0, 1, 0, 0, 0, 0, 0],
#                        [1, 0, 1, 0, 0, 0, 0, 0]]
