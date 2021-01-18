import pygame, math, time, random
import numpy as np

pygame.init()

white = (255, 255, 255)
black = (0, 0, 0)

#adjusts how coarse or fine the circle/donut looks
theta_iter = 20
phi_iter = 45
#circle radius
d_r = 45
r = 90
#rotation speeds
yaw =   0.004
pitch = 0.04
roll =  0.12

WIDTH = 800
HEIGHT = 600

center_x = 400
center_y = 300

screen = pygame.display.set_mode((WIDTH, HEIGHT))

display_surface = pygame.display.set_mode((WIDTH, HEIGHT))

font = pygame.font.SysFont('Arial', 10, bold=True)

#donut properties
#distance from screen
K = 50
K_z = 225

def project(x, y, z, k=K, kz=K_z):
    #return (x*k/(z + kz), y*k/(z + kz))
    return (x,y)

def illuminate(norm):

    i = random.randrange(6)
    return ".:;-=+*#%@"[i]

def add_text(char, coord):
    t = font.render(str(char), True, white)
    display_surface.blit(t, coord)

#some common trig functions
def sinsin(a, b):
    return math.sin(a)*math.sin(b)

def coscos(a, b):
    return math.cos(a)*math.cos(b)

def sincos(a, b):
    return math.sin(a)*math.cos(b)

def sinsinsin(a,b,c):
    return math.sin(a)*math.sin(b)*math.sin(c)

def sinsincos(a,b,c):
    return math.sin(a)*math.sin(b)*math.cos(c)

def sincoscos(a,b,c):
    return math.sin(a)*math.cos(b)*math.cos(c)

while True:
    alpha, beta, gamma = 0, 0, 0
    while True:
        screen.fill((black))
        #yaw += yaw
        beta += pitch
        gamma += roll
        X, Y, Z = 0, 0, 0
        for i in range(theta_iter):
            theta = 2*math.pi*i/theta_iter
            x, y, z = d_r*math.cos(theta), d_r*math.sin(theta), 0
            x = x + r

            for j in range(phi_iter):
                x_, y_, z_ = x, y, z
                phi = 2*math.pi*j/phi_iter
                x_, y_, z_ = x*math.cos(phi) + z*math.sin(phi), y, -1* x*math.sin(phi) - z*math.cos(phi)

                #Representation of rotation matricies of roll, pitch, and yaw
                X = x_*coscos(alpha, beta) + y_*(sinsincos(gamma, beta, alpha) - sincos(alpha, gamma)) + z_*(sincoscos(beta, alpha, gamma) + sinsin(alpha, gamma))
                Y = x_*sincos(alpha, beta) + y_*(sinsinsin(alpha, beta, gamma) + coscos(alpha, gamma)) + z_*(sinsincos(alpha, beta, gamma) - sincos(gamma, alpha))
                Z = -1*x_*math.sin(beta) + y_*sincos(gamma, beta) + z_*coscos(beta, gamma)
                Y = Y + center_y
                X = X + center_x - r

                #construct normal vector
                #find the 'center' of the taurus 
                int_x, int_y, int_z = r, 0, 0
                int_x, int_y, int_z = int_x*math.cos(phi) + int_z*math.sin(phi), int_y, -1* int_x*math.sin(phi) - int_z*math.cos(phi)

                int_X = int_x*coscos(alpha, beta) + int_y*(sinsincos(gamma, beta, alpha) - sincos(alpha, gamma)) + int_z*(sincoscos(beta, alpha, gamma) + sinsin(alpha, gamma))
                int_Y = int_x*sincos(alpha, beta) + int_y*(sinsinsin(alpha, beta, gamma) + coscos(alpha, gamma)) + int_z*(sinsincos(alpha, beta, gamma) - sincos(gamma, alpha))
                int_Z = -1*int_x*math.sin(beta) + int_y*sincos(gamma, beta) + int_z*coscos(beta, gamma)

                int_Y = int_Y + center_y
                int_X = int_X + center_x - r

                #subtracting the point from the center will give us the surface normal
                surface_norm = np.array([X - int_X, Y - int_Y, Z - int_Z])
                #lighting direction  (arboitrary)
                light_dir = np.array([1, -1, 0])
                cos_theta = np.dot(surface_norm, light_dir)/(np.linalg.norm(surface_norm)*np.linalg.norm(light_dir))
                #this is a number between -1 and 1 so we can convert to 0 - 9
                luminance = cos_theta*5 + 5
                luminance = int(luminance)

                add_text(".:;-=+*#%@"[luminance], project(X, Y, Z))
        time.sleep(.050)
        pygame.display.update()
