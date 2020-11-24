import random
import numpy as np
def main():
    # find P(C|¬s, w)
    # initiate the state
    s1 = 0   # P(c,r,¬s,w)
    s2 = 0   # P(c,¬r,¬s,w)
    s3 = 0   # P(¬c,r,¬s,w)
    s4 = 0   # P(¬c,¬r,¬s,w)
    
    # randomize the initial state
    v = random.randint(0, 3)
    if v == 0:      # s1
        C = True
        R = True
    elif v == 1:    # s2
        C = True
        R = False
    elif v == 2:    # s3
        C = False
        R = True
    else:           # s4
        C = False
        R = False
    # generating sampling size of 1,000,000
    n = 1000000
    for i in range(n):
        k = random.randint(0, 1)  # choose either C or R
        t = random.random() # value to determine state switch
        if k == 0: # 0 for choosing C
            # Use P(C|r,¬s) = < 0.87805, 0.12195 >
            
            if R == True:         
                if t <= 0.87805: # C = true and state is now at s1
                    s1 = s1 + 1
                    C = True
                else: # C = false and state is now at s3
                    s3 = s3 + 1
                    C = False
            else: # R == False
                # Use P(C|¬r,¬s) = < 0.31034, 0.68966 >
                if t <= 0.31034: # C = true and state is now at s2
                    s2 = s2 + 1
                    C = True
                else: # C = False and state is now s4
                    s4 = s4 + 1
        else: # 1 for choosing R
            # Use P(R|c,¬s,w) = < 0.9863, 0.0137 >
            
            if C == True:
                if t <= 0.9863: # R = true and state is now at s1
                    s1 = s1 + 1
                    R = True
                else: # R = false and state is now at s2
                    s2 = s2 + 1
                    R = False
            else: # C == False, use P(R|¬c,¬s,w) = < 0.81818, 0.18182 >
                if t <= 0.81818: # R = true and state is now at s3
                    s3 = s3 + 1
                    R = True
                else: # R = false and state is now at s4
                    s4 = s4 + 1
                    R = False
    # calculate P(C|¬s, w)
    # = a<s1+s2, s3+s4> a = 1/n
    print('Part A. The sampling probabilities')
    print('P(C|¬s,r) = <0.87805, 0.12195>')
    print('P(C|¬s,¬r) = <0.31034, 0.68966>')
    print('P(R|c,¬s,w) = <0.9863, 0.0137>')
    print('P(R|¬c,¬s,w) = <0.81818, 0.18182>')
    
    print('\nPart B. The transition probability matrix')
    print('         S1','       S2','       S3','     S4')
    print('S1','0.931275',' 0.006850',' 0.060975','      0')
    print('S2','0.493150',' 0.162020','        0','0.34483')
    print('S3','0.439150','        0',' 0.470065','0.09091')
    print('S4','       0',' 0.155170',' 0.940130','0.43574')
    
    print('\nPart C. The probability for the query')
    print('P(C|¬s, w) = < ' + str((s1+s2)/n) + ', ' + str((s3+s4)/n) + ' >')
    print(f'Error: {np.absolute((.85767 - (s1+s2)/n) ) / .85767}')
    
main()