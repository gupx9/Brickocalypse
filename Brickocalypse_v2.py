from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import * #for utilities like gluPerspective() and gluSphere()
from OpenGL.GLUT import GLUT_BITMAP_HELVETICA_18
import math
import random
import time

# Camera-related variables
camera_pos = (0, 500, 600) # start 500 units away along  +Y,+Z,

# x = 0 → camera is centered horizontally ___
# y = 500 → camera is 500 units towards me
# z = 500 → camera is 500 units "up" __I__

screen_width = 1200
screen_height = 700
fovY = 120  #Field Of View, in degrees.
GRID_LENGTH = 800  # full length of grid lines along each axis (1000 in neg,0,100 in pos)
cells = 15
cell_size = GRID_LENGTH*2 / cells #one side / a

#main_char
scale_factor = 1
player_x = 0
player_y = 0
player_z = 0
move_speed = 40
player_angle = 0
life = 5
score = 0
missed_bullets = 0

fpp = False
game_over = False
cam_rotate = True
rotation_speed = 0.5

#enemy
enemy_scale_factor = 1.5
enemy_count = 5
enemy_li = []
enemy_speed = 0.05

#bullet
bullet_li = []
bullet_speed = 5
max_bullets = 30
last_shot_time = 0

# ===================== NEW GLOBALS =====================
tower_height = 0
target_height = 12  # win condition

brick_li = []   # scattered tower pieces
powerup_li = [] # scattered powerups
last_powerup_time = 0
day_night = "day"
last_day_switch = time.time()

# apply player modifiers
player_boost_speed = False
boost_end_time = 0


def draw_text(x, y, text, font=GLUT_BITMAP_HELVETICA_18): #draws 2D text on the screen

    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    # Set up an orthographic projection that matches window 
    # kottuk jaygay akbo, canvas 
    # Sets coordinates so (0,0) is center of the window
    gluOrtho2D(-screen_width/2, screen_width/2, -screen_height/2, screen_height/2) # left, right, bottom, top
    #changing to 2d to draw text

    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()

    glColor3f(1,1,1)
    #position from where text will start showing
    glRasterPos2f(x,y)
    
    for ch in text:
        glutBitmapCharacter(font, ord(ch))

    #Restore projection and modelview matrices (back to 3D)
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

def main_char():
    global player_x, player_y, player_z, player_angle, scale_factor
    glPushMatrix()
    glTranslatef(player_x, player_y, player_z)
    if game_over:
        glRotatef(-90, 1, 0, 0)


    glRotatef(180, 0, 0, 1)
    glRotatef(player_angle, 0, 0, 1)

    #___leg___
    glColor3f(0,0,1)
    #right leg
    glPushMatrix()
    glTranslatef(-10*scale_factor, 0, 0) #move right
    gluCylinder(gluNewQuadric(), 1*scale_factor, 10*scale_factor, 80*scale_factor, 10, 10)
    glPopMatrix()
    #left leg
    glPushMatrix()
    glTranslatef(10*scale_factor, 0, 0) #move left
    gluCylinder(gluNewQuadric(), 1*scale_factor, 10*scale_factor, 80*scale_factor, 10, 10)
    glPopMatrix()

    #___body___
    glColor3f(0.25, 0.35, 0.10)
    glPushMatrix()
    glTranslatef(0, 0, 100*scale_factor) #over legs
    glScalef(1.75*scale_factor, 1*scale_factor, 3*scale_factor)
    glutSolidCube(23)
    glPopMatrix()

    #___head___
    glColor3f(0.0, 0.0, 0.0)
    glPushMatrix()
    glTranslatef(0, 0, 145*scale_factor) #over body
    gluSphere(gluNewQuadric(), 30, 10, 10)
    glPopMatrix()

    #___arms___
    glColor3f(0.82, 0.70, 0.55)
    #right arm
    glPushMatrix()
    glTranslatef(-17*scale_factor, 65*scale_factor, 125*scale_factor)
    glRotatef(90, 1, 0, 0)
    gluCylinder(gluNewQuadric(), 3*scale_factor, 8*scale_factor, 65*scale_factor, 10, 10)
    glPopMatrix()
    #left arm
    glPushMatrix()
    glTranslatef(17* scale_factor, 65*scale_factor, 125*scale_factor)
    glRotatef(90, 1, 0, 0)
    gluCylinder(gluNewQuadric(), 3*scale_factor, 8*scale_factor, 65*scale_factor, 10, 10)
    glPopMatrix()

    #___gun___
    glColor3f(0.5, 0.5, 0.5)
    glPushMatrix()
    glTranslatef(0, 100*scale_factor, 125*scale_factor)
    glRotatef(90, 1, 0, 0)
    gluCylinder(gluNewQuadric(), 1*scale_factor, 10*scale_factor, 100*scale_factor, 10, 10)
    glPopMatrix()

    glPopMatrix()

