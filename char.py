
#coding:utf-8

 

import sys

import time

from math import pi as PI

from math import sin, cos

 

from OpenGL.GL import *

from OpenGL.GLU import *

from OpenGL.GLUT import *

 

 

def Redraw():

	global n,theta,R,k

	glClear(GL_COLOR_BUFFER_BIT)	

						

	if (k==1): 

		glColor3f(1.0,0,0) #设置红色绘图颜色

		k=2

	elif (k==2): 

		glColor3f(0,1.0,0) 

		k=0

	else:

		glColor3f(1.0,1.0,0) 

		k=1

	glLineWidth(1.0)

	glBegin(GL_POLYGON)					#开始绘制六边形	

	for i in range(n):

		glVertex2f( R*cos(theta+i*2*PI/n), R*sin(theta+i*2*PI/n))			

	glEnd()

	glColor3f(0.0,0.0,0)

	glRasterPos2i(-1,0)	#定位当前光标，起始字符位置

	glutBitmapCharacter(GLUT_BITMAP_9_BY_15,ord('C'))	#写字符"C"

	glutBitmapCharacter(GLUT_BITMAP_9_BY_15,ord('l'))	#写字符"l"

	glutBitmapCharacter(GLUT_BITMAP_9_BY_15,ord('o'))	#写字符"o"

	glutBitmapCharacter(GLUT_BITMAP_9_BY_15,ord('c'))	#写字符"c"

	glutBitmapCharacter(GLUT_BITMAP_9_BY_15,ord('K'))	#写字符"k"

	glColor3f(1.0,1.0,1.0) #设置白色绘图颜色

	glLineWidth(3.0)

	# 绘制直线

	glBegin(GL_LINES)

	# 直线第一点坐标

	glVertex3f(0.0, 0.0, 0.0)

	# 直线第二点坐标

	glVertex3f(R*cos(2*PI/n), R*sin(2*PI/n), 0.0)

	# 结束绘制

	glEnd()

 

	glutSwapBuffers()					#双缓冲的刷新模式；

 

#设置渲染状态

def SetupRC():

	glClearColor(0.0, 0.0, 1.0, 1.0)  #背景蓝色

 

#改变窗口大小时调用

def Resize(w,h):

	global n,theta,R

	glMatrixMode(GL_PROJECTION)					#投影矩阵模式

	glLoadIdentity()							#矩阵堆栈清空

	#设置裁剪窗口大小

	glOrtho(-1.5*R*w/h,1.5*R*w/h,-1.5*R,1.5*R, 1.0, -1.0)

 

	glViewport(0, 0, w, h)						#设置视区大小

	glMatrixMode(GL_MODELVIEW)					#模型矩阵模式

 

def myidle():	

	global theta

	theta=theta+2.0 

	if (theta>=2*PI):

		theta=theta-2*PI 

	glutPostRedisplay()	#重画，相当于重新调用Redraw(),改编后的变量得以传给绘制函数

	time.sleep(0.5) 	#延时0.5秒

 

#使用glut初始化OpenGL

glutInit()

glutInitWindowSize(700,700)

#设置显示模式；（注意双缓冲）

glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)

glutCreateWindow("A Rotating Square")

k=0

n=6				#多边形变数

R=10			#外接圆半径

theta=0.0		#旋转初始角度值

#调用函数绘制图像

glutDisplayFunc(Redraw)

glutReshapeFunc(Resize)

glutIdleFunc(myidle)     #注册闲置回调函数

SetupRC()

#主循环

glutMainLoop()
