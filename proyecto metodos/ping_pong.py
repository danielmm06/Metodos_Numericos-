import pygame
from pygame.locals import *
import sys, os, traceback
import random
from math import *
import math
import time
import numpy as np
import pylab as pl
import pylab as pl2
#Instancia de las variables globales para su uso en el calculo de regresion lineal 
global tiempoder
global tiempoizq
global velocidadizq
global velocidadder
global aceleracion
global fuerza
global vectorx
#global posicion #15
global posicion1
global posaux1
global posaux2

posaux1=[]
posaux2=[]  #770

cont=0

# declarando que son vectores
fuerza=[]
tiempoder=[]
tiempoizq=[]
velocidadizq=[]
velocidadder=[]
aceleracion=[]
vectorx=[]

if sys.platform == 'win32' or sys.platform == 'win64':
    os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.display.init()
pygame.font.init()
pygame.mixer.init(buffer=0)

screen_size = [800,600]
icon = pygame.Surface((1,1)); icon.set_alpha(0); pygame.display.set_icon(icon)
pygame.display.set_caption("--- Ping Pong --- 2016 --- Metodos Numericos --- ")
surface = pygame.display.set_mode(screen_size)

#declaracion de la ruta de los diferentes sonidos del juego
sounds = {
    "ping" : pygame.mixer.Sound("data/ping.wav"),
    "click" : pygame.mixer.Sound("data/click.wav"),
    "da-ding" : pygame.mixer.Sound("data/da-ding.wav")
}
#dandole el parametro del volumen a los sonidos
sounds["ping"].set_volume(0.05)
sounds["click"].set_volume(0.5)
sounds["da-ding"].set_volume(0.5)

font = {
    18 : pygame.font.SysFont("verdana",18),
    72 : pygame.font.SysFont("Times New Roman",72)
}

def rndint(x):
    return int(round(x))
def clamp(x, minimum,maximum):
    if x < minimum: return minimum
    if x > maximum: return maximum
    return x

#clase de las paletas o raquetas
class Paddle:
    def __init__(self, x,y,w,h, key_l,key_r,key_d,key_u):
        self.pos = [x,y]
        self.dim = [w,h]

        
        self.key_l = key_l
        self.key_r = key_r
        self.key_d = key_d
        self.key_u = key_u
    def move(self, rel_x,rel_y):
        self.pos[0] += dt*rel_x
        self.pos[1] -= dt*rel_y
        self.pos[0] = clamp(self.pos[0],0,screen_size[0]-self.dim[0])
        self.pos[1] = clamp(self.pos[1],0,screen_size[1]-self.dim[1])

    def update(self,key):
        speed = 200
        if self.key_l!=None and key[self.key_l]: self.move(-speed, 0)
        if self.key_r!=None and key[self.key_r]: self.move( speed, 0)
        if self.key_d!=None and key[self.key_d]: self.move( 0,-speed)
        if self.key_u!=None and key[self.key_u]: self.move( 0, speed)

    def draw(self,color):
        pygame.draw.rect(surface,        color,(self.pos[0],self.pos[1],self.dim[0],self.dim[1]),0)
        pygame.draw.rect(surface,(255,255,255),(self.pos[0],self.pos[1],self.dim[0],self.dim[1]),1)

#Clase de los Jugadores
class Player:
    def __init__(self,color,paddles):
        self.score = 0
        self.color = color
        self.paddles = list(paddles)
        
	#Contador de Puntaje
    def add_score(self):
        self.score += 1
        sounds["da-ding"].play()
     	
 
players = [
    Player((0,255,0), [Paddle(               5,   screen_size[1]/2-30,10,60, None,None,   K_s, K_w)]),
    Player((0,0,255), [Paddle(screen_size[0]-5-10,screen_size[1]/2-30,10,60, None,None,K_DOWN,K_UP)])
]
       