def main_chr_with_samller_head():
    global player_x, player_y, player_z, player_angle, scale_factor
    glPushMatrix()
    glTranslatef(player_x, player_y, player_z)
    glRotatef(180, 0, 0, 1)
    glRotatef(player_angle, 0, 0, 1)

    #___leg___
    glColor3f(0,0,1)
    #right leg
    glPushMatrix()
    glTranslatef(-10*scale_factor, 0, 0) #move right
    gluCylinder(gluNewQuadric(), 1*scale_factor, 10*scale_factor, 80*scale_factor, 10, 10)
    glPopMatrix()
    #left leg
    glPushMatrix()
    glTranslatef(10*scale_factor, 0, 0) #move left
    gluCylinder(gluNewQuadric(), 1*scale_factor, 10*scale_factor, 80*scale_factor, 10, 10)
    glPopMatrix()

    #___body___
    glColor3f(0.25, 0.35, 0.10)
    glPushMatrix()
    glTranslatef(0, 0, 100*scale_factor) #over legs
    glScalef(1.75*scale_factor, 1*scale_factor, 3*scale_factor)
    glutSolidCube(23)
    glPopMatrix()

    #___head___
    glColor3f(0.0, 0.0, 0.0)
    glPushMatrix()
    glTranslatef(0, 0, 145*scale_factor) #over body
    gluSphere(gluNewQuadric(), 10, 10, 10)
    glPopMatrix()

    #___arms___
    glColor3f(0.82, 0.70, 0.55)
    #right arm
    glPushMatrix()
    glTranslatef(-17*scale_factor, 65*scale_factor, 125*scale_factor)
    glRotatef(90, 1, 0, 0)
    gluCylinder(gluNewQuadric(), 3*scale_factor, 8*scale_factor, 65*scale_factor, 10, 10)
    glPopMatrix()
    #left arm
    glPushMatrix()
    glTranslatef(17* scale_factor, 65*scale_factor, 125*scale_factor)
    glRotatef(90, 1, 0, 0)
    gluCylinder(gluNewQuadric(), 3*scale_factor, 8*scale_factor, 65*scale_factor, 10, 10)
    glPopMatrix()

    #___gun___
    glColor3f(0.5, 0.5, 0.5)
    glPushMatrix()
    glTranslatef(0, 100*scale_factor, 125*scale_factor)
    glRotatef(90, 1, 0, 0)
    gluCylinder(gluNewQuadric(), 1*scale_factor, 10*scale_factor, 100*scale_factor, 10, 10)
    glPopMatrix()

    glPopMatrix()

def make_bricks():
    global brick_li
    brick_li = []
    for i in range(10): # scatter 10 bricks
        brick_li.append({"x": random.randint(-GRID_LENGTH+100, GRID_LENGTH-100),
                         "y": random.randint(-GRID_LENGTH+100, GRID_LENGTH-100),
                         "z": 0, "collected": False})
def draw_bricks():
    global brick_li
    glColor3f(0.8, 0.3, 0.1) # brown bricks
    for b in brick_li:
        if not b["collected"]:
            glPushMatrix()
            glTranslatef(b["x"], b["y"], b["z"]+20)
            glutSolidCube(30)
            glPopMatrix()
def check_brick_collection():
    global brick_li, tower_height
    for b in brick_li:
        if not b["collected"]:
            dist = math.sqrt((player_x-b["x"])**2+(player_y-b["y"])**2)
            if dist < 40:
                b["collected"] = True
                # player returns to center to place
    if player_x**2 + player_y**2 < 80**2:  # near tower center
        for b in brick_li:
            if b["collected"]:
                tower_height += 1
                b["collected"] = False

