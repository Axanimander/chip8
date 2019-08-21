"""Chip 8 interpreter/emulator by Axanimander"""
import pygame
import sys #Just for sys.exit, if on Linux then get rid of this and edit the escape code on line 502
import random
from pygame.locals import *
pygame.init()
screen = 0
monocolor = 0
def init():
   global screen
   screen = pygame.display.set_mode((640, 320))
   global monocolor
   monocolor = (255, 255, 255) #Whatever our color besides black is to be
fset = [
    0xF0, 0x90, 0x90, 0x90, 0xF0,
  0x20, 0x60, 0x20, 0x20, 0x70,
  0xF0, 0x10, 0xF0, 0x80, 0xF0,
  0xF0, 0x10, 0xF0, 0x10, 0xF0,
  0x90, 0x90, 0xF0, 0x10, 0x10,
  0xF0, 0x80, 0xF0, 0x10, 0xF0,
  0xF0, 0x80, 0xF0, 0x90, 0xF0,
  0xF0, 0x10, 0x20, 0x40, 0x40,
  0xF0, 0x90, 0xF0, 0x90, 0xF0,
  0xF0, 0x90, 0xF0, 0x10, 0xF0,
  0xF0, 0x90, 0xF0, 0x90, 0x90,
  0xE0, 0x90, 0xE0, 0x90, 0xE0,
  0xF0, 0x80, 0x80, 0x80, 0xF0,
  0xE0, 0x90, 0x90, 0x90, 0xE0,
  0xF0, 0x80, 0xF0, 0x80, 0xF0,
  0xF0, 0x80, 0xF0, 0x80, 0x80
    ]
print("input the rom name you want, must be in folder with chip8.py")
z = open(raw_input(), 'rb')#proper rom loading later
print("input the delay you  want, 0 = way too fast")
delay = int(raw_input())
V = [0] * 16 #Registers
buff = [] #ROM buffer
key = [0] * 0x10 #keypad, currently the buttons are 1, q, a, z, 2, w, s, x, 3, e, d, c, v, 4, r, f, v, this could easily be adapted to the numpad
pc  = 0x200 #ROMs start at 0x200
I = 0x200 #see above
MEM = [0] * 4096 #4 kb of memory
pix = [0] * 2048 # 64 x 32 display
stack = [0] * 0xF #Stack to store pc when subroutine or jump is performed
sp = 0 # stack pointer to remember which level of stack is used
soundTimer = 0 #supposed to emit a beep when this hits 0 in a program, not implemented
delayTimer = 0 #supposed to run at 60 hz, it just counts down every few ops instead
drawflag = 0
keyflag = 0
event = 0 #keyboard events for pygame
def getop():
   global pc
   return MEM[pc] << 8 | MEM[pc + 1]  #get opcode
   
   
def loadfont(): # Load font into memory
    for i in range(0, 80):
        MEM[i] = fset[i]
buff = z.read() #temp

def loadmem(): #Load buffer into memory
    for i in range(len(buff)):
        MEM[i + 512] = ord(buff[i])
        
def clearscreen():
   
    global pix
    pix = [0] * 2048
  
   
def drawsprite(x, y, Height):
    global V
    V[0xf] = 0
    pixel = 0
    yl = 0
    xl = 0
  
    global pix
    for yl in range(Height):
       pixel = MEM[I + yl]
       for xl in range(8):
          if(((pixel & (0x80 >> xl)) != 0)):  
             if pix[(x + xl + ((y + yl) * 64)) % 2048]  == 1:
                V[0xf] = 1
             pix[x + xl + ((y + yl) * 64) % 2048] ^= 1
   
def rand():
   return random.randint(1, 1000)

