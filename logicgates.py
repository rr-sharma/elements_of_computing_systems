# so by convention we are taking a single bus as a list of 0 and 1s. by default we have let the single digit bus to be a integer


def bnot(a):
    if a==1:
        return 0
    elif a ==0:
        return 1

def bor(a,b):
    if a ==1 or b ==1:
        return 1
    else:
        return 0
def bor3way(a,b,c):
    if bor(a,b) ==1 or c ==1:
        return 1
    else:
        return 0
def band(a,b):
    if a == 1 and b ==1:
        return 1
    else:
        return 0

# def bxor(a,b):
#     if 
value = 0

def mux(a,b,sel):  #not inuse currently
    if sel == 1:
        return b
    else:
        return a

def andmuxor(a,b,sel):
    if sel == 0:
        return band(a,b)
    else:
        return bor(a,b)

def dmux(in_,sel):
    if sel==0:
        return (in_,0)
    else:
        return (0,in_)

#incoding can be done using dmux and mux 11:8 ,12th
# using map function and list function for the first time
# weill be using list of single integers for 16bit buss
def and16(a,b):
    # list1 = list(map(int, str(a)))
    # list2 = list(map(int, str(b)))
    # list3 =[]
    # for i in range(len(list1)):
    #      list3.append(bnot(list1[i],list2[i]))
    # return int("".join(map(str, list3)))
    # error as str(number) losses information
    list3=[]
    for i in range(len(a)):
        list3.append(band(a[i],b[i]))
    return list3

def not16(listof16bitnumber):
    out =[]
    for i in range(len(listof16bitnumber)):
        out.append(bnot(listof16bitnumber[i]))
    return out
#my mux and dmux are in built for nay length
#or8way , mux4way16,8way,    demux4way16,8way

#outputs a list of 4 
def dmux4way16(in1,bit2sel):
    if bit2sel[0]==0:
        if bit2sel[1]==0:
            out = [in1,0,0,0]
        else :
            out = [0,in1,0,0]
    if bit2sel[0]==1:
        if bit2sel[1] == 0:
            out = [0,0,in1,0]
        else:
            out = [0,0,0,in1]
    return out 

#outputs a list of 8
def dmux8way16(in1,bit3sel):
    if bit3sel[0]==0:
        if bit3sel[1]==0:
            if bit3sel[2]==0:
                return [in1,0,0,0,0,0,0,0]
            if bit3sel[2]==1:
                return [0,in1,0,0,0,0,0,0]
        if bit3sel[1]==1:
            if bit3sel[2]==0:
                return [0,0,in1,0,0,0,0,0]
            if bit3sel[2]==1:
                return [0,0,0,in1,0,0,0,0]
    if bit3sel[0]==1:
        if bit3sel[1]==0:
            if bit3sel[2]==0:
                return [0,0,0,0,in1,0,0,0]
            if bit3sel[2]==1:
                return [0,0,0,0,0,in1,0,0]
        if bit3sel[1]==1:
            if bit3sel[2]==0:
                return [0,0,0,0,0,0,in1,0]
            if bit3sel[2]==1:
                return [0,0,0,0,0,0,0,in1]

#mux4way16 chosees one singnal out of 4
def mux4way16(in1,in2,in3,in4,bit2sel):
    if bit2sel[0]==0:
        if bit2sel[1]==0:
            out = in1
        else :
            out = in2
    if bit2sel[0]==1:
        if bit2sel[1] == 0:
            out = in3
        else:
            out = in4
    return out 

def mux8way16(a,b,c,d,e,f,g,h,bit3sel):
    if bit3sel[0]==0:
        if bit3sel[1]==0:
            if bit3sel[2]==0:
                return a
            if bit3sel[2]==1:
                return b
        if bit3sel[1]==1:
            if bit3sel[2]==0:
                return c
            if bit3sel[2]==1:
                return d
    if bit3sel[0]==1:
        if bit3sel[1]==0:
            if bit3sel[2]==0:
                return e
            if bit3sel[2]==1:
                return f
        if bit3sel[1]==1:
            if bit3sel[2]==0:
                return g
            if bit3sel[2]==1:
                return h


def or16(listof16bit,listof16bit2):
    out =[]
    for i in range(len(listof16bit)):
        out.append(bor(listof16bit[i],listof16bit2[i]))
    return out

# you need a way to select 4 numbers, therfore a 2 bit select signal is required.well wew can name it selector


def halfadder(a, b):
    # Sum is calculated using the XOR gate
    sum_bit = a ^ b
    # Carry is calculated using the AND gate
    carry_bit = a & b
    return sum_bit, carry_bit
#and and & are different ?

def fulladder(a, b, carry_in):
    # First half adder adds the two main bits
    sum1, carry1 = halfadder(a, b)
    
    # Second half adder adds the incoming carry to the previous sum
    sum_final, carry2 = halfadder(sum1, carry_in)
    
    # The final carry out is True if either half adder produced a carry
    carry_out = carry1 | carry2
    
    return sum_final, carry_out

def oldadder(bin_a, bin_b):
    # Example inputs: bin_a =, bin_b = [0, 1, 1]
    carry = 0
    result = []
    
    # Loop backwards through the bits (from right to left)
    for bit_a, bit_b in zip(reversed(bin_a), reversed(bin_b)):
        # Use the full adder logic built from the half adder returns
        sum_bit, carry = fulladder(bit_a, bit_b, carry)
        result.append(sum_bit)
        
    if carry:
        result.append(carry)
        
    return list(reversed(result))

# Example: 3 + 3 (binary 11 + 11)
#print(adder([1, 1,1,1,1], [1, 1,1,1,1]))  # Output: [1, 1, 0] (binary 6)

# ignore overflow
def adder(bin_a, bin_b):
    # Example inputs: bin_a =, bin_b = [0, 1, 1]
    carry = 0
    result = []
    
    # Loop backwards through the bits (from right to left)
    for bit_a, bit_b in zip(reversed(bin_a), reversed(bin_b)):
        # Use the full adder logic built from the half adder returns
        sum_bit, carry = fulladder(bit_a, bit_b, carry)
        result.append(sum_bit)
        
    if carry:
        result.append(carry)
        
    return list(reversed(result))

def complementof2(listof16bit):
    result = []
    for i in range(16):
        result.append(1-listof16bit[i])
    final = adder(result,[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1])
    return final

# adds 1
def inc16(listof16):
    return adder(listof16,[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1])
