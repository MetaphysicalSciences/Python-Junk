import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

# Define vertices of a cube
vertices = (
    (1, -1, -1),
    (1, 1, -1),
    (-1, 1, -1),
    (-1, -1, -1),
    (1, -1, 1),
    (1, 1, 1),
    (-1, -1, 1),
    (-1, 1, 1)
)

# Define edges connecting the vertices
edges = (
    (0,1),
    (1,2),
    (2,3),
    (3,0),
    (4,5),
    (5,7),
    (7,6),
    (6,4),
    (0,4),
    (1,5),
    (2,7),
    (3,6)
)

# Define surfaces (faces) for the cube
surfaces = (
    (0,1,2,3),
    (4,5,7,6),
    (0,1,5,4),
    (2,3,6,7),
    (1,2,7,5),
    (0,3,6,4)
)

# Define colors for each face
colors = (
    (1,0,0),  # red
    (0,1,0),  # green
    (0,0,1),  # blue
    (1,1,0),  # yellow
    (1,0,1),  # magenta
    (0,1,1),  # cyan
)

def Cube():
    glBegin(GL_QUADS)
    for i_surface, surface in enumerate(surfaces):
        glColor3fv(colors[i_surface])
        for vertex in surface:
            glVertex3fv(vertices[vertex])
    glEnd()

    glColor3fv((0,0,0))
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()

def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)

    # Set perspective
    gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)

    glTranslatef(0.0, 0.0, -5)  # Move cube away from camera

    clock = pygame.time.Clock()

    angle = 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        angle += 1  # increase rotation angle

        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

        glPushMatrix()
        glRotatef(angle, 1, 1, 1)  # rotate around x,y,z axes
        Cube()
        glPopMatrix()

        pygame.display.flip()
        clock.tick(60)  # Limit to 60 FPS

    pygame.quit()

if __name__ == "__main__":
    main()