class Ball:

    def __init__(self, x,y, speed):
        self.pos = [x,y]
        self.trail = []
        global start 
        start = time.time()
        angle = pi/2 
        while abs(cos(angle)) < 0.1 or abs(cos(angle)) > 0.9:
            angle = radians(random.randint(30,360))
        
        speed =random.uniform(150,250)

        self.speed = [speed*cos(angle),speed*sin(angle)]
        global posicion
        posicion=0
        
        self.radius = 5 # radio de la pelota para hallar masa
        print "--------------"
        print "radio ",self.radius
        area=pi*(self.radius**2)
        print "area ",area
        global masa
        masa=(pi*area*(self.radius**4))/3 #Calculo de la masa basado en el despeje por integrales
        print "masa",masa

    def update(self):
        self.trail = [self.pos + [self.radius]] + self.trail
        while len(self.trail) > 10: self.trail = self.trail[:-1]
        

    def move(self, dt):
        
        self.pos[0] += dt*self.speed[0]
        self.pos[1] += dt*self.speed[1]
        posaux1.append(self.pos[0])
        posaux2.append(self.pos[1])
        if(len(posaux1)>2):
            posaux1.pop(0)
            posaux2.pop(0)
            regresion()
        

    def speed_up(self):
        factor = 1.1
        self.speed[0] *= factor
        self.speed[1] *= factor
        
        end = time.time() #se de tiene el conteo del tiempo, al tocar la bola con la paleta
        temp = end - start #se realiza el calculo, para hallar la duracion de tiempo real. 

        magnitudveloc=sqrt((self.speed[0]**2)+(self.speed[1]**2))  # se halla el vector resultante de velocidad
        velocidadconver=magnitudveloc/100 #se hace ajuste de cm a m en la velocidad
        calculaacelara=velocidadconver/temp #calculo de aceleracion 
        masaconver=masa/1000   #conversion de la masa de g a kg
        calculafuer=masaconver*calculaacelara #calculo fuerza
          # adicion del tiempo al vector respectivo
       	print "posicion: ",self.pos[0]
        if self.pos[0] >14:
        	if self.pos[0] <16:
	        	tiempoizq.append(temp)
	        	velocidadizq.append(velocidadconver)# adicion de la velocidad al vector respectivo
			    
        
        if self.pos[0] >760:
        	if self.pos[0] <790:
		        velocidadder.append(velocidadconver)# adicion de la velocidad al vector respectivo
      			tiempoder.append(temp)

        aceleracion.append(calculaacelara) # adicion de la aceleracion al vector respectivo
        global cont   #instancia de variabale contador para calculo de regresion lineal
        cont+=1     # aumento en contador
        vectorx.append(cont)  #adicion del contador al vectorx
        
        fuerza.append(calculafuer) #adicion del contador al vector respectivo
        #Impresiones en consola, para tener control previo de la informacion del momento
        print 'duracion tiempo:\t{}'.format(temp)
        print "velocidad resutando",velocidadconver
        print "aceleracion",calculaacelara
        print "fuerza",calculafuer
        print "-----------------"
        
         
        #Impresiones en consola de los vectores, para tener control previo de la informacion.    
        print "\nvelocidad vector izq",velocidadizq
        print "\nvelocidad vector derecha",velocidadder
        
        print "\naceleracion vector",aceleracion
        print "\nfuerza vector",fuerza
        #print "valor x: ", vectorx

        
    	
    def draw(self):
        light = 255/10
        for px,py,r in self.trail[::-1]:
            pygame.draw.circle(surface,(light,0,0),list(map(rndint,[px,py])),r)
            light += 255/10
        pygame.draw.circle(surface,(255,255,255),list(map(rndint,self.pos)),self.radius)
balls = []

def regresion():
        
        xi=np.array(posaux1)
        yi=np.array(posaux2)
        n=len(xi)
        mult, sum1, sumax, sumay=0,0,0,0
        for i in range (n):
            sumax+=xi[i]
            sumay+=yi[i]
            mult+=xi[i]*yi[i]
            sum1+=xi[i]**2
        expo=sumax**2
        a1=(n*mult-(sumax*sumay))/(n*sum1-expo)
        xmedia=sumax/n
        ymedia=sumay/n
        a0=ymedia-(a1*xmedia)
        #print "la funcion es:"+str(a0)+"+"+str(a1)+"x"
        for m in range (15,785):
            y=a0+a1*m
            #if(y>485):
                #y=485
            #elif(y<=15):
                #y=15

            pygame.draw.line(surface,(255,0,0),(m,y),(m,y),3)
        pygame.display.update()




