def integer(string):
 
    text=""
    numbers=""
    res=[]
    for i in string:
        if(i.isdigit()):
            numbers+=i
        else:
            text+=i
    res.append(text)
    res.append(numbers)
    
    return res[1]
