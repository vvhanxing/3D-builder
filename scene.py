import sys

import numpy

from node import Sphere, Cube, SnowFigure ,Cylinder#

import math 





class Scene(object):



    # the default depth from the camera to place an object at

    PLACE_DEPTH = 15.0



    def __init__(self):

        # The scene keeps a list of nodes that are displayed

        self.node_list = list()

        self.selected_node_list = list(["None"])#3

        # Keep track of the currently selected node.

        # Actions may depend on whether or not something is selected

        self.selected_node = None



    def add_node(self, node):

        """ Add a new node to the scene """

        self.node_list.append(node)

#####################################################
                                                    #
    def remove_node(self, node):                    # 
                                                    #
        """ Remove selected node in the scene """   #
                                                    #
        #print(self.node_list)                      # 
                                                    #
        if node in self.node_list:                  #    
                                                    #
            self.node_list.remove(node)             #
                                                    #
#####################################################


#####################################################
                                                    #
    def rotate_node(self, node,up):                 # 
                                                    #
        """ Remove selected node in the scene """   #
                                                    #
        #print(self.node_list)

        if up =="x":                                        # 
                                                            #
            node.rotate(10,0,0)
        if up =="-x":
            node.rotate(-10,0,0)
        if up =="y":                                        # 
                                                            #
            node.rotate(0,10,0)
        if up =="-y":
            node.rotate(0,-10,0)

        if up =="z":                                        # 
                                                            #
            node.rotate(0,0,10)
        if up =="-z":
            node.rotate(0,0,-10)#
#####################################################                                            

    def render(self):

        """ Render the scene. This function simply calls the render function for each node. """

        for node in self.node_list:

            node.render()



    def pick(self, start, direction, mat):

        """ Execute selection.

            Consume: start, direction describing a Ray

                     mat              is the inverse of the current modelview matrix for the scene """

        if self.selected_node is not None:

            self.selected_node.select(False)

            self.selected_node = None



        # Keep track of the closest hit.

        mindist = sys.maxsize

        closest_node = None

        for node in self.node_list:

            hit, distance = node.pick(start, direction, mat)

            if hit and distance < mindist:

                mindist, closest_node = distance, node

                if node != self.selected_node_list[len(self.selected_node_list)-1]:#3

                    self.selected_node_list.append(node)#3

                #print(self.selected_node_list)#3



        # If we hit something, keep track of it.

        if closest_node is not None:

            closest_node.select()

            closest_node.depth = mindist

            closest_node.selected_loc = start + direction * mindist

            self.selected_node = closest_node



    def move_selected(self, start, direction, inv_modelview):

        """ Move the selected node, if there is one.

            Consume:  start, direction  describes the Ray to move to

                      inv_modelview     is the inverse modelview matrix for the scene """

        if self.selected_node is None: return



        # Find the current depth and location of the selected node

        node = self.selected_node

        depth = node.depth

        oldloc = node.selected_loc

        #print(oldloc)



        # The new location of the node is the same depth along the new ray

        newloc = (start + direction * depth)



        # transform the translation with the modelview matrix

        translation = newloc - oldloc

        pre_tran = numpy.array([translation[0], translation[1], translation[2], 0])

        translation = inv_modelview.dot(pre_tran)



        # translate the node and track its location

        node.translate(translation[0], translation[1], translation[2])

        node.selected_loc = newloc



    def place(self, shape, start, direction, inv_modelview):

        """ Place a new node.

            Consume:  shape             the shape to add

                      start, direction  describes the Ray to move to

                      inv_modelview     is the inverse modelview matrix for the scene """

        new_node = None

        if shape == 'sphere': new_node = Sphere()

        elif shape == 'cube': new_node = Cube()

        elif shape == 'cylinder': new_node = Cylinder()

        elif shape == 'figure': new_node = SnowFigure()



        self.add_node(new_node)

        if new_node.call_list!=5:


            #print(dir(new_node),new_node.call_list)
            # place the node at the cursor in camera-space

            translation = (start + direction * self.PLACE_DEPTH)



            # convert the translation to world-space

            pre_tran = numpy.array([translation[0], translation[1], translation[2], 1])

            translation = inv_modelview.dot(pre_tran)



            new_node.translate(translation[0], translation[1], translation[2])


        if new_node.call_list==5 and len(self.selected_node_list)>2:
            
            #print(dir(new_node),new_node.call_list)
            # place the node at the cursor in camera-space

            translation = (start + direction * self.PLACE_DEPTH)



            # convert the translation to world-space

            pre_tran = numpy.array([translation[0], translation[1], translation[2], 1])

            translation = inv_modelview.dot(pre_tran)

            #print(self.selected_node_list[-1].translate)
            #print(self.selected_node_list[-2].translation_matrix)
            
            center_x = (self.selected_node_list[-2].translation_matrix[0,3]+self.selected_node_list[-1].translation_matrix[0,3])/2

            center_y = (self.selected_node_list[-2].translation_matrix[1,3]+self.selected_node_list[-1].translation_matrix[1,3])/2

            center_z = (self.selected_node_list[-2].translation_matrix[2,3]+self.selected_node_list[-1].translation_matrix[2,3])/2

            new_node.translate(center_x, center_y, center_z)

            direction_x = (self.selected_node_list[-2].translation_matrix[0,3]-self.selected_node_list[-1].translation_matrix[0,3])
            
            direction_y = (self.selected_node_list[-2].translation_matrix[1,3]-self.selected_node_list[-1].translation_matrix[1,3])
            
            direction_z = (self.selected_node_list[-2].translation_matrix[2,3]-self.selected_node_list[-1].translation_matrix[2,3])


            
            if math.fabs(direction_z)>2:

                new_node.rotate( math.atan(direction_z/direction_y)+math.pi/2, math.atan(direction_x/direction_z) ,0,False)

                


            elif math.fabs(direction_y)>2:

                new_node.rotate(90,0,0)
                
                new_node.rotate( math.atan(direction_y/direction_z)+math.pi/2, math.atan(direction_x/direction_y) ,0,False)

                

            elif math.fabs(direction_x)>2:

                new_node.rotate(0,90,0)
                
                new_node.rotate( math.atan(direction_x/direction_z)+math.pi/2, math.atan(direction_y/direction_x) ,0,False)


                

            print(math.atan(direction_z/direction_y)*180/math.pi, math.atan(direction_x/direction_z)*180/math.pi )










                
            #print("1",math.atan(direction_z/direction_y)*(180/math.pi),math.atan(direction_x/direction_z)*(180/math.pi))
            
            print("2",direction_z/direction_y,direction_x/direction_z)

            print("3",direction_z,direction_y,direction_x,direction_z)
            
            
        



    def rotate_selected_color(self, forwards):

        """ Rotate the color of the currently selected node """

        if self.selected_node is None: return

        self.selected_node.rotate_color(forwards)



    def scale_selected(self, up):

        """ Scale the current selection """

        if self.selected_node is None: return

        self.selected_node.scale(up)


############################################################
    def remove_selected(self, up):                         # 
                                                           #
        """ Remove the current selection """               #
                                                           #
        if self.selected_node is None: return              #
                                                           #
                                                           #
        self.remove_node(self.selected_node  )             #
                                                           #
############################################################

############################################################
    def rotate_selected(self, up):                         # 
                                                           #
        """ Remove the current selection """               #
                                                           #
        if self.selected_node is None: return              #
                                                           #
                                                           #
        self.rotate_node(self.selected_node ,up )          #
                                                           #
############################################################