def keydwn(pkey):
   print(pkey)
   global key
   if(pkey== pygame.K_1):
           key[0x1] = 1
   elif(pkey== pygame.K_2):
           key[0x2] = 1
   elif(pkey== pygame.K_3):
           key[0x3] = 1
   elif(pkey== pygame.K_4):
           key[0xC] = 1
   elif(pkey== pygame.K_q):
           key[0x4] = 1
   elif(pkey== pygame.K_w):
           key[0x5] = 1
   elif(pkey== pygame.K_e):
           key[0x6] = 1
   elif(pkey== pygame.K_r):
           key[0xD] = 1
   elif(pkey== pygame.K_a):
           key[0x7] = 1
   elif(pkey== pygame.K_s):
           key[0x8] = 1
   elif(pkey== pygame.K_d):
           key[0x9] = 1
   elif(pkey== pygame.K_f):
           key[0xE] = 1
   elif(pkey== pygame.K_z):
           key[0xA] = 1
   elif(pkey== pygame.K_x):
           key[0x0] = 1
   elif(pkey== pygame.K_c):
           key[0xB] = 1
   elif(pkey== pygame.K_v):
           key[0xF] = 1

def keyup(pkey):
   global key
   key = [0] * 0x10 #below is the old bad and tedious keyup code that I never got working right
   """ 
   if(pkey== pygame.K_1):
           key[0x1] = 0
   elif(pkey==pygame.K_2):
           key[0x2] = 0
   elif(pkey==pygame.K_3):
           key[0x3] = 0
   elif(pkey== pygame.K_4):
           key[0xC] = 0
   elif(pkey== pygame.K_q):
           key[0x4] = 0
   elif(pkey== pygame.K_w):
           key[0x5] = 0
   elif(pkey== pygame.K_e):
           key[0x6] = 0
   elif(pkey== pygame.K_r):
           key[0xD] = 0
   elif(pkey== pygame.K_a):
           key[0x7] = 0
   elif(pkey== pygame.K_s):
           key[0x8] = 0
   elif(pkey== pygame.K_d):
           key[0x9] = 0
   elif(pkey== pygame.K_f):
           key[0xE] = 0
   elif(pkey== pygame.K_z):
           key[0xA] = 0
   elif(pkey== pygame.K_x):
           key[0x0] = 0
   elif(pkey== pygame.K_c):
           key[0xB] = 0
   elif(pkey== pygame.K_v):
           key[0xF] = 0"""
def draw():
   global pix
   
   for y in range(32):
      for x in range(64):
         if(pix[(y * 64) + x] == 1):
          pygame.draw.rect(screen, monocolor, (x * 7, y * 5, 7, 5))
   pygame.display.flip()
