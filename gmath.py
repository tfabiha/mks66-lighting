import math
from display import *


  # IMPORANT NOTE

  # Ambient light is represeneted by a color value

  # Point light sources are 2D arrays of doubles.
  #      - The first index (LOCATION) represents the vector to the light.
  #      - The second index (COLOR) represents the color.

  # Reflection constants (ka, kd, ks) are represened as arrays of
  # doubles (red, green, blue)

AMBIENT = 0
DIFFUSE = 1
SPECULAR = 2
LOCATION = 0
COLOR = 1
SPECULAR_EXP = 4

#lighting functions
def get_lighting(normal, view, ambient, light, areflect, dreflect, sreflect ):
    a = calculate_ambient( ambient, areflect )
    d = calculate_diffuse( light, dreflect, normal )
    s = calculate_specular( light, dreflect, view, normal )

    for i in range(3):
        if d[i] < 0:
            d[i] = 0
        if s[i] < 0:
            s[i] = 0
    
    #print(a)
    #print(d)
    #print(s)
    
    return [ int(a[i] + d[i] + s[i]) for i in range(3) ]
    
def calculate_ambient(alight, areflect):
    x = [ alight[i] * areflect[i] for i in range(3) ]
    print(x)
    return x
    
def calculate_diffuse(light, dreflect, normal):
    #print(light[0])
    #print(normal)
    location = normalize( light[LOCATION] )
    normal = normalize( normal )
    colors = light[COLOR]

    #print(location)
    #print(normal)
    
    const = dot_product( location, normal )
    return [ colors[i] * dreflect[i] * const for i in range(3) ]

def calculate_specular(light, sreflect, view, normal):
    location = normalize( light[LOCATION] )
    normal = normalize( normal )
    view = normalize( view )
    colors = light[COLOR]

    const0 = dot_product( location, normal )
    r = [ 2 * ( normal[i] * const0 ) - location[i] for i in range(3) ]

    return [ colors[i] * sreflect[i] * ( dot_product( r, view ) ** SPECULAR_EXP ) for i in range(3)]
    
def limit_color(color):
    for i in range(color):
        if color[i] < 0:
            color[i] = 0
        if color[i] > 255:
            color[i] = 255
    return color

#vector functions
#normalize vetor, should modify the parameter
def normalize(vector):
    magnitude = math.sqrt( vector[0] * vector[0] +
                           vector[1] * vector[1] +
                           vector[2] * vector[2])
    for i in range(3):
        vector[i] = vector[i] / magnitude

    return vector

#Return the dot porduct of a . b
def dot_product(a, b):
    #print(a)
    #print(b)
    #print("")
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]

#Calculate the surface normal for the triangle whose first
#point is located at index i in polygons
def calculate_normal(polygons, i):

    A = [0, 0, 0]
    B = [0, 0, 0]
    N = [0, 0, 0]

    A[0] = polygons[i+1][0] - polygons[i][0]
    A[1] = polygons[i+1][1] - polygons[i][1]
    A[2] = polygons[i+1][2] - polygons[i][2]

    B[0] = polygons[i+2][0] - polygons[i][0]
    B[1] = polygons[i+2][1] - polygons[i][1]
    B[2] = polygons[i+2][2] - polygons[i][2]

    N[0] = A[1] * B[2] - A[2] * B[1]
    N[1] = A[2] * B[0] - A[0] * B[2]
    N[2] = A[0] * B[1] - A[1] * B[0]

    return N
