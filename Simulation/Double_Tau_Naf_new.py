# TAU_NAF convertor
import random
import math
import time

# Y^2 + X*Y = X^3 + ax^2 + 1
# {S1,S2} --> 0,-1,+1,0 (NOT ACCURED)
# {S1,S3} --> 0,-1,-1,0 (NOT ACCURED)
# {S2,S3} --> +1,0,-1,0 (ACCURED)
# {S2,S2} --> +1,0,+1,0 (ACCURED)
# {S3,S3} --> -1,0,-1,0 (ACCURED)
# {S3,S2} --> -1,0,+1,0 (ACCURED)
# {S4,S2} --> 0,+1,+1,0 (NOT ACCURED)
# {S4,S3} --> 0,+1,-1,0 (NOT ACCURED)
# {S5,S2} --> 0,0,+1,0 (ACCURED)
# {S5,S3} --> 0,0,-1,0 (ACCURED)

a = 1
meu = pow(-1, 1-a)

def inject_single_fault(result,MAX_ERROR_INJECTION_Portion):

    possible_outputs = [[0,0],[0,1],[0,-1],[1,1],[1,0],[1,-1],[-1,-1],[-1,0],[-1,1]]
    number_of_errors = math.floor(len(result)*MAX_ERROR_INJECTION_Portion)
    for i in range(number_of_errors):
        index = random.randint(0,int((len(result)-1)/2))*2
        if(index+1<len(result)):
            temp_possible_output = possible_outputs[:]
            u0 = result[index]
            u1 = result[index+1]
            temp_possible_output.remove([u0,u1])
            output_bit = random.choice(temp_possible_output)
            result[index] = output_bit[0]
            result[index+1] = output_bit[1]
            return
def inject_fault(result,MAX_ERROR_INJECTION_Portion):
    possible_outputs = [[0,0],[0,1],[0,-1],[1,1],[1,0],[1,-1],[-1,-1],[-1,0],[-1,1]]
    number_of_errors = math.floor(len(result)*MAX_ERROR_INJECTION_Portion)
    # print(len(result))
    # print(number_of_errors)
    # print("######")
    # time.sleep(1)
    for i in range(number_of_errors):
        index = random.randint(0,int((len(result)-1)/2))*2
        if(index+1<len(result)):
            temp_possible_output = possible_outputs[:]
            u0 = result[index]
            u1 = result[index+1]
            temp_possible_output.remove([u0,u1])
            output_bit = random.choice(temp_possible_output)
            result[index] = output_bit[0]
            result[index+1] = output_bit[1]
def insert_fault_burst(result,MAX_ERROR_INJECTION_Portion):
    possible_outputs = [1, -1, 0]
    number_of_errors = math.floor(len(result)*MAX_ERROR_INJECTION_Portion)
    index = random.randint(0,len(result)-1)
    for i in range(number_of_errors):
        if(index+i<len(result)):
            temp_possible_output = possible_outputs[:]
            temp_possible_output.remove(result[index+i])
            result[index+i] = random.choice(temp_possible_output)
def generate_error(MAX_ITERATION,Exact_ERROR_Portion,zero_checker,positive_checker,negative_checker):
    CC_ERROR_COUNTER = 0
    for i in range(MAX_ITERATION):
        CC_ERROR_COUNTER , output = Double_TAU_NAF_WITH_ERROR_BURST(i+1000000, 0,Exact_ERROR_Portion,CC_ERROR_COUNTER,zero_checker,positive_checker,negative_checker)
        # CC_ERROR_COUNTER , output = Double_TAU_NAF_WITH_ERROR_BURST(i*10+j, j,Exact_ERROR_INJECTION,CC_ERROR_COUNTER,zero_checker,positive_checker,negative_checker)
    print("------------------------DOUBLE_TAU_NAF------------------------")
    print("Zero Checker = {zero_checker}".format(zero_checker=zero_checker))
    print("Positive Checker = {Positive_checker}".format(Positive_checker=positive_checker))
    print("Negative Checker = {negative_checker}".format(negative_checker=negative_checker))
    print("Exact error injection is {Exact_ERROR_Portion}".format(Exact_ERROR_Portion=Exact_ERROR_Portion))
    print("Precision is: {precision}%, Number of samples: {MAX_ITERATION}, Detected errors by CC: {CC_ERROR_COUNTER}"
      .format(MAX_ITERATION=MAX_ITERATION,
              CC_ERROR_COUNTER=CC_ERROR_COUNTER,
              precision=(CC_ERROR_COUNTER/MAX_ITERATION)*100))