lp= 0 # Timer delay counter thingy (because I don't want to emulate 60hz)
def exop():
    global pix
    global pc
    global V
    global stack
    global sp
    global I
    global delayTimer
    global soundTimer
    global drawflag
    global lpc
    global key
    global keyflag
    global event
    global lp
    hum = V[3]
    oppy = getop()
    lp += 1
    dbg = 0
    if oppy == 0:
       pc += 2
       
    if oppy & 0xf000 == 0x1000: #opcode 0x1000: Jumps to address at NNN
        pc = oppy & 0x0fff
        if dbg:
         print(1)
         
    elif oppy & 0xf000 == 0x0000:
       
       if oppy & 0x000f == 0x0000:#opcode 0x00e0: Clears the screen
        pix = [0] * 4096
        drawflag = 1
        pc += 2
        if dbg:
         print(2)
         
       elif oppy & 0x000f == 0x000e: # opcode 0x00EE: returns from a subroutine
           sp -= 1
           pc = stack[sp]
           pc += 2
           if dbg:
            print(3)
            
    elif oppy & 0xF000 == 0x2000: #opcode 0x2NNN: Calls subroutine at NNN
     stack[sp] = pc
     sp += 1
     pc = oppy & 0x0fff
     if dbg:
      print(4)
      
    elif oppy & 0xf000 == 0x3000: #opcode 0x3XNN: Skips the next instruction if VX equals NN
        if V[(oppy & 0x0f00) >> 8] == (oppy & 0x00ff):
            pc += 4
        else:
            pc += 2
        if dbg:
         print(6)
         
    elif oppy & 0xf000 == 0x4000:# opcode 4XNN: Skips the next instruction if VX doesn't equal NN.
       if(V[(oppy & 0x0F00) >> 8] != (oppy & 0x00FF)):
          pc += 4
       else:
          pc += 2
       if dbg:
          print(7)
          print(V[(oppy & 0x0f00) >> 8])
          
    elif oppy & 0xf000 == 0x5000: #opcode 5XY0: Skips the next instruction if VX equals VY.
       if(V[(oppy & 0x0F00) >> 8] == V[(oppy & 0x00F0) >> 4]):
            pc += 4
       else:
            pc += 2
       if dbg:
          print(8)
          
    elif oppy & 0xf000 == 0x6000: #opcode 6XNN: Sets VX to NN.
        V[(oppy & 0x0f00) >> 8] = (oppy & 0x00ff)
        pc += 2
        if dbg:
           print(9)
    elif oppy & 0xf000 == 0x7000: #opcode 7XNN: Adds NN to VX.
       V[(oppy & 0x0F00) >> 8] += (oppy & 0x00FF)
       pc += 2
       if dbg:
          print(10)
          
    elif oppy & 0xf000 == 0x8000: #opcodes of the form 0x8***
        if oppy & 0x000f == 0x0000:
           V[(oppy & 0x0F00) >> 8] = V[(oppy & 0x00F0) >> 4]
           pc += 2
           if dbg:
            print(11)
            
        elif oppy & 0x000f == 0x0001: #opcode 0x8XY1: sets VX to VX OR VY
           V[(oppy & 0x0f00) >> 8] |= V[(oppy & 0x00f0) >> 4]
           pc += 2
           if dbg:
            print(12)
            
        elif oppy & 0x000f == 0x0002: #opcode 0x8XY2: sets VX to VX AND VY
           V[(oppy & 0x0F00) >> 8] &= V[(oppy & 0x00F0) >> 4]
           pc += 2
           if dbg:
            print(13)
            
        elif oppy& 0x000f == 0x0003: #OPCODE 0x8XY3: sets VX to VX XOR VY
           V[(oppy & 0x0F00) >> 8] ^= V[(oppy & 0x00F0) >> 4]
           pc += 2
           if dbg:
            print(14)
                  
        elif oppy & 0x000f == 0x0004: #opcode 0x8XY4: Adds VY to VX. VF is set to 1 when there's a carry, and to 0 when there isn't
            if V[(oppy & 0x00f0) >> 4] > (0xff -  V[(oppy & 0x0f00) >> 8]):
                V[0xf] = 1
            else:
                V[0xf] = 0
            V[(oppy & 0x00f0) >> 4] += V[(oppy & 0x0f00) >> 8]
            pc += 2
            if dbg:
             print(15)
                  
        elif oppy & 0x000f == 0x0005: #opcode 0x8XY5: Subtracts VY from VX, VF is set to 0 if there is a borrow
            if V[(oppy & 0x00f0) >> 4] > V[(oppy & 0x0f00) >> 8]:
                V[0xf] = 0
            else:
                V[0xf] = 1
            V[(oppy & 0x0f00) >> 8] -= V[(oppy & 0x00f0) >> 4]
            pc += 2
            if dbg:
             print(16)
                  
        elif oppy & 0x000f == 0x0006: #opcode 0x8XY6: Shifts VX right by one. VF is set to the value of the least significant bit of VX before the shift
            V[0xf] = V[oppy & 0x0f00 >> 8] & 1
            V[(oppy & 0x0f00) >> 8] >>= 1
            pc += 2
            if dbg:
             print(17)
                  
        elif oppy & 0x000f == 0x0007: #opcode 0x8XY7: Sets VX to VY minus VX. VF is set to 0 when there's a borrow, and 1 when there isn't.
          if (V[(oppy & 0x0F00) >> 8] > V[(oppy & 0x00F0) >> 4]):
             V[0xf] = 0
          else:
             V[0xf] = 1
          V[(oppy & 0x0F00) >> 8] = V[(oppy & 0x00F0) >> 4] - V[(oppy & 0x0F00) >> 8]
          pc += 2
          if dbg:
           print(18)
                  
        elif oppy & 0x000f == 0x000e: #opcode 0x8XYE:  Shifts VX left by one. VF is set to the value of the most significant bit of VX before the shift
            V[0xF] = V[(oppy & 0x0F00) >> 8] >> 7
            V[(oppy & 0x0F00) >> 8] <<= 1
            pc += 2;
            if dbg:
             print(19)
                  
        else:
           print("Unknown opcode: " + str(hex(oppy)))
                  
    elif oppy & 0xf000 == 0x9000: #opcode 0x9XY0: Skips next instruction if VX does not equal VY
            if V[(oppy & 0x0f00) >> 8] != V[(oppy & 0x00f0) >> 4]:
                pc += 4
            else:
                pc += 2
            if dbg:
             print(20)
    elif oppy & 0xf000 == 0xa000: #opcode 0xANNN: sets I to the address NNN
        I = oppy & 0x0fff
        pc += 2
        if dbg:
         print(21)
    elif oppy & 0xf000 == 0xb000: #opcode 0xBNNN: jumps to the address NNN + V0
       pc = (oppy & 0x0fff) + V[0]
       #pc += 2
       if dbg:
          print(22)
    elif oppy & 0xf000 == 0xc000: #0xCXNN: sets VX to a random number and NN
     V[(oppy & 0x0F00) >> 8] = (rand() % 0xFF) & (oppy & 0x00FF)
     pc += 2
     if dbg:
        print(23)
    elif oppy & 0xf000 == 0xd000: #0xDXYN: Draws a sprite at coordinate (VX, VY) that has a width of 8 pixels and a height of N pixels. 
                                     #Each row of 8 pixels is read as bit-coded starting from memory location I; 
                     #I value doesn't change after the execution of this instruction. 
                     #VF is set to 1 if any screen pixels are flipped from set to unset when the sprite is drawn, 
                     #and to 0 if that doesn't happen
        drawsprite(V[(oppy & 0x0f00) >> 8], V[(oppy & 0x00f0) >> 4], oppy & 0x000f)
       
        drawflag = 1
        pc += 2
        if dbg:
         print(24)
    elif oppy & 0xf000 == 0xe000: #opcodes of the form 0xE***
       if oppy & 0x00ff == 0x009e: #opcode 0xEX9E: skips the next instruction if the key stored in VX is pressed
          
          if(key[V[(oppy & 0x0F00) >> 8]] != 0):
             pc += 4
             keyflag = 1
           #  print('A')
          else:
             pc += 2
            # print('B')
          if dbg:
               print(25 + 'a')
       elif oppy & 0x00ff == 0x00a1: #opcode 0xEXA1: Skips the next instruction if the key stored in VX isn't pressed
        
          if (key[V[(oppy & 0x0F00) >> 8]] == 0):
             pc += 4
             keyflag = 1
            # print('C')
          else:
             pc += 2
             
           #  print('D')
          if dbg:
              print(25)
    elif oppy & 0xf000 == 0xf000: #opcodes of the form 0xF***
       if oppy & 0x000f == 0x0007: #opcode 0xFX07: sets VX to the value of the delay timer
          V[(oppy & 0x0f00) >> 8] = delayTimer
          pc += 2
          if dbg:
             print(26)
       elif oppy & 0x00ff == 0x000a: #opcode 0xFX0A: A key press is awaited, and then stored in VX
          kp = False
          key = [0] * 0x10
          
          for m in range(16):
             if(key[m] != 0):
                V[(oppy & 0x0f00) >> 8] = m
                kp = True 
          if not kp:
             return
          pc += 2
          if dbg:
           print(27)
       elif oppy & 0x00ff == 0x0015: #opcode 0xfx15: sets the delay timer to vx
          delayTimer = V[(oppy & 0x0f00) >> 8]
          pc += 2
          if dbg:
           print(28)
       elif oppy & 0x00ff == 0x0018: #opcode 0xfx18: sets the sound timer to vx
          soundTimer = V[(oppy & 0x0f00) >> 8]
          pc += 2
          if dbg:
           print(29)
       elif oppy & 0x00ff == 0x001e: #opcode 0xfx1e: adds VX to I
          if(I + V[(oppy & 0x0f00) >> 8] > 0xfff):
             V[0xf] = 1
          else:
             V[0xf] = 0
          I += V[(oppy & 0x0f00) >>8]
          pc += 2
          if dbg:
             print(30)
       elif oppy & 0x00ff == 0x0029: #opcode 0xfx29: Sets I to the location of the sprite for the character in VX. Characters 0-F (in hexadecimal) are represented by a 4x5 font.
          I = V[(oppy & 0x0f00) >> 8] * 0x5
          pc += 2
          if dbg:
             print(31)
       elif oppy & 0x00ff == 0x0033: #opcode 0xfx33: Stores the Binary-coded decimal representation of VX, with the most significant of three digits at the address in I, the middle digit at I plus 1,
                                        #and the least significant digit at I plus 2. (In other words, take the decimal representation of VX, place the hundreds digit in memory at location
                                        #in I, the tens digit at location I+1, and the ones digit at location I+2.)
          MEM[I] = V[(oppy & 0x0F00) >> 8] / 100
          MEM[I + 1] = (V[(oppy & 0x0F00) >> 8] / 10) % 10
          MEM[I + 2] = (V[(oppy & 0x0F00) >> 8] % 100) % 10
          pc += 2
          if dbg:
             print(32)
       elif oppy & 0x00ff == 0x0055: #opcode 0xFX55: stores V0 to VX starting at address I
          for i in range(((oppy & 0x0f00) >> 8 ) + 1):
             MEM[I + i] = V[i]
          I += ((oppy & 0x0f00) >> 8) + 1
          pc += 2
          if dbg:
             print(33)
       elif oppy & 0x00ff == 0x0065: #opcode 0xfx65: Fills V0 to VX with values from memory starting at address I
          for n in range(0, (((oppy & 0x0f00) >> 8) + 1)):
             V[n] = MEM[I + n]
          I += ((oppy & 0x0f00) >> 8) + 1
          pc += 2
          if dbg:
             print(34)
       else:
        print("Unknown opcode: " + str(hex(oppy)))
        pc += 2
    
    else:
        print("Unknown opcode: " + str(hex(oppy)))
        pc += 2
    if lp % 2  == 0: #Timer delay, very fiddly, 
       if delayTimer > 0:
         delayTimer -= 1
         
       if soundTimer > 0:
         soundTimer -= 1
init() #Initialize pygame
                  
def getinput(): #gets input...
   for event in pygame.event.get():
      if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
         keydwn(event.key)
                  
def fixop(): #patches up operator overflows
   for n in range(len(V)):
      if V[n] >= 256:
         V[n] -= 256
                  
def mainloop():
   global screen
   loadmem() #Fill MEM with rom starting at 0x200
   loadfont() #Fill beginning of MEM with the font
   global drawflag
   global keyflag
   global event
   global I
   while(1):
     exop() #execute the opcode in MEM that the PC is pointed at
     fixop() #fix operator overflows (the need for this may be a flaw but roms seem to work)
     if I > 4096: #Index register overflow protection
        I = I % 4096
     if drawflag == 1: #Time to create art
        draw()
        drawflag = 0
        screen.fill((0,0,0)) #Because screen refreshing is for noobs
     pygame.time.wait(delay)
     for event in pygame.event.get():
           if event.type == KEYDOWN: 
               keydwn(event.key)
           elif event.type == KEYUP:
              keyup(1)
           elif event.type == pygame.QUIT:
              sys.exit()   
mainloop()

            

   
