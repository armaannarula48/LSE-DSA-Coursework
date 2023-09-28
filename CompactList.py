# Candidate No: 46724

MIN = -1000
MAX = 1000

class CompactList:
    def __init__(self,inlist=[]):
        inlist.sort()
        self.lst = []   # Compact List Representation
        
        if len(inlist) > 0:
            self.lst.append(inlist[0])      #Add first value in inlist into the compact list
            prev = inlist[0]
            
            for i in range(1, len(inlist)):
                if inlist[i] > prev + 1:
                    self.lst.append(prev+1)     #Adding first number after inlist[i-1] not in the list
                    self.lst.append(inlist[i])
                prev = inlist[i]
            
            if prev < MAX:
                self.lst.append(prev+1)
                        
    
    
    
    def cardinality(self):
        count = 0
        if len(self.lst) > 0:
            for i in range(1, len(self.lst), 2):             #Step size 2 to iterate thorugh odd indexed values
                count += (self.lst[i] - self.lst[i-1])
            
            if (len(self.lst) % 2) == 1:                        #Odd length compact list includes values from last element in compact list until MAX
                count += (MAX + 1 - self.lst[len(self.lst) - 1]) 
        
        return count
    
    
    
    def complement(self):  
        comp = CompactList([])
        
        if len(self.lst) > 0:
            if self.lst[0] > MIN:
                comp.lst.append(MIN)            #e.g. Complement of <10, 20> begins with <MIN, 10, ...>
                comp.lst.append(self.lst[0])
            
            for i in range(1, len(self.lst)):               
                comp.lst.append(self.lst[i])
        else:
            comp.lst.append(MIN)        #if list length is 0 i.e. empty set, the complement is the whole set represented by compact list [MIN]
        
        return comp
            
    
    def union(self,cl):
        l, r = 0, 0
        union_cl = CompactList([])
        
        while l < len(self.lst) and r < len(cl.lst):
            if self.lst[l] < cl.lst[r]:
                if union_cl.lst and self.lst[l] < union_cl.lst[-1]:         
                    if l+1 < len(self.lst) and self.lst[l+1] < union_cl.lst[-1]:        #Checking if current indices in lst and self are less than values we added in union_cl in prior iteration
                        l+=2
                        continue
                    else:
                        union_cl.lst.pop()
                    
                else: 
                    union_cl.lst.append(self.lst[l])

                l += 1
                
                if l < len(self.lst):
                    if self.lst[l] < cl.lst[r]:
                        union_cl.lst.append(self.lst[l])        #e.g. the case <10,20> U <30,40>, we append 10,20 to our compact list
                        l += 1
                    else:
                        r += 1
                        if r < len(cl.lst):
                            if self.lst[l] < cl.lst[r]:             
                                union_cl.lst.append(cl.lst[r])  #e.g. the case <10,20> U <15,25>, we append 10,25 to our compact list
                                
                            else:
                                union_cl.lst.append(self.lst[l]) #e.g. the case <10,20> U <15,18>, we append 10,20 to our compact list
                            l+=1
                            r+=1
                        else:
                            return union_cl                     #e.g. the case <10,30> U <15>, we return the compact list <10>
                else:
                    return union_cl                             #e.g. the case <10> U <20,30> , we return the compact list <10>
            
            else:
                
                if union_cl.lst and cl.lst[r] <  union_cl.lst[-1]:
                    if r+1 < len(cl.lst) and cl.lst[r+1] < union_cl.lst[-1]:
                        r+=2
                        continue
                    else:
                        union_cl.lst.pop()
                        
                else: 
                    union_cl.lst.append(cl.lst[r])
                
                r+=1
                
                if r < len(cl.lst):                         
                    if cl.lst[r] < self.lst[l]:
                        union_cl.lst.append(cl.lst[r])      #e.g. the case <30,40> U <10,20>, we append 10,20 to our compact list
                        r+=1
                    else:
                        l+=1
                        if l < len(self.lst):
                            if cl.lst[r] < self.lst[l]:
                                union_cl.lst.append(self.lst[l])    #e.g. the case <15,25> U <10,20>, we append 10,25 to our compact list
                            else:
                                union_cl.lst.append(cl.lst[r])      #e.g. the case <15,18> U <10,20>, we append 10,20 to our compact list
                            l += 1
                            r += 1
                            
                        else:
                            return union_cl                     #e.g. the case <15> U <10,30>  , we return the compact list <10>
                    
                else:
                    return union_cl                        #e.g. the case <20,30> U <10> , we return the compact list <10>
                
        ### Note all the above if statements and operations inside the while loop have O(1) runtime.
        

        #Add remaining elements in self and cl to the union compact list 
        
        while(l < len(self.lst)):
            if union_cl.lst and self.lst[l] <  union_cl.lst[-1]:
                if l+1 < len(self.lst) and self.lst[l+1] < union_cl.lst[-1]:
                    l+=2
                    continue
                else:
                    union_cl.lst.pop()
            else: 
                union_cl.lst.append(self.lst[l])
            l += 1
        
        while(r < len(cl.lst)):
            if union_cl.lst and cl.lst[r] < union_cl.lst[-1]:
                if r+1 < len(cl.lst) and cl.lst[r+1] < union_cl.lst[-1]:
                    r+=2
                    continue
                else:
                    union_cl.lst.pop()

            else: 
                union_cl.lst.append(cl.lst[r])
            
            r+=1
        
        return union_cl
        
 
    
    # Set is empty when the length of the compact list is 0, len() is an O(1) operation
    
    def isEmpty(self): 
        return len(self.lst) == 0
                                   
    
    # A ∩ B = (A' ∪ B')'
    
    def intersection(self,cl):
        
        return ((self.complement()).union(cl.complement())).complement()
    
    
    # A \ B = A ∩ B'
    
    def difference(self,cl):
        
        return self.intersection(cl.complement())
    
    
    # A subset of B iff cardinality of A = cardinality of intersection between A and B
    
    def subsetOf(self,cl):
        
        return self.cardinality() == (self.intersection(cl)).cardinality()
    
    # A = B iff A subset of B and B subset of A
    
    def equals(self,cl):  
    
        return self.subsetOf(cl) and cl.subsetOf(self)
    
    # inserting val into A: A U {val}
    
    def insert(self,value):   
        value_cl = CompactList([value])     #Compact list representation of singleton set {val}
        
        return self.union(value_cl)
        
    #Deleting val from A is equivalent to taking the difference between the sets A and {val}

    def delete(self,value):   
        value_cl = CompactList([value])     #Compact list representation of singleton set {val}
        
        return self.difference(value_cl) 
    
    
    # Modified version of binary search
    
    def contains(self, value):
        start,end = 0,len(self.lst)-1
        while start<=end:
            m=(start+end)//2
            if self.lst[m] == value:
                if m % 2 == 0:    #Even indexed values in compact list are included in set
                    return True
                else:           #Odd indexed values not included
                    return False
            
            elif self.lst[m] > value:
                end = m-1
            else:
                start = m+1
        
        #Value is in between (end, start) 
        
        if end % 2 == 0:
            return True
        else:
            return False
    
        
    def __str__(self):    
        compactString = ""
        for i in range(0,len(self.lst),2):
            if i + 1 < len(self.lst):
                compactString += "[" + str(self.lst[i]) + "," + str(self.lst[i+1] - 1) +"]" + " U "
            
            #Odd length list: add MAX in the last closed interval
            
            else:
                compactString += "[" + str(self.lst[i]) + "," + str(MAX) + "]" + " U "
        
        if len(self.lst) == 0:
            return None
        else:
            return compactString[:-2]   #Slicing to remove final union symbol
    


