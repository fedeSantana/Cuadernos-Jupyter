import plotly.tools as tls
from matplotlib import animation
from matplotlib import pyplot as plt
import numpy as np
import matplotlib

matplotlib.use('Qt5Agg')

class function:

    def __init__(self, domain, conditionArray, functions, velocity):
        self.conditionArray = conditionArray
        self.functions = functions
        self.lastX = domain[1]
        self.x = np.linspace(domain[0]-0.01, domain[1]+0.01, domain[2])
        self.velocity = velocity

    def __str__(self):
        return str("Aca voy a poner en el JupyterNotebook algo cool para mostrar tipo Latex la ec")

    def Xvalues(self):
        return self.x

    def Velocidad(self):
        return (self.x[10] - self.x[9])*self.velocity

    def VelocidadEntera(self):
        return self.velocity

    def Condition(self):
        
        conditions = [self.x < self.conditionArray[0]]
       
        if (len(self.conditionArray) == 2):
            conditions.append( (self.x > self.conditionArray[0]) & (self.x < self.conditionArray[1]) )
            conditions.append( self.x > self.conditionArray[1] )
            return conditions

        else:
            for i, condition in enumerate(self.conditionArray[1:-1:]):
                conditions.append( (self.x >= condition) & (self.x < self.conditionArray[i+1]) )
            
            conditions.append(self.x > self.conditionArray[-1])   
            return conditions

    def setFunctions(self, functions):
        self.functions = functions

    def Yvalues(self):
        return np.piecewise(self.x, self.Condition(), self.functions)

    def LastX(self):
        return self.lastX

    def Desplazamiento (self, XMAX):
        return XMAX - self.LastX()
    



# Primero preparo la figura.
fig = plt.figure(num=None, figsize=(14, 6), dpi=80,
                 facecolor='w', edgecolor='k')

#Luego preparo el eje.
XMAX = 20
ax = plt.axes(xlim=(-10, XMAX), ylim=(-20, 50))

#eje_x = [1,2,3,4,5,6,7,8,9,10]
#my_xticks = ['t', 't-1', 't-2', 't-3', 't-4', 't-5', 't-6', 't-7', 't-8', 't-9']
#plt.xticks(eje_x, my_xticks)

#Preparo las funciones que usaré
movefunction = function([0, 5, 100], [0,5], [lambda x: 0, lambda x: x**2, lambda x: 0], 1)
staticfunction = function([5, 10,100], [5,10], [lambda x: 0, lambda x: -x+20, lambda x: 0], 1)

#Cargo a init las dos líneas vacias
line, = ax.plot([], [], lw=2)
line2, = ax.plot([], [], lw=2)
#line3, = ax.plot([], [], lw=2)
#Preparo los valores de la función que se moverá
x_move = movefunction.Xvalues()
y_move = np.flip(movefunction.Yvalues())

#Preparo los valores de la función estática
x_static = staticfunction.Xvalues()
y_static = staticfunction.Yvalues()

# Inicializo el poligono vacío que luego rellenará el area.
polygone = ax.fill_between(x_static[0:0], y_static[0:0], facecolor='yellow', alpha=0.5)
polygone2 = ax.fill_between(x_static[0:0], y_static[0:0], facecolor='yellow', alpha=0.5)

# Integral de Convolucion x[t]*h[t]
dt = 0.01
y_convolve = np.convolve(y_move,y_static,'same')*dt


# Funcion que inicia la animación
def init():
    line.set_data([], [])
    line2.set_data([x_static], [y_static])
    return line, line2, polygone, polygone2

# Función animación, es llamada cíclicamente.

def animate(t):
    global y_static
    global y_move
    global x_move
    global polygone
    #Variable auxiliar que contendrá los valors iniciales de x_move.
    x_move_t = np.copy(x_move)

    # x = xinicial + v*t
    x_move_t = x_move_t + staticfunction.Velocidad()*t

    ax.collections.clear() # Sino no funciona el rellenado correctamente
    
    t_encuentro_maximo_minimo = int((x_static[0]-x_move[-1])/staticfunction.Velocidad())
    t_encuentro_minimo_minimo = int((x_static[0]-x_move[0])/staticfunction.Velocidad())
   

    # Si se encuentran:
    if (t > t_encuentro_maximo_minimo) and (t < t_encuentro_minimo_minimo):
        polygone = ax.fill_between(
            x_static[0:(t-t_encuentro_maximo_minimo)*staticfunction.VelocidadEntera()],
            y_static[0:(t-t_encuentro_maximo_minimo)*staticfunction.VelocidadEntera()],
            facecolor='blue',
            alpha=0.5
        )
        polygone2 = ax.fill_between(
            np.flip(x_move_t)[0:(t-t_encuentro_maximo_minimo)*staticfunction.VelocidadEntera()],
            np.flip(y_move)[0:(t-t_encuentro_maximo_minimo)*staticfunction.VelocidadEntera()],
            facecolor='green',
            alpha=0.5
        )

    if (t > t_encuentro_maximo_minimo) and (t > t_encuentro_minimo_minimo):
        polygone = ax.fill_between(
            x_static[(t-t_encuentro_minimo_minimo)*staticfunction.VelocidadEntera()::],
            y_static[(t-t_encuentro_minimo_minimo)*staticfunction.VelocidadEntera()::],
            facecolor='blue',
            alpha=0.5
        )
        polygone2 = ax.fill_between(
            np.flip(x_move_t)[(t-t_encuentro_minimo_minimo)*staticfunction.VelocidadEntera()::],
            np.flip(y_move)[(t-t_encuentro_minimo_minimo)*staticfunction.VelocidadEntera()::],
            facecolor='green',
            alpha=0.5
        )
                
    line.set_data(x_move_t, y_move)
    return line, line2, polygone, polygone2


# call the animator.  blit=True means only re-draw the parts that have changed.
anim = animation.FuncAnimation(fig, animate, init_func=init,
                               frames=int((round(movefunction.Desplazamiento(XMAX)/staticfunction.Velocidad())))
, interval=10, blit=True)

# save the animation as an mp4.  This requires ffmpeg or mencoder to be
# installed.  The extra_args ensure that the x264 codec is used, so that
# the video can be embedded in html5.  You may need to adjust this for
# your system: for more information, see
# http://matplotlib.sourceforge.net/api/animation_api.html
# anim.save('basic_animation.mp4', fps=300, extra_args=['-vcodec', 'libx264'])

plt.show()
