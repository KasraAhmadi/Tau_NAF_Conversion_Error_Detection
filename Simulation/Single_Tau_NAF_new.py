import time
import math
import random
# TAU_NAF convertor
# Y^2 + X*Y = X^3 + ax^2 + 1
a = 1
meu = pow(-1, 1-a)
samples = []
NUMBER_OF_TEST_CASES = 1000000
CC_ERROR_COUNTER = 0
Total_not_injection = 0

def coherency_checker(zero_counter, array):
    zero_loop_counter = 0
    for element in array:
        if (element == 0):
            zero_loop_counter += 1
    if (zero_loop_counter == zero_counter):
        return True
    else:
        return False 
def Tau_checker(array):
    for i in range(len(array)):
        if(i != len(array)-1):
            if(array[i]*array[i+1] != 0):
                return False
    return True
def generate_error(Exact_ERROR_Portion):
    CC_ERROR_COUNTER = 0
    Total_not_injection = 0
    for i in range(NUMBER_OF_TEST_CASES):
        CC_ERROR_COUNTER,output = TAU_NAF_WITH_ERROR_BURST((i+1000000), 0,Exact_ERROR_Portion,CC_ERROR_COUNTER)
        # TAU_NAF_WITH_ERROR_BURST((i*10+j),0)
            # print("Number: {num}, Len tau: {tau_len}".format(num=2*math.log((i*10)+j,2),tau_len=len(res["result"])))
    print("###TAU_NAF###")
    print("Error portion is {MAX_ERROR_INJECTION_Portion}".format(MAX_ERROR_INJECTION_Portion=Exact_ERROR_Portion))
    print("Precision is: {precision}%, Number of samples: {NUMBER_OF_TEST_CASES}, Detected errors by CC: {CC_ERROR_COUNTER}"
            .format(NUMBER_OF_TEST_CASES=NUMBER_OF_TEST_CASES,
                    CC_ERROR_COUNTER=CC_ERROR_COUNTER,
                    precision=(CC_ERROR_COUNTER/NUMBER_OF_TEST_CASES)*100))
    print(Total_not_injection)
    print("------------")
def insert_fault(result,Exact_ERROR_Portion):
    injected = False
    possible_outputs = [1, -1, 0]
    number_of_errors = math.floor(len(result)*Exact_ERROR_Portion)
    # print(len(result))
    # print(number_of_errors)
    # print("#####")
    # time.sleep(1)
    for i in range(number_of_errors):
        index = random.randint(0,len(result)-1)
        temp_possible_output = possible_outputs[:]
        temp_possible_output.remove(result[index])
        result[index] = random.choice(temp_possible_output)
        injected = True
    return injected

def insert_single_fault(result,Exact_ERROR_Portion):
    injected = False
    error_number = 0
    possible_outputs = [1, -1, 0]
    number_of_errors = math.floor(len(result)*Exact_ERROR_Portion)
    for i in range(number_of_errors):
        index = random.randint(0,len(result)-1)
        temp_possible_output = possible_outputs[:]
        temp_possible_output.remove(result[index])
        result[index] = random.choice(temp_possible_output)
        error_number += 1
        injected = True
        break
    return injected
def insert_fault_burst(result,Exact_ERROR_Portion):
    injected = False
    possible_outputs = [1, -1, 0]
    number_of_errors = math.floor(len(result)*Exact_ERROR_Portion)
    index = random.randint(0,len(result)-1)
    for i in range(number_of_errors):
        if(index+i<len(result)):
            temp_possible_output = possible_outputs[:]
            temp_possible_output.remove(result[index+i])
            result[index+i] = random.choice(temp_possible_output)
            injected = True
    return injected
def TAU_NAF_WITH_ERROR(d0, d1,Exact_ERROR_Portion,CC_ERROR_COUNTER):
    result = []
    zero_counter = 0
    positive_counter = 0
    negative_counter = 0
    c0 = d0
    c1 = d1
    while c0 != 0 or c1 != 0:
        if (c0 % 2 == 1):
            output_bit = int(2 - ((c0 - 2*c1) % 4))
            c0 = c0 - output_bit
            if(output_bit == 1):
                positive_counter += 1
            elif(output_bit == -1):
                negative_counter += 1
        else:
            output_bit = 0
            zero_counter += 1
        temp_c0 = c0
        temp_c1 = c1
        c0 = temp_c1 + (meu * temp_c0/2)
        c1 = -temp_c0/2
        result.insert(0,output_bit)
    if(insert_fault(result,Exact_ERROR_Portion) == False):
        Total_not_injection += 1
    if(coherency_checker(zero_counter,result) == False):
        CC_ERROR_COUNTER += 1
        output = dict({"d0": d0, "d1": d1, "result": "CC_ERROR_FINDER"})
        # print("CC detected Error")
    else:
        output = dict({"d0": d0, "d1": d1, "result": result})
        # print("No Error detected")
    return CC_ERROR_COUNTER, output
def TAU_NAF_WITH_ERROR_BURST(d0, d1,Exact_ERROR_Portion,CC_ERROR_COUNTER):
    start_to_inject = False
    possible_outputs = [1, -1, 0]
    fault_injected = 0
    result = []
    zero_counter = 0
    c0 = d0
    c1 = d1
    while c0 != 0 or c1 != 0:
        if (c0 % 2 == 1):
            output_bit = int(2 - ((c0 - 2*c1) % 4))
            c0 = c0 - output_bit
        else:
            output_bit = 0
            zero_counter += 1
        temp_c0 = c0
        temp_c1 = c1
        c0 = temp_c1 + (meu * temp_c0/2)
        c1 = -temp_c0/2
        temp_possible_output = possible_outputs[:]
        temp_possible_output.remove(output_bit)
        result.insert(0,output_bit)
    if(insert_fault_burst(result,Exact_ERROR_Portion) == False):
        Total_not_injection += 1
    if (coherency_checker(zero_counter, result) == False):
        CC_ERROR_COUNTER += 1
        output = dict({"d0": d0, "d1": d1, "result": "CC_ERROR_FINDER"})
        # print("CC detected Error")
    else:
        output = dict({"d0": d0, "d1": d1, "result": result})
        # print("No Error detected")
    return CC_ERROR_COUNTER,output

generate_error(Exact_ERROR_Portion=1/40)
generate_error(Exact_ERROR_Portion=1/20)
generate_error(Exact_ERROR_Portion=0.1)
generate_error(Exact_ERROR_Portion=1/5)
generate_error(Exact_ERROR_Portion=1/3)
generate_error(Exact_ERROR_Portion=2/3)




