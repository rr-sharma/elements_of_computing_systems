from components import cpu,rom
from rampart import ram
# inout loop we control the clock cycle by controlling the simulated singnal
#the loop in which signal value changes.
cpu = cpu()
ram = ram()


reset = 0
pcout = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
fromramM =[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
while True:
    
    inst = rom(pcout)
    writeM,addressM,outM,pcout = cpu.tick(inst,fromramM,reset)

    ram.store(addressM,outM,writeM)
    ram.tick()
    
    fromramM = ram.value(addressM)

#make ram , 3 components, screen, keyboard,ram