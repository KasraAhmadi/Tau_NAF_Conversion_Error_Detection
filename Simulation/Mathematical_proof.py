import math

#Zero_Counter Single TAU_NAF MATHEMATICAL PROOFS

def single_NAF_zero(k):
    P = 2/10
    N = 2/10
    C = 6/10
    sum = 0
    for i in range(int(k/2)+1):
        i_factoriel = math.factorial(i)
        k_neg_2I = math.factorial(k-(2*i))
        fractor = i_factoriel*i_factoriel*k_neg_2I
        sum += math.factorial(k)*((P*C)**i)*(N**(k-2*i))/fractor
    return(1-sum)

#Zero_Counter Double_TAU_NAF MATHEMATICAL PROOFS


def double_NAF_zero(k):
    P = 1/10
    N = 3/10
    C = 1/2
    CC = 1/10
    sum = 0
    for j in range(int(k/2)+1):
        for i in range(int((k-(2*j))/2)+1):
            sum += math.comb(k,i)*(C**i)*math.comb(k-i,j)*(CC**j)*math.comb(k-i-j,i+(2*j))*(P**(i+(2*j)))*(N**(k-(2*i)-(3*j)))
    return 1-sum

def double_NAF_positive(k):
    P = 7/20
    PP = 3/40
    N = 15/40
    C = 1/5
    sum = 0
    for j in range(int(k/2)+1):
        for i in range(int((k-(2*j))/2)+1):
            sum += math.comb(k,i)*(P**i)*math.comb(k-i,j)*(PP**j)*math.comb(k-i-j,i+(2*j))*(C**(i+(2*j)))*(N**(k-(2*i)-(3*j)))
    return 1-sum


my_dict = {}
for i in range(40):
    index = ((i/40)*100)
    my_dict[index] = double_NAF_positive(i)
print(my_dict)
    