def get_input():
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if   event.type == QUIT: return False
        elif event.type == KEYDOWN:
            if   event.key == K_ESCAPE: return False
    for player in players:
        for paddle in player.paddles:
            paddle.update(keys)
    return True
def update():
    for ball in balls:
        ball.update()
between_rounds_timer = 3.0
def move():
    global balls, between_rounds_timer

    balls2 = []
    for ball in balls:
        removed = False
        for substep in range(10): 
            ball.move(dt/10.0)
            
            if ball.pos[0] < 0:
                players[1].add_score()
                removed = True
                break
            elif ball.pos[0] > screen_size[0]:
                players[0].add_score()
                removed = True
                break

            if ball.pos[1] < 0:  #pared superior 
            	
                ball.pos[1] = 0
                ball.speed[1] *= -1
                sounds["ping"].play()

            elif ball.pos[1] > screen_size[1]: #pared inferior
            	ball.pos[1] = screen_size[1]
                ball.speed[1] *= -1
                sounds["ping"].play()

            for player in players:
                for paddle in player.paddles:
                    #Golpe con paletas o raquetas
                    if ball.pos[0] > paddle.pos[0] and ball.pos[0] < paddle.pos[0]+paddle.dim[0] and\
                       ball.pos[1] > paddle.pos[1] and ball.pos[1] < paddle.pos[1]+paddle.dim[1]:
                        dist_lrdu = [
                            ball.pos[0] - paddle.pos[0],
                            (paddle.pos[0]+paddle.dim[0]) - ball.pos[0],
                            (paddle.pos[1]+paddle.dim[1]) - ball.pos[1],
                            ball.pos[1] - paddle.pos[1],
                        ]
                        dist_min = min(dist_lrdu)

                        if   dist_min == dist_lrdu[0]: ball.speed[0] = -abs(ball.speed[0])
                        elif dist_min == dist_lrdu[1]: ball.speed[0] =  abs(ball.speed[0])
                        elif dist_min == dist_lrdu[2]: ball.speed[1] =  abs(ball.speed[1])
                        elif dist_min == dist_lrdu[3]: ball.speed[1] = -abs(ball.speed[1])
                        sounds["click"].play()
                        ball.speed_up()

                        
        if not removed: balls2.append(ball)

    if len(balls2) == 0 and len(balls) > 0: #someone scored the last of the balls
        between_rounds_timer = 3.0

    balls = balls2
    if len(balls) == 0:
        between_rounds_timer -= dt
        if between_rounds_timer < 0:
            balls.append(Ball(screen_size[0]/2,screen_size[1]/2,200.0))
def draw():
    surface.fill((0,0,0))

    for ball in balls:
        ball.draw()
    for player in players:
        for paddle in player.paddles:
            paddle.draw(player.color)
    #Impresion a pantalla de la Puntuacion     
    p1_score_text = font[18].render("Score "+str(players[0].score),True,(255,255,255))
    p2_score_text = font[18].render("Score "+str(players[1].score),True,(255,255,255))
    surface.blit(p1_score_text,(                                         20,20))
    surface.blit(p2_score_text,(screen_size[0]-p2_score_text.get_width()-20,20))


    if between_rounds_timer > 0:
        alpha = between_rounds_timer - int(between_rounds_timer)
        alpha = rndint(255*alpha)


        count = font[72].render(str(int(between_rounds_timer)+1),True,(alpha,alpha,alpha))
        
        sc = 0.5  *  (1.0 + between_rounds_timer-int(between_rounds_timer))
        count = pygame.transform.smoothscale(count,list(map(rndint,[count.get_width()*sc,count.get_height()*sc])))
        
        surface.blit(count,(screen_size[0]/2-count.get_width()/2,screen_size[1]/2-count.get_height()/2))
    
    pygame.display.flip()


 
