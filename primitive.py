from OpenGL.GL import glBegin, glColor3f, glEnd, glEndList, glLineWidth, glNewList, glNormal3f, glVertex3f, GL_COMPILE, GL_LINES, GL_QUADS,GL_TRIANGLE_STRIP

from OpenGL.GLU import gluDeleteQuadric, gluNewQuadric, gluSphere, gluCylinder


G_OBJ_PLANE = 1

G_OBJ_SPHERE = 2

G_OBJ_CUBE = 3
#######################2
G_OBJ_CYLINDER = 4    #2
#######################2

G_OBJ_SNOWFIGURE = 5 #3






def make_plane():

    glNewList(G_OBJ_PLANE, GL_COMPILE)

    glBegin(GL_LINES)

    glColor3f(0, 0, 0)

    for i in range(41):

        glVertex3f(-10.0 + 0.5 * i, 0, -10)

        glVertex3f(-10.0 + 0.5 * i, 0, 10)

        glVertex3f(-10.0, 0, -10 + 0.5 * i)

        glVertex3f(10.0, 0, -10 + 0.5 * i)



    # Axes

    glEnd()

    glLineWidth(5)



    glBegin(GL_LINES)

    glColor3f(0.5, 0.7, 0.5)

    glVertex3f(0.0, 0.0, 0.0)

    glVertex3f(5, 0.0, 0.0)

    glEnd()



    glBegin(GL_LINES)

    glColor3f(0.5, 0.7, 0.5)

    glVertex3f(0.0, 0.0, 0.0)

    glVertex3f(0.0, 5, 0.0)

    glEnd()



    glBegin(GL_LINES)

    glColor3f(0.5, 0.7, 0.5)

    glVertex3f(0.0, 0.0, 0.0)

    glVertex3f(0.0, 0.0, 5)

    glEnd()



    # Draw the Y.

    glBegin(GL_LINES)

    glColor3f(0.0, 0.0, 0.0)

    glVertex3f(0.0, 5.0, 0.0)

    glVertex3f(0.0, 5.5, 0.0)

    glVertex3f(0.0, 5.5, 0.0)

    glVertex3f(-0.5, 6.0, 0.0)

    glVertex3f(0.0, 5.5, 0.0)

    glVertex3f(0.5, 6.0, 0.0)



    # Draw the Z.

    glVertex3f(-0.5, 0.0, 5.0)

    glVertex3f(0.5, 0.0, 5.0)

    glVertex3f(0.5, 0.0, 5.0)

    glVertex3f(-0.5, 0.0, 6.0)

    glVertex3f(-0.5, 0.0, 6.0)

    glVertex3f(0.5, 0.0, 6.0)



    # Draw the X.

    glVertex3f(5.0, 0.0, 0.5)

    glVertex3f(6.0, 0.0, -0.5)

    glVertex3f(5.0, 0.0, -0.5)

    glVertex3f(6.0, 0.0, 0.5)



    glEnd()

    glLineWidth(1)

    glEndList()





def make_sphere():

    glNewList(G_OBJ_SPHERE, GL_COMPILE)

    quad = gluNewQuadric()

    gluSphere(quad, 0.5, 30, 30)

    gluDeleteQuadric(quad)

    glEndList()





def make_cube():

    glNewList(G_OBJ_CUBE, GL_COMPILE)

    vertices = [((-0.5, -0.5, -0.5), (-0.5, -0.5, 0.5), (-0.5, 0.5, 0.5), (-0.5, 0.5, -0.5)),

                ((-0.5, -0.5, -0.5), (-0.5, 0.5, -0.5), (0.5, 0.5, -0.5), (0.5, -0.5, -0.5)),

                ((0.5, -0.5, -0.5), (0.5, 0.5, -0.5), (0.5, 0.5, 0.5), (0.5, -0.5, 0.5)),

                ((-0.5, -0.5, 0.5), (0.5, -0.5, 0.5), (0.5, 0.5, 0.5), (-0.5, 0.5, 0.5)),

                ((-0.5, -0.5, 0.5), (-0.5, -0.5, -0.5), (0.5, -0.5, -0.5), (0.5, -0.5, 0.5)),

                ((-0.5, 0.5, -0.5), (-0.5, 0.5, 0.5), (0.5, 0.5, 0.5), (0.5, 0.5, -0.5))]

    normals = [(-1.0, 0.0, 0.0), (0.0, 0.0, -1.0), (1.0, 0.0, 0.0), (0.0, 0.0, 1.0), (0.0, -1.0, 0.0), (0.0, 1.0, 0.0)]



    glBegin(GL_QUADS)

    for i in range(6):

        glNormal3f(normals[i][0], normals[i][1], normals[i][2])

        for j in range(4):

            glVertex3f(vertices[i][j][0], vertices[i][j][1], vertices[i][j][2])

    glEnd()

    glEndList()

#####################################################################2
                                                                    #2
def make_Cylinder():                                                #2
    #glNewList(G_OBJ_PLANE, GL_COMPILE)                             #2
    #glLineWidth(50.0)                                              #2
    #glColor3f(0.0, 0.0, 0.0)                                       #2
    #glBegin(GL_LINES)                                              #2 
    #glVertex3f(1.0, 0.0, 0.0)                                      #2
    #glVertex3f(0.0, 1.0, 0.0)                                      #2
    #glEnd()                                                        #2
                                                                    #2
    #glColor3f(1.0, 0.0, 0.0)                                       #2
    #glBegin(GL_TRIANGLE_STRIP)                                     #2
    #glVertex3f(1.000000 ,0.000000, 0.000000)
    #glVertex3f(0.000000, 1.000000, 0.000000)
    #glVertex3f(1.000000, 1.000000, 1.000000)
    #glEnd()

    glNewList(G_OBJ_CYLINDER, GL_COMPILE)

    quad = gluNewQuadric()
    

    gluCylinder(quad, 0.2,0.2,2.0,32,32)#半径半径长切分次数切分次数

    #glRotatef(2, 0, 0, 1)

    gluDeleteQuadric(quad)
    
    glEndList()                                                     #2
                                                                    #2
                                                                    #2
#####################################################################2
def init_primitives():

    make_plane()

    make_sphere()

    make_cube()
#######################2
    make_Cylinder()   #2
#######################2