if __name__ == "__main__":
    
    """
    mycl1 = CompactList([])
    print(mycl1.lst)
    print(mycl1.cardinality())
    mycl1_comp = mycl1.complement()
    print(mycl1.isEmpty())
    
    mycl2 = CompactList([3,4,5,8,9])
    print(mycl2.lst)
    print(mycl2.cardinality())
    #print(mycl2, "contains 4:",mycl2.contains(4)) 
    
    mycl2_comp = mycl2.complement()
    print(mycl2_comp.lst)
    
    mycl4 = CompactList([999,998,1000])
    print(mycl4.lst)
    print(mycl4.cardinality())
    
    mycl4_comp = mycl4.complement()
    print(mycl4_comp.lst)
    
    mycl5 = CompactList([])
    mycl5.lst += [-1000,100,104,108]
    mycl5_comp = mycl5.complement()
    print(mycl5_comp.lst)


    """
    
    mycl6 = CompactList()
    mycl6.lst += [2,5,8,10]
    
    
    
    mycl7 = CompactList([])
    mycl7.lst += [-1000]
    
    mycl8 = CompactList([])
    mycl8.lst += [15,20]
    
    mycl9 = CompactList([])
    mycl9.lst += [1,8,10,18]
    
    mycl10 = CompactList([])
    mycl10.lst += [2,5,9]
    
    print(str(mycl6))  
    mycl6.insert(5)
    print(str(mycl6))
    

    """
    #print(mycl3.cardinality())

    mycl1 = mycl2.complement()
    print(mycl1.lst)
    print(mycl1)
    #print(mycl1.cardinality())
                           

    mycl1 = CompactList([MAX])
    print(mycl1.lst)
    print(mycl1)
    print(mycl1.cardinality())

    """