def make_enemy():
    global enemy_li, tower_height
    enemy_li=[]
    for i in range(enemy_count):
        t = "normal"
        if tower_height >= 8:
            t = random.choice(["normal","fast","tank"])
        elif tower_height >= 4:
            t = random.choice(["normal","fast"])
        enemy_li.append({"x":random.randint(-GRID_LENGTH, GRID_LENGTH),
                         "y": random.randint(-GRID_LENGTH, GRID_LENGTH),
                         "z":0, "alive":True, "type":t})

def draw_enemy():
    global enemy_scale_factor, enemy_li
    for enemy in enemy_li:
        if enemy["alive"] == False:
            continue

        #enemy size change
        scale = enemy_scale_factor * (1+ 0.2*math.sin(time.time()*2.5 ))
        glPushMatrix()
        glTranslatef(enemy["x"], enemy["y"], enemy["z"])

        #___body___
        glColor3f(1.0, 0.0, 0.0)
        glPushMatrix()
        glTranslatef(0, 300, 50*scale)
        gluSphere(gluNewQuadric(), 50*scale, 20, 20)
        glPopMatrix()

        #___head___
        glColor3f(0.0, 0.0, 0.0)
        glPushMatrix()
        glTranslatef(0, 280, 120*scale) #over body
        gluSphere(gluNewQuadric(), 15*scale, 20, 20)
        glPopMatrix()

        glPopMatrix()
def draw_tower():
    global tower_height
    glColor3f(0.5,0.3,0.7)
    for i in range(tower_height):
        glPushMatrix()
        glTranslatef(0,0,i*50)
        glutSolidCube(50)
        glPopMatrix()
def make_powerup():
    global powerup_li, last_powerup_time
    now = time.time()
    if now - last_powerup_time > 10:
        last_powerup_time = now
        p = random.choice(["speed","ammo","slow"])
        powerup_li.append({"x":random.randint(-GRID_LENGTH,GRID_LENGTH),
                           "y":random.randint(-GRID_LENGTH,GRID_LENGTH),
                           "z":0,"type":p})
def draw_powerups():
    global powerup_li
    for p in powerup_li:
        if p["type"]=="speed": glColor3f(0,1,0)
        if p["type"]=="ammo": glColor3f(1,1,0)
        if p["type"]=="slow": glColor3f(0,0,1)
        glPushMatrix()
        glTranslatef(p["x"],p["y"],p["z"]+20)
        glutSolidCube(20)
        glPopMatrix()

def check_powerup_collection():
    global powerup_li, player_boost_speed, boost_end_time, bullet_speed, enemy_speed
    for p in powerup_li.copy():
        dist = math.sqrt((player_x-p["x"])**2+(player_y-p["y"])**2)
        if dist<40:
            if p["type"]=="speed":
                player_boost_speed = True
                boost_end_time = time.time()+5
            if p["type"]=="ammo":
                bullet_speed *= 2
                boost_end_time = time.time()+5
            if p["type"]=="slow":
                enemy_speed *= 0.5
                boost_end_time = time.time()+5
            powerup_li.remove(p)

def draw_bullets():
    global bullet_li
    glColor3f(1, 1, 0)  #yellow bullets
    for bullet in bullet_li:
        glPushMatrix()
        glTranslatef(bullet["x"], bullet["y"], bullet["z"])
        glutSolidCube(10)
        glPopMatrix()

def draw_shapes():
    global fpp
    # +x is left, -x is right
    # +y is is towards me, -y is away from me
    # +z is up, -z is down
    if not fpp:
        main_char()
    if fpp:
        main_chr_with_samller_head()
 
    draw_enemy()
    draw_bullets()

def shoot_bullet():
    global bullet_li

    if len(bullet_li) >= max_bullets:
        return
    
    #bullet direction based on player angle, basically angular vector direction
    dx = math.sin(math.radians(player_angle)) #as + is left,flip
    dy = -math.cos(math.radians(player_angle)) #as +y is down,flip
    dz = 0
    
    #Start bullet at gun position
    bullet_li.append({"x":player_x, "y":player_y, "z":player_z + 125*scale_factor, "dx":dx, "dy":dy, "dz":dz, "distance":0})


