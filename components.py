from logicgates import not16,adder,and16,mux,mux8way16,inc16,band,bor3way
import linecache

# index coresponding to names = zn,nx,zy,ny,f,no
def ALU(listx,listy,controllist):
    if controllist[0]==1:
        listx = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    if controllist[1]==1:
        listx=not16(listx)
    if controllist[2]==1:
        listy = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    if controllist[3]:
        listy = not16(listy)
    if controllist[4] ==1:
        out = adder(listx,listy)
    else:
        out = and16(listx,listy)
    if controllist[5]==1:
        final = not16(out)
        out = final
    zr = 0
    ng = 0
    if out == [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]:
        zr =1
    if out[0] == 1:#means it is negative
        ng =1
    return out,zr,ng
#a,b,c = x,y,z

#   value,  store(data,load),   tick
class dflipflop:
    def __init__(self):
        self.oldstate= 0
        self.newstate=0
    def value(self):
        return self.oldstate

    def store(self,input):
        self.newstate= input
    def tick(self):
        self.oldstate=self.newstate
#   value  store(data,load), tick
class bitregister:
    def __init__(self):
        self.d = dflipflop()                     # storing thing inside the bitregister object ex botregister.d 
        
# the bit register needs to output value like a flip flop
    def store(self,data,load):
        value = mux(data,self.d.value(),load)
        self.d.store(value)
    def value(self):
        return self.d.value()
    def tick(self):
        self.d.tick()
#   value,  store(data,load), tick    made by using ai , my code is still in there so update it
class register:
    def __init__(self):
        # 1. Create a list holding 16 distinct 1-bit registers
        self.bits = []
        for i in range(16):
            self.bits.append(bitregister())

    def store(self, listof16bit, load):
        # 2. Loop through all 16 slots. 
        # Pass each individual data bit and the load bit to each register.
        for i in range(16):
            self.bits[i].store(listof16bit[i], load)

    def value(self):
        # 3. Collect the current value from each of the 16 registers
        list16 = []
        for i in range(16):
            list16.append(self.bits[i].value())
        return list16

    def tick(self):
        # 4. Crucial for your emulator! 
        # When the clock ticks, all 16 registers must tick.
        for i in range(16):
            self.bits[i].tick()

    # class register:
    #     def __init__(self):
    #         for i in range(16):
    #             self.i = bitregister()
    #     def store(self,listof16bit,load):
    #         for i in range(16):
    #             self.i.store(listof16bit[i],load)
    #     def value(self):
    #         for i in range(16):
    #             self.list16[i] = self.i.value()
    #         return self.list16
    #     def tick():
    #         #in progress
# value(address)     , store(adress,data,load),   tick
class ram8:
    def __init__(self):
        self.listofram = []
        for i in range(8):
            self.listofram.append(register())
    def value(self,adress):
        return self.listofram[mux8way16(0,1,2,3,4,5,6,7,adress)].value()

    def store(self,adress,data,load):
        self.listofram[mux8way16(0,1,2,3,4,5,6,7,adress)].store(data,load)
    def tick(self):
        for i in range(8):
            self.listofram[i].tick()
#ram hierchy is made by ai after ram 8
# value(address), store(address,data,load), tick
class ram64:
    def __init__(self):
        self.listofram = []
        for i in range(8):
            self.listofram.append(ram8())

    def value(self,address):
        return self.listofram[mux8way16(0,1,2,3,4,5,6,7,address[:3])].value(address[3:])

    def store(self,address,data,load):
        self.listofram[mux8way16(0,1,2,3,4,5,6,7,address[:3])].store(address[3:],data,load)

    def tick(self):
        for i in range(8):
            self.listofram[i].tick()


# value(address), store(address,data,load), tick

class ram512:
    def __init__(self):
        self.listofram = []
        for i in range(8):
            self.listofram.append(ram64())

    def value(self,address):
        return self.listofram[mux8way16(0,1,2,3,4,5,6,7,address[:3])].value(address[3:])

    def store(self,address,data,load):
        self.listofram[mux8way16(0,1,2,3,4,5,6,7,address[:3])].store(address[3:],data,load)

    def tick(self):
        for i in range(8):
            self.listofram[i].tick()


# value(address), store(address,data,load), tick

class ram4k:
    def __init__(self):
        self.listofram = []
        for i in range(8):
            self.listofram.append(ram512())

    def value(self,address):
        return self.listofram[mux8way16(0,1,2,3,4,5,6,7,address[:3])].value(address[3:])

    def store(self,address,data,load):
        self.listofram[mux8way16(0,1,2,3,4,5,6,7,address[:3])].store(address[3:],data,load)

    def tick(self):
        for i in range(8):
            self.listofram[i].tick()


# value(address), store(address,data,load), tick

class ram16k:
    def __init__(self):
        self.listofram = []
        for i in range(8):
            self.listofram.append(ram4k())

    def value(self,address):
        return self.listofram[mux8way16(0,1,2,3,4,5,6,7,address[:3])].value(address[3:])

    def store(self,address,data,load):
        self.listofram[mux8way16(0,1,2,3,4,5,6,7,address[:3])].store(address[3:],data,load)

    def tick(self):
        for i in range(8):
            self.listofram[i].tick()
class programcounter:
    def __init__(self):
        self.old = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        self.new = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    def store(self,reset,incr,load,input):
        if reset == 1:
            self.new = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        elif load == 1:
            self.new = input
        elif incr == 1:
            self.new = inc16(self.old)
        else:
            self.new = self.old
        return self.old
    def value(self):
        return self.old
    def tick(self):
        self.old = self.new

#tick, instruction.outputing pc,buttion for reset
class cpu():
    def __init__(self):
        self.A = register()
        self.D = register()
        self.PC = programcounter()
    def tick(self,instruction,inM,reset):
        if instruction[0] == 0:
            self.A.store(instruction,1)

            outM = self.D.value()
            writeM = 0
            pc_load = 0
        else:
           outM,zr,ng = ALU(self.D.value(),mux(self.D.value(),inM,instruction[3]),instruction[4:10])
        

           is_pos = not (zr or ng)

           j1 = instruction[13]  # Less than zero
           j2 = instruction[14]  # Equal to zero
           j3 = instruction[15]  # Greater than zero

           jump_lt = band(j1 , ng)
           jump_eq = band(j2 , zr)
           jump_gt = band(j3 , is_pos)

        
           pc_load = bor3way(jump_lt , jump_eq , jump_gt)
           writeM = instruction[12]
           self.D.store(outM,instruction[11])
           self.A.store(outM,instruction[10])

        pcout = self.PC.store(reset,1,pc_load,self.A.value())
        addressM = self.A.value()

        self.A.tick()
        self.D.tick()
        self.PC.tick()
        return writeM,addressM,outM,pcout

# so first tick the cpu to get the pcout value then use it afterwards.

#using ai
def bin_to_int(b_list):
    return int(''.join(map(str, b_list)), 2)
def int_to_binary_list_fixed(num, bits=14):
    # Formats the integer as a zero-padded binary string of 'bits' length
    return [int(digit) for digit in f"{num:0{bits}b}"]

def rom(adressof15bit):

    line_number = bin_to_int(adressof15bit) + 1
    line = linecache.getline("rom.txt", line_number).strip()

    return [int(x) for x in line]







        
  
           

    
