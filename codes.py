import random
class Codes():
    def __init__(self):
        pass
    def add_codes(self,Number_of_codes,Number_of_numbers,list_codes):
        the_codes=[]
        N=0
        while Number_of_codes > N:
            v = random.choices('0123456789',k=Number_of_numbers)         
            code =''.join(v) 
            if code not in list_codes:
                if code not in the_codes:
                    the_codes.append(code)
                    N +=1
        return the_codes