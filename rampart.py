import tkinter as tk
import numpy as np
from components import ram16k,register,int_to_binary_list_fixed









class screen:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("my emulator")
        self.root.geometry("800x450")
        self.canvas = tk.Canvas(self.root, width=512, height=256,highlightthickness=0, bd=0)
        self.canvas.pack()
        self.ram = ram16k()
        self.pixelscreen = np.array([[None for _ in range(512)] for _ in range(256)])
        for i in range(256):
            for a in range(512):
                self.pixelscreen[i][a] = self.canvas.create_rectangle(
                    a * 10, i * 10, a * 10 +10, i * 10+10 , fill="black"
                )
    def store(self,adress,data,load):
        # take input store it in ram
        self.ram.store(adress,data,load)
    def value(self,adress):
        return self.ram.value(adress)
    def tick(self):
        #update screen
        # reads ram and makes the screen 
        self.screen = np.array([[self.ram.value(int_to_binary_list_fixed(32*i + a)) for a in range(32)] for i in range(16)])
                
        # update screen using screen list
        for i in range(256):
            for a in range(512):
                if self.screen[i][a]==1:
                    self.canvas.itemconfig(self.pixelscreen[i][a], fill="black")
                else:
                    self.canvas.itemconfig(self.pixelscreen[i][a], fill="white")

        #tick the ram
        self.ram.tick()






class keyboard:
    def __init__(self):
        self.answer = register()
        self.root = tk.Tk()
        self.root.title("my keyboard")
        self.root.geometry("80x45")
        self.root.bind("<Key>", self.store)
    def store(self,event):
        # 2. Get the character pressed
        char_pressed = event.char
        
        if char_pressed:  # Only process if it's a valid printable key
            # 3. Convert the character to its integer ASCII/Unicode value
            ascii_val = ord(char_pressed)
            
            # 4. Convert that integer into a 16-bit binary list (list16)
            # Example: 'A' -> 65 -> [0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1]
            list16 = [int(bit) for bit in f"{ascii_val:016b}"]
            
            # 5. Pass the 16-bit list and the load bit (1) into the register
            self.answer.store(list16, 1)
    def value(self):
        return self.answer.value()
    def tick(self):
        self.answer.value.tick()





class ram:
    def __init__(self):
        self.ram14 = ram16k()
        self.screen= screen()
        self.keyboard = keyboard()

    def store(self,adressof15,data, load):
        if (adressof15[0],adressof15[1])== (0,0) :
            self.ram14.store(adressof15[1:16],data,load)
        if (adressof15[0],adressof15[1])== (1,0) :
            self.screen.store(adressof15[1:16],data,load)
        if (adressof15[0],adressof15[1])== (1,1) :
            self.keyboard.store(adressof15[1:16],data,load)
    def value(self,adressof15):
        if (adressof15[0],adressof15[1])== (0,0) :
            self.ram14.value(adressof15[1:16])
        if (adressof15[0],adressof15[1])== (1,0) :
            self.screen.value(adressof15[1:16])
        if (adressof15[0],adressof15[1])== (1,1) :
            self.keyboard.value(adressof15[1:16])

    def tick(self):
        self.ram14.tick()
        self.screen.tick()
        self.keyboard.tick()