def animate():
    global bullet_li, enemy_li, score, life, missed_bullets, enemy_speed, game_over,player_boost_speed, boost_end_time, bullet_speed,tower_height
    if game_over:
        return
    

    #bullet movement
    for bullet_dict in bullet_li.copy():
        bullet_dict["x"] += bullet_dict["dx"]*bullet_speed
        bullet_dict["y"] += bullet_dict["dy"]*bullet_speed
        bullet_dict["z"] += bullet_dict["dz"]*bullet_speed
        bullet_dict["distance"] += bullet_speed
        
        #check missed bullets (if goes beyond max boundary)
        if bullet_dict["distance"] >= GRID_LENGTH:
            bullet_li.remove(bullet_dict)
            missed_bullets += 1
            continue
        
        #bullet collision check
        for enemy in enemy_li:
            if enemy["alive"] == False and game_over == True:
                continue
            distance = math.sqrt((bullet_dict["x"]-enemy["x"])**2 + (bullet_dict["y"]-(enemy["y"]+300))**2 +(bullet_dict["z"]-(enemy["z"]+50))**2)
            
            if distance < 100:  #collision radius
                if bullet_dict in bullet_li:
                    bullet_li.remove(bullet_dict)
                score += 1
                enemy["x"] = random.randint(-GRID_LENGTH+100, GRID_LENGTH-100)
                enemy["y"] = random.randint(-GRID_LENGTH+100, GRID_LENGTH-100)
                enemy["z"] = 0
                enemy["alive"] = True
                break

    if player_boost_speed and time.time()>boost_end_time:
        player_boost_speed=False
    if bullet_speed>5 and time.time()>boost_end_time:
        bullet_speed=5
    if enemy_speed<0.05 and time.time()>boost_end_time:
        enemy_speed=0.05

    #move enemies toward player
    for enemy in enemy_li:
        if enemy["alive"] == False:
            continue
        #enemy at center so
        enemy_center_x = enemy["x"]
        enemy_center_y = enemy["y"] + 300
        enemy_center_z = enemy["z"] + 50*enemy_scale_factor
        #player center-enemy center
        dx = player_x - enemy_center_x
        dy = player_y - enemy_center_y
        dz = player_z - enemy_center_z
        #eucledian dist
        dist = math.sqrt(dx*dx + dy*dy + dz*dz)

        spd = enemy_speed
        if enemy["type"]=="fast":
            spd *= 2
        if enemy["type"]=="tank":
            spd *= 0.5
        enemy["x"] += (dx/dist) * spd
        enemy["y"] += (dy/dist) * spd
            

        #enemy-player collision check
        if dist < 150: #hit
            life -= 1
            if life <= 0:
                game_over = True
            enemy["alive"] = False
            #respawn if hit
            enemy["x"] = random.randint(-GRID_LENGTH+100, GRID_LENGTH-100)
            enemy["y"] = random.randint(-GRID_LENGTH+100, GRID_LENGTH-100)
            enemy["z"] = 0

        # enemy-tower collision
        if abs(enemy_center_x) < 50 and abs(enemy_center_y) < 50:
            if enemy["type"] == "tank":
                tower_height = max(0, tower_height - 4)
            else:
                tower_height = max(0, tower_height - 1)

            enemy["alive"] = False
            if tower_height <= 0:
                game_over = True
    if tower_height >= target_height:
        game_over = True
        print("🎉 You Win! Tower Completed.")


def keyboardListener(key, x, y):
    global player_x, player_y, player_z, player_angle, GRID_LENGTH, life, score, bullet_li, missed_bullets, game_over, cam_rotate
    global tower_height,brick_li,powerup_li
    
    if key == b'w' and game_over == False:  #forward in facing direction
        player_x += move_speed*math.sin(math.radians(player_angle))
        player_y -= move_speed*math.cos(math.radians(player_angle))

    elif key == b's' and game_over == False:  #backward
        player_x -= move_speed*math.sin(math.radians(player_angle))
        player_y += move_speed*math.cos(math.radians(player_angle))

    elif key == b'a' and game_over == False:  #rotate left
        player_angle += 10
        if player_angle >= 360:
            player_angle -= 360 #resets to 0

    elif key == b'd' and game_over == False:  #rotate right
        player_angle -= 10
        if player_angle < 0:
            player_angle += 360 #same

    if key == b'r':  #restart
        life = 5
        score = 0
        missed_bullets = 0
        bullet_li = []
        game_over = False
        make_enemy()   #respawn
        tower_height = 0
        brick_li = []
        powerup_li = []
        make_bricks()
        player_x, player_y, player_z, player_angle = 0, 0, 0, 0


    #keep player within boundary (based on feet movementa)
    if player_x < -GRID_LENGTH:
        player_x = -GRID_LENGTH
    if player_x > GRID_LENGTH:
        player_x = GRID_LENGTH
    if player_y < -GRID_LENGTH:
        player_y = -GRID_LENGTH
    if player_y > GRID_LENGTH:
        player_y = GRID_LENGTH


    glutPostRedisplay()