def Double_TAU_NAF_WITH_ERROR(d0, d1,Exact_ERROR_Portion,CC_ERROR_COUNTER,zero_checker,positive_checker,negative_checker):
    zero_counter = 0
    positive_counter = 0
    negative_counter = 0
    c0 = d0
    c1 = d1
    u = 0 
    result = []
    while c0 != 0 or c1 != 0:
        u = (c0 - 2*c1) % 4
        if u == 3: # sE1 -->  0,-1
            u0 = -1
            u1 = 0
            zero_counter += 1 
            negative_counter += 1
        elif (u == 2): # s2 --> +1,0
            u0 = 0
            u1 = 1
            temp = ((2*(((c1%4)+1)%4))%8)
            if(((temp%8) == (c0%8))):
                u1 = -1 # s3 --> -1,0
                negative_counter += 1
            else:
                positive_counter += 1

            zero_counter+=1
        elif(u == 1): # s4 -->  0,+1
            u0 = 1
            u1 = 0
            zero_counter += 1
            positive_counter += 1
        else: # s5 -->  0,0
            u0 = 0 
            u1 = 0
            zero_counter += 2
        c0 = c0 - u0
        c1 = c1 - u1
        result.insert(0,u0)
        result.insert(0,u1)
        temp_c0 = c0
        temp_c1 = c1
        c0 = ((-1 * temp_c0) + (2 * meu * temp_c1))/4
        c1 = -1 * ((meu * temp_c0) + (2 * temp_c1))/4
    inject_fault(result,Exact_ERROR_Portion)
    if (coherency_checker(array=result,zero_counter=zero_counter,positive_counter=positive_counter,negative_counter=negative_counter,
                          zero_checker=zero_checker,positive_checker=positive_checker,negative_checker=negative_checker) == False):
        CC_ERROR_COUNTER += 1
        output = dict({"d0": d0, "d1": d1, "result": "CC_ERROR_FINDER"})
    else:
        output = dict({"d0": d0, "d1": d1, "result": result})
        # print("No Error detected")
    # print(CC_ERROR_COUNTER)
    return CC_ERROR_COUNTER,output
def Double_TAU_NAF_WITH_ERROR_BURST(d0, d1,exact_fault_injected,CC_ERROR_COUNTER,zero_checker,positive_checker,negative_checker):
    possible_outputs = [[0,0],[0,1],[0,-1],[1,1],[1,0],[1,-1],[-1,-1],[-1,0],[-1,1]]
    len_NAF = math.ceil(math.log(d0,2)) # Lenght of TAU NAF is 2 * log(number,2)
    if(len_NAF == 0):
        error_proabability = 1
    else:
        error_proabability = 1/len_NAF
    start_to_inject = False
    fault_injected = 0
    zero_counter = 0
    positive_counter = 0
    negative_counter = 0
    c0 = d0
    c1 = d1
    u = 0 
    result = []
    while c0 != 0 or c1 != 0:
        u = (c0 - 2*c1) % 4
        if u == 3: # sE1 -->  0,-1
            u0 = -1
            u1 = 0
            zero_counter += 1 
            negative_counter += 1
        elif (u == 2): # s2 --> +1,0
            u0 = 0
            u1 = 1
            temp = ((2*(((c1%4)+1)%4))%8)
            if(((temp%8) == (c0%8))):
                u1 = -1 # s3 --> -1,0
                negative_counter += 1
            else:
                positive_counter += 1

            zero_counter+=1
        elif(u == 1): # s4 -->  0,+1
            u0 = 1
            u1 = 0
            zero_counter += 1
            positive_counter += 1
        else: # s5 -->  0,0
            u0 = 0 
            u1 = 0

        c0 = c0 - u0
        c1 = c1 - u1

        if(random.uniform(0,1)<error_proabability or start_to_inject==True):
            start_to_inject = True
            if (fault_injected < exact_fault_injected):
                temp_possible_output = possible_outputs[:]
                temp_possible_output.remove([u0,u1])
                output_bit = random.choice(temp_possible_output)
                fault_injected += 1
                result.insert(0,output_bit[0])
                result.insert(0,output_bit[1])
            else:
                result.insert(0,u0)
                result.insert(0,u1)
        else:
            result.insert(0,u0)
            result.insert(0,u1)
        
        temp_c0 = c0
        temp_c1 = c1
        c0 = ((-1 * temp_c0) + (2 * meu * temp_c1))/4
        c1 = -1 * ((meu * temp_c0) + (2 * temp_c1))/4
    
    if (coherency_checker(array=result,zero_counter=zero_counter,positive_counter=positive_counter,negative_counter=negative_counter,
                          zero_checker=zero_checker,positive_checker=positive_checker,negative_checker=negative_checker) == False):
        CC_ERROR_COUNTER += 1
        output = dict({"d0": d0, "d1": d1, "result": "CC_ERROR_FINDER"})
    else:
        output = dict({"d0": d0, "d1": d1, "result": result})
    return CC_ERROR_COUNTER,output