def main():
    global dt
    dt = 1.0/60.0
    
    clock = pygame.time.Clock()


    while True:
        if not get_input(): break
        update()
        move()
        draw()
        clock.tick(60)
        dt = 1.0/clamp(clock.get_fps(),30,90)
    
    #------CODIGO REGRESION LINEAL-------------
	

    #---------- FIN DEL CODIGO DE REGRESION LINEAL-----------
    print "\n Ahora a Graficar... "

    x= np.array(tiempoder)
    print "\nvector grafica tiempo derecha",x
    y = np.array(velocidadder)
    print "\nvector grafica velocidad derecha",y
    x2= np.array(tiempoizq)
    y2 = np.array(velocidadizq)
    tiempo,ecuacion1,ecuacion2,valores=[],[],[],[]
    n,n2=len(x),len(x2)

    for t in range (1, 16):
        tiempo.append(t)

    def sumProd(vec1,vec2, cont):
        suma1=0
        for i in range(cont):
            suma1+=(vec1[i]*vec2[i])
        return suma1

    def sumXY(vec1,vec2,cont):
        suma2=0
        suma3=0
        for j in range (cont):
            suma2+=vec1[j]
            suma3+=vec2[j]
        producto=suma2*suma3
        return producto

    def sumCuadr(vec1, cont):
        suma4=0
        for k in range(cont):
            suma4+=math.pow(vec1[k],2)
        return suma4

    def cuadrado(vec1, cont):    
        suma5=0
        for l in range(cont):
            suma5+=vec1[l]
        return (math.pow(suma5,2))

    def mediaX(vec1, cont): 
        suma6=0
        for o in range(cont):
            suma6+=vec1[o]
        return (suma6/len(vec1))

    def mediaY(vec2, cont):
        suma7=0
        for m in range(cont):
            suma7+=vec2[m]
        return (suma7/len(vec2))

    def raices(vec1,vec2,cont):
        raiz1=0
        raiz2=0
        sumx=0
        sumcx=0
        sumy=0
        sumcy=0
        for k in range(cont):
            sumx+=math.pow(vec1[k],2)
            sumcx+=vec1[k]
            sumy+=math.pow(vec2[k],2)
            sumcy+=vec2[k]
        raiz1=math.sqrt(((cont*sumx)-(math.pow(sumcx,2))))
        raiz2=math.sqrt(((cont*sumy)-(math.pow(sumcy,2))))
        return (raiz1*raiz2)

    def coeficiente(vec1,vec2,cont):
        r=(((cont*sumProd(vec1,vec2,cont))-sumXY(vec1,vec2,cont))/(raices(vec1,vec2,cont)))
        return (r)

    def error(vec1,vec2,a1,a0,cont):
        sr=0
        for p in range(cont):
            sr+=math.pow(vec2[p]-a0-a1*vec1[p],2)
        syx=math.sqrt(sr/(cont-2))
        return syx
        
    a1A=(n*sumProd(x,y,n)-sumXY(x,y,n))/(n*sumCuadr(x,n)-cuadrado(x,n))
    a0A=mediaY(y,n)-a1A*mediaX(x,n)

    a1B=(n2*sumProd(x2,y2,n2)-sumXY(x2,y2,n2))/(n2*sumCuadr(x2,n2)-cuadrado(x2,n2))
    a0B=mediaY(y2,n2)-a1B*mediaX(x2,n2)

    for w in range (40):
        func1=a0A+(a1A*w)
        ecuacion1.append(func1)
        func2=a0B+(a1B*w)
        ecuacion2.append(func2)
        valores.append(w)
        
   
    
    pl.grid(True)
    pl.axis([0,20,-10,25])
    pl.ylabel('Velocidad')
    pl.xlabel('Tiempo')
    pl.plot(x, y, 'co', label="Puntos Jugador 1")
    pl.plot(valores, ecuacion1, 'm--', linewidth=2.0, label="y=30.391-0.780x")
    pl.legend(loc = 'lower left', numpoints = 2)
    

    pl2.title("Grafica Partida")
    pl2.grid(True)
    pl2.axis([0,23,-10,23])
    pl2.ylabel('Velocidad')
    pl2.xlabel('Tiempo')
    pl2.plot(x2, y2, 'ro', label="Puntos Jugador 2")
    pl2.plot(valores, ecuacion2, 'b--', linewidth=2.0, label="y=27.655-0.683x")
    pl2.legend(loc = 'lower left', numpoints = 2)
    pl2.show()
    pl.show()

    pygame.quit();
    sys.exit()

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        tb = sys.exc_info()[2]
        traceback.print_exception(e.__class__, e, tb)
        pygame.quit()
        input()
        sys.exit()
    

       