def specialKeyListener(key, x, y):
    """
    Handles special key inputs (arrow keys) for adjusting the camera angle and height.
    """
    global camera_pos
    x, y, z = camera_pos

    # Move camera up (UP arrow key)
    if key == GLUT_KEY_UP:
        y -= 10

    # # Move camera down (DOWN arrow key)
    if key == GLUT_KEY_DOWN:
        y += 10

    # moving camera left (LEFT arrow key)
    if key == GLUT_KEY_LEFT:
        x += 10  

    # moving camera right (RIGHT arrow key)
    if key == GLUT_KEY_RIGHT:
        x -= 10  


    camera_pos = (x, y, z)


def mouseListener(button, state, x, y):
    global fpp
    """
    Handles mouse inputs for firing bullets (left click) and toggling camera mode (right click).
    """
    # # Left mouse button fires a bullet
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN and game_over == False:
        shoot_bullet()

    # # Right mouse button toggles camera tracking mode
    if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        fpp = not fpp


def setupCamera():
    global screen_width, screen_height, fpp, scale_factor, player_angle
    """
    Configures the camera's projection and view settings.
    Uses a perspective projection and positions the camera to look at the target.
    """
    glMatrixMode(GL_PROJECTION)  # Switch to projection matrix mode
    glLoadIdentity()  # Reset the projection matrix
    # Set up a perspective projection (field of view, aspect ratio, near clip, far clip)
    aspect_ratio = screen_width/screen_height
    if fpp:
        gluPerspective(fovY, aspect_ratio, 0.1, 2500)
    else:
        gluPerspective(fovY, aspect_ratio, 0.1, 1500) #fov, ratio, closest obj, farthest obj
    glMatrixMode(GL_MODELVIEW)  # Switch to model-view matrix mode
    glLoadIdentity()  # Reset the model-view matrix

    # Extract camera position and look-at target
    if fpp:
        cam_pos_x = player_x
        cam_pos_y = player_y-30 #behind
        cam_pos_z = player_z + 170*scale_factor #top

        look_at_x = player_x
        look_at_y = player_y
        look_at_z = player_z + 150*scale_factor

        gluLookAt(cam_pos_x, cam_pos_y, cam_pos_z,
                look_at_x, look_at_y, look_at_z,
                0, 0, 1)
    else:
        x, y, z = camera_pos
        # Position the camera and set its orientation
        gluLookAt(x, y, z,  # Camera position
                0, 0, 0,  # Look-at target
                0, 0, 1)  # Up vector (Y-axis)


def idle():
    """
    Idle function that runs continuously:
    - Triggers screen redraw for real-time updates.
    """
    # Ensure the screen updates with the latest changes
    animate()
    make_powerup()            # spawn powerups over time
    check_powerup_collection()
    check_brick_collection()
    glutPostRedisplay()
    glutPostRedisplay()