def coherency_checker(zero_counter,positive_counter,negative_counter,array,
                      zero_checker=False,negative_checker=False,positive_checker=False):
    zero_loop_counter = 0
    positive_loop_counter = 0
    negative_loop_counter = 0

    for element in array:
        if (element == 0):
            zero_loop_counter += 1
        elif(element == 1):
            positive_loop_counter += 1
        elif(element == -1):
            negative_loop_counter += 1
    if(zero_checker):
        if(zero_loop_counter != zero_counter):
            return False
    if(negative_checker):
        if(negative_loop_counter != negative_counter):
            return False
    if(positive_checker):
        if(positive_loop_counter != positive_counter):
            return False
    return True

generate_error(MAX_ITERATION=1000000,Exact_ERROR_Portion=1/40,zero_checker=True,positive_checker=False,negative_checker=False)
generate_error(MAX_ITERATION=1000000,Exact_ERROR_Portion=1/20,zero_checker=True,positive_checker=False,negative_checker=False)
generate_error(MAX_ITERATION=1000000,Exact_ERROR_Portion=1/10,zero_checker=True,positive_checker=False,negative_checker=False)
generate_error(MAX_ITERATION=1000000,Exact_ERROR_Portion=1/5,zero_checker=True,positive_checker=False,negative_checker=False)
generate_error(MAX_ITERATION=1000000,Exact_ERROR_Portion=1/3,zero_checker=True,positive_checker=False,negative_checker=False)
generate_error(MAX_ITERATION=1000000,Exact_ERROR_Portion=2/3,zero_checker=True,positive_checker=False,negative_checker=False)

# generate_error(MAX_ITERATION=1000000,Exact_ERROR_Portion=1/40,zero_checker=False,positive_checker=True,negative_checker=False)
# generate_error(MAX_ITERATION=1000000,Exact_ERROR_Portion=1/20,zero_checker=False,positive_checker=True,negative_checker=False)
# generate_error(MAX_ITERATION=1000000,Exact_ERROR_Portion=1/10,zero_checker=False,positive_checker=True,negative_checker=False)
# generate_error(MAX_ITERATION=1000000,Exact_ERROR_Portion=1/5,zero_checker=False,positive_checker=True,negative_checker=False)
# generate_error(MAX_ITERATION=1000000,Exact_ERROR_Portion=1/3,zero_checker=False,positive_checker=True,negative_checker=False)
# generate_error(MAX_ITERATION=1000000,Exact_ERROR_Portion=2/3,zero_checker=False,positive_checker=True,negative_checker=False)

# generate_error(MAX_ITERATION=1000000,Exact_ERROR_INJECTION=1,zero_checker=False,positive_checker=False,negative_checker=True)
# generate_error(MAX_ITERATION=1000000,Exact_ERROR_INJECTION=3,zero_checker=False,positive_checker=False,negative_checker=True)
# generate_error(MAX_ITERATION=1000000,Exact_ERROR_INJECTION=5,zero_checker=False,positive_checker=False,negative_checker=True)
# generate_error(MAX_ITERATION=1000000,Exact_ERROR_INJECTION=10,zero_checker=False,positive_checker=False,negative_checker=True)
# generate_error(MAX_ITERATION=1000000,Exact_ERROR_INJECTION=100,zero_checker=False,positive_checker=False,negative_checker=True)
# generate_error(MAX_ITERATION=1000000,Exact_ERROR_INJECTION=1000,zero_checker=False,positive_checker=False,negative_checker=True)

generate_error(MAX_ITERATION=1000000,Exact_ERROR_Portion=1/40,zero_checker=True,positive_checker=True,negative_checker=True)
generate_error(MAX_ITERATION=1000000,Exact_ERROR_Portion=1/20,zero_checker=True,positive_checker=True,negative_checker=True)
generate_error(MAX_ITERATION=1000000,Exact_ERROR_Portion=1/10,zero_checker=True,positive_checker=True,negative_checker=True)
generate_error(MAX_ITERATION=1000000,Exact_ERROR_Portion=1/5,zero_checker=True,positive_checker=True,negative_checker=True)
generate_error(MAX_ITERATION=1000000,Exact_ERROR_Portion=1/3,zero_checker=True,positive_checker=True,negative_checker=True)
generate_error(MAX_ITERATION=1000000,Exact_ERROR_Portion=2/3,zero_checker=True,positive_checker=True,negative_checker=True)

# generate_error(MAX_ITERATION=1000000,Exact_ERROR_INJECTION=1000,zero_checker=True,positive_checker=True,negative_checker=False)
# generate_error(MAX_ITERATION=1000000,Exact_ERROR_INJECTION=1000,zero_checker=False,positive_checker=True,negative_checker=True)

# generate_error(MAX_ITERATION=1000000,Exact_ERROR_INJECTION=1000,zero_checker=True,positive_checker=False,negative_checker=True)
# generate_error(MAX_ITERATION=1000000,Exact_ERROR_INJECTION=1000,zero_checker=True,positive_checker=True,negative_checker=True)



