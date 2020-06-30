import numpy

from math import pi ,cos,sin



def translation(displacement):

    t = numpy.identity(4)

    t[0, 3] = displacement[0]

    t[1, 3] = displacement[1]

    t[2, 3] = displacement[2]

    return t





def scaling(scale):

    s = numpy.identity(4)

    s[0, 0] = scale[0]

    s[1, 1] = scale[1]

    s[2, 2] = scale[2]

    s[3, 3] = 1

    return s


def rotation(x,y,z,set_angle=True):

    r = numpy.identity(4)

    if x !=0:

        if set_angle==True:
        
            theta = (x*pi)/180
            
        if set_angle==False:
            
            theta = x
            

        r[1, 1] =  cos(theta)

        r[1, 2] =  sin(theta)
        
        r[2, 1] = -sin(theta)
        
        r[2, 2] =  cos(theta)



    if y !=0:

        
        
        if set_angle==True:
        
            theta = (y*pi)/180
            
        if set_angle==False:
            
            theta = y

        r[0, 0] =  cos(theta)

        r[0, 2] = -sin(theta)
        
        r[2, 0] = sin(theta)
        
        r[2, 2] =  cos(theta)




    if z !=0:
        
        if set_angle==True:
        
            theta = (z*pi)/180
            
        if set_angle==False:
            
            theta = z

        r[0, 0] =  cos(theta)

        r[0, 1] =  sin(theta)

        r[1, 0] =  -sin(theta)

        r[1, 1] =  cos(theta)



    return r
