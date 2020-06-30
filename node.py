import random

from OpenGL.GL import glCallList, glColor3f, glMaterialfv, glMultMatrixf, glPopMatrix, glPushMatrix, GL_EMISSION, GL_FRONT

#from OpenGL.GL import glRotatef#4

import numpy



from primitive import G_OBJ_CUBE, G_OBJ_SPHERE,G_OBJ_CYLINDER,G_OBJ_SNOWFIGURE#3
from aabb import AABB

from transformation import scaling, translation,rotation

import color





class Node(object):

    """ Base class for scene elements """

    def __init__(self):

        self.color_index = random.randint(color.MIN_COLOR, color.MAX_COLOR)

        self.aabb = AABB([0.0, 0.0, 0.0], [0.5, 0.5, 0.5])

        self.translation_matrix = numpy.identity(4)

        self.scaling_matrix = numpy.identity(4)

        self.rotation_matrix = numpy.identity(4)

        self.selected = False



    def render(self):

        """ renders the item to the screen """

        glPushMatrix()

        glMultMatrixf(numpy.transpose(self.translation_matrix))

        glMultMatrixf(self.scaling_matrix)

        glMultMatrixf(self.rotation_matrix)

        cur_color = color.COLORS[self.color_index]

        glColor3f(cur_color[0], cur_color[1], cur_color[2])

        if self.selected:  # emit light if the node is selected

            glMaterialfv(GL_FRONT, GL_EMISSION, [0.3, 0.3, 0.3])

        

        self.render_self()

        if self.selected:

            glMaterialfv(GL_FRONT, GL_EMISSION, [0.0, 0.0, 0.0])

        glPopMatrix()

        #glRotatef(45,0,0,1)
        
        



    def render_self(self):

        raise NotImplementedError("The Abstract Node Class doesn't define 'render_self'")



    def translate(self, x, y, z):

        self.translation_matrix = numpy.dot(self.translation_matrix, translation([x, y, z]))


    def rotate(self,x,y,z,set_angle = True):

        for r in [[x,0,0], [0,y,0],[0,0,z]]:
            
            self.rotation_matrix = numpy.dot(self.rotation_matrix, rotation(*r,set_angle))
            
            
    def scale_init(self, x, y, z):


        self.scaling_matrix = numpy.dot(self.scaling_matrix, scaling([x, y, z]))

        #self.aabb.scale(s)         


    def rotate_color(self, forwards):

        self.color_index += 1 if forwards else -1

        if self.color_index > color.MAX_COLOR:

            self.color_index = color.MIN_COLOR

        if self.color_index < color.MIN_COLOR:

            self.color_index = color.MAX_COLOR



    def scale(self, up,set_scale_z = False,scale_z = 1):

        s =  1.1 if up else 0.9

        self.scaling_matrix = numpy.dot(self.scaling_matrix, scaling([s, s, s]))

        self.aabb.scale(s)



    def pick(self, start, direction, mat):

        """ Return whether or not the ray hits the object

           Consume:  start, direction    the ray to check

                     mat                 the modelview matrix to transform the ray by """



        # transform the modelview matrix by the current translation

        newmat = numpy.dot(numpy.dot(mat, self.translation_matrix), numpy.linalg.inv(self.scaling_matrix))

        results = self.aabb.ray_hit(start, direction, newmat)

        return results



    def select(self, select=None):

        """ Toggles or sets selected state """

        if select is not None:

            self.selected = select

        else:

            self.selected = not self.selected



class Primitive(Node):

    def __init__(self):

        super(Primitive, self).__init__()

        self.call_list = None



    def render_self(self):

        glCallList(self.call_list)







class Sphere(Primitive):

    """ Sphere primitive """

    def __init__(self):

        super(Sphere, self).__init__()

        self.call_list = G_OBJ_SPHERE





class Cube(Primitive):

    """ Cube primitive """

    def __init__(self):

        super(Cube, self).__init__()

        self.call_list = G_OBJ_CUBE

##############################################2
class Cylinder(Primitive):                   #2
                                             #2
    """ Cube primitive """                   #2
                                             #2
    def __init__(self):                      #2
                                             #2
        super(Cylinder, self).__init__()     #2
                                             #2
        self.call_list = G_OBJ_CYLINDER      #2
##############################################2



class HierarchicalNode(Node):

    def __init__(self):

        super(HierarchicalNode, self).__init__()

        self.child_nodes = []



    def render_self(self):

        for child in self.child_nodes:

            child.render()





class SnowFigure(HierarchicalNode):

    def __init__(self):

        super(SnowFigure, self).__init__()

        self.call_list = G_OBJ_SNOWFIGURE

        self.child_nodes = [ Cylinder(), Cylinder()]

        self.child_nodes[0].translate(0, 0, 0)

        self.child_nodes[1].translate(0, 0, 0)

        #self.child_nodes[1].scaling_matrix = numpy.dot(self.scaling_matrix, scaling([0.8, 0.8, 0.8]))

        self.child_nodes[1].rotate(180,0,0)



        for child_node in self.child_nodes:

            child_node.color_index = color.MIN_COLOR

        self.aabb = AABB([0.0, 0.0, 0.0], [0.5, 1.1, 0.5])