def showScreen():
    global life, score, missed_bullets,cell_size,cells
    """
    Display function to render the game scene:
    - Clears the screen and sets up the camera.
    - Draws everything of the screen
    """
    global day_night, last_day_switch
    now=time.time()
    if now-last_day_switch>20:
        day_night="night" if day_night=="day" else "day"
        last_day_switch=now

    if day_night=="day":
        glClearColor(0.2,0.6,1.0,1.0) # bright sky
    else:
        glClearColor(0.0,0.0,0.0,1.0) # dark night
        # dark overlay to reduce visibility
        glViewport(0, 0, screen_width, screen_height)


    # Clear color and depth buffers
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
 
    glLoadIdentity()  # Reset modelview matrix
    glViewport(0, 0, screen_width, screen_height)  # Set viewport size

    setupCamera()  # Configure camera perspective

    barrier_height = 200
    #top barrier --> -Y
    glBegin(GL_QUADS)
    glColor3f(0.0, 1.0, 1.0)
    glVertex3f(-GRID_LENGTH, -GRID_LENGTH, 0)
    glVertex3f(GRID_LENGTH, -GRID_LENGTH, 0)
    glVertex3f(GRID_LENGTH, -GRID_LENGTH, barrier_height)
    glVertex3f(-GRID_LENGTH, -GRID_LENGTH, barrier_height)
    glEnd()

    #bot barrier --> +Y
    glBegin(GL_QUADS)
    glColor3f(1,1,1)
    glVertex3f(-GRID_LENGTH, GRID_LENGTH, 0)          # bottom-left
    glVertex3f(GRID_LENGTH, GRID_LENGTH, 0)           # bottom-right
    glVertex3f(GRID_LENGTH, GRID_LENGTH, barrier_height) # top-right
    glVertex3f(-GRID_LENGTH, GRID_LENGTH, barrier_height) # top-left
    glEnd()

    #left barrier --> +X
    glBegin(GL_QUADS)
    glColor3f(0,0,1)
    glVertex3f(GRID_LENGTH, -GRID_LENGTH, 0)
    glVertex3f(GRID_LENGTH, GRID_LENGTH, 0)
    glVertex3f(GRID_LENGTH, GRID_LENGTH, barrier_height)
    glVertex3f(GRID_LENGTH, -GRID_LENGTH, barrier_height)
    glEnd()

    #right barrier --> -X
    glBegin(GL_QUADS)
    glColor3f(0,1,0)
    glVertex3f(-GRID_LENGTH, -GRID_LENGTH, 0)
    glVertex3f(-GRID_LENGTH, GRID_LENGTH, 0)
    glVertex3f(-GRID_LENGTH, GRID_LENGTH, barrier_height)
    glVertex3f(-GRID_LENGTH, -GRID_LENGTH, barrier_height)
    glEnd()

    # Draw the grid (game floor)
    glBegin(GL_QUADS)
    for row in range(cells):
        for column in range(cells):

            #color alternate
            if (row + column) % 2 != 0:
                glColor3f(1.0, 1.0, 1.0)
            if (row + column) % 2 == 0:
                glColor3f(0.7, 0.5, 0.95)

            #satrts from (-GRID_LENGTH, -GRID_LENGTH) - top-right corner (-x,-y,0)
            x0 = -GRID_LENGTH + row*cell_size
            y0 = -GRID_LENGTH + column*cell_size

            #bot-left corner of each cell (x,y,0)
            x1 = x0 + cell_size
            y1 = y0 + cell_size

            #draw one quad (z plane)
            #drawing starts from top right --> top left
            #starts with purple then white .....
            glVertex3f(x1, y1, 0) #bot-left
            glVertex3f(x0, y1, 0) #bot-right
            glVertex3f(x0, y0, 0) #top-right
            glVertex3f(x1, y0, 0) #top-left
    glEnd()

    #20 px right, 200 px down from top-left
    draw_text(-screen_width/2 + 20, screen_height/2- 200, f"Player Life Remaining: {life}")
    #20 px right, 180 px down from top-left
    draw_text(-screen_width/2 + 20, screen_height/2- 180, f"Game Score: {score}")
    #20 px right, 160 px down from top-left
    draw_text(-screen_width/2 + 20, screen_height/2- 160, f"Player Bullet Missed: {missed_bullets}")
    draw_bricks()
    draw_powerups()
    draw_tower()
    draw_shapes()
    # Swap buffers for smooth rendering (double buffering)
    
    glutSwapBuffers()
    



# Main function to set up OpenGL window and loop
def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)  # Double buffering, RGB color, depth test
    glutInitWindowSize(1200,700)  # Window size
    glutInitWindowPosition(0,0)  # Window position top left
    wind = glutCreateWindow(b"Brickocalypse")  # Create the window

    glutDisplayFunc(showScreen)  # Register display function
    glutKeyboardFunc(keyboardListener)  # Register keyboard listener
    glutSpecialFunc(specialKeyListener)
    glutMouseFunc(mouseListener)
    glutIdleFunc(idle)  # Register the idle function to move the bullet automatically
    make_enemy() #instant spawn
    make_bricks()
    glutMainLoop()  # Enter the GLUT main loop

if __name__ == "__main__":
    main()
