import matplotlib

matplotlib.use('Qt5Agg')

import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
import plotly.tools as tls

class function:

    def __init__(self, conditionArray,funcArray, Xfunc):
        self.conditionArray = conditionArray
        self.funcArray = funcArray
        self.Xfunc = Xfunc
        self.x = np.linspace(self.Xfunc[0]-0.01, self.Xfunc[1]+0.01, self.Xfunc[2])

    def __str__(self):
        return str("Aca voy a poner en el JupyterNotebook algo cool para mostrar tipo Latex la ec")

    def Xvalues(self):
        return self.x
    
    def Condition(self):
        return [self.x<self.Xfunc[0], (self.x>=self.Xfunc[0]) & (self.x<=self.Xfunc[1]), self.x>self.Xfunc[2]]

    def Function(self):
        return [lambda f:self.funcArray[0],lambda f:self.funcArray[1],lambda f:self.funcArray[2]]

    def Yvalues(self):
        return np.piecewise(self.x, self.Condition(), self.Function()) 

    def lastX(self):
        return self.Xfunc[1]

# First set up the figure, the axis, and the plot element we want to animate
fig = plt.figure(num=None, figsize=(14, 6), dpi=80, facecolor='w', edgecolor='k')

movefunction = function ([2,11],[0, 1, 0], [2,4,1000])
staticfunction = function ([7.5,11], [0, 10, 0], [7.5, 11, 1000])

XMAX = 20
desplazamiento = XMAX - movefunction.lastX()


ax = plt.axes(xlim=(0, XMAX), ylim=(-0.1, 50))
#eje_x = [1,2,3,4,5,6,7,8,9,10]
#my_xticks = ['t', 't-1', 't-2', 't-3', 't-4', 't-5', 't-6', 't-7', 't-8', 't-9']
#plt.xticks(eje_x, my_xticks)

line, = ax.plot([], [], lw=2)
line2, = ax.plot ([], [], lw=2)

x2 = staticfunction.Xvalues()
y2 = staticfunction.Yvalues()
polygone = ax.fill_between (x2[0:0] ,y2[0:0], facecolor='yellow', alpha=0.5)


# initialization function: plot the background of each frame
def init():
    line.set_data([], [])
    line2.set_data([x2], [y2])
    return line, line2, polygone

# animation function.  This is called sequentially
def animate(t):

    x = movefunction.Xvalues()
    y = movefunction.Yvalues()
    z = np.copy(x)
    
    z = z + (t/100)

    ax.collections.clear()
     
    if (z[-1] >= x2[0]): # Si la parte más a la derecha de la funcion que se mueve es mayor que la parte de mas a la izquierda de la estatica:
        polygone = ax.fill_between (x2[0:2*(t-348)] ,y2[0:2*(t-348)], facecolor='yellow', alpha=0.5)

    else:
        polygone = ax.fill_between (x2[0:0] ,y2[0:0], facecolor='yellow', alpha=0.5)
    # sin el else no anda, se referencia antes de que se llame, no entiendo por que.

    line.set_data(z, y)
    return line, line2, polygone


# call the animator.  blit=True means only re-draw the parts that have changed.
anim = animation.FuncAnimation(fig, animate, init_func=init,
                               frames= desplazamiento * 100, interval=5, blit=True)

# save the animation as an mp4.  This requires ffmpeg or mencoder to be
# installed.  The extra_args ensure that the x264 codec is used, so that
# the video can be embedded in html5.  You may need to adjust this for
# your system: for more information, see
# http://matplotlib.sourceforge.net/api/animation_api.html
#anim.save('basic_animation.mp4', fps=30, extra_args=['-vcodec', 'libx264'])

plt.show()

#Si ymove>yquieto pinto yquieto,
#Sino pinto ymove
#Mientras haya intersección:
#Si ymove>yquieto pinto yquieto,
#Sino pinto ymove
#Una variable que guarde un array de condiciones y otro un array de funciones
#Y un intervalo donde graficar en X la función
#Una clase llamada funcion que le pasas las condiciones y las funciones y las escribe correctamente
#Adentro tiene el piecewise directamentee
#Los parametros para inicializarla son:
#1. Un np.ndarray de valores de X.
#2. Un array de funciones
#3. Un array de condiciones

#Los metodos son:
#yvalues()
#xvalues()
#
#
#
#