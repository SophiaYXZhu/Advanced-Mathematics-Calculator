from itertools import permutations

def calculate(inp):
    modinp = stringToList(inp)
    length = len(modinp)
    i = length-1
    while(i>=0):
        if modinp[i]=="(":
            ret = []
            j=i+1
            while(modinp[j]!=")"):
                ret.append(modinp[j])
                f = modinp.pop(i)
            f = modinp.pop(j)
            simplified = calculate(ret)
            modinp.insert(i+1,simplified)
            f = modinp.pop(i)
        length = len(modinp)
        i-=1
    i = 0
    while(i<length):
        if modinp[i]=="'":
            f = modinp.pop(i)
            if modinp[i-1]=='1': modinp[i-1]='0'
            elif modinp[i-1]=='0': modinp[i-1]='1'
        length = len(modinp)
        i+=1
    i = 0
    while(i<length):
        if modinp[i]=="*":
            calculated = andaction(modinp[i-1],modinp[i+1])
            f = modinp.pop(i-1)
            f = modinp.pop(i-1)
            modinp[i-1] = calculated
        length = len(modinp)
        i+=1
    i = 0
    while(i<length):
        if modinp[i]=="+":
            calculated = oraction(modinp[i-1],modinp[i+1])
            f = modinp.pop(i-1)
            f = modinp.pop(i-1)
            f = modinp.pop(i-1)
            modinp.insert(i-1,calculated)
        length = len(modinp)
        i+=1
    while(len(modinp)>1):
        modinp = stringToList(calculate(modinp))
    return(listToString(modinp))
def listToString(lis):
    string = ""
    for i in lis:
        string +=i
    return string
def stringToList(string):
    lis = []
    for i in string:
        lis.append(i)
    return lis
def andaction(a,b):
    if a==b=='1': return '1'
    else: return '0'
def oraction(a,b):
    if a==b=='0': return '0'
    else: return '1'
def permutate(variables):
    num = len(variables)
    numlis = []
    permutationlist = []
    last = ()
    for i in range(num):
        numlis.append(str(i))
    for i in range(num+1):
        newnumlis = []
        for j in range(num):
            if int(numlis[j])<i: newnumlis.append('0')
            else: newnumlis.append('1')
        perms = permutations(newnumlis) 
        for k in list(perms): 
            if permutationlist.count(k)==0: permutationlist.append(k)
    for i in range(len(permutationlist)):
        permutationlist[i] = list(permutationlist[i])
    return permutationlist

def output(request):
    inputvar = request.form.get("formula")
    result = {}
    result.update({"formula": inputvar})
    if len(inputvar) > 1 and ('+' not in inputvar and '*' not in inputvar and '\'' not in inputvar and ')' not in inputvar and '(' not in inputvar):
        message = 'The input is not in correct format for calculation!'
        result.update({"message": message})
        return result
    if not inputvar[0].isalpha() and inputvar[0] != '(':
        message = 'The input is not in correct format for calculation!'
        result.update({"message": message})
        return result
    if not inputvar[len(inputvar)-1].isalpha() and inputvar[len(inputvar)-1] != '\'' and inputvar[len(inputvar)-1] != ')':
        message = 'The input is not in correct format for calculation!'
        result.update({"message": message})
        return result
    for i in range(len(inputvar)):
        if inputvar[i] not in ["+", "*", "'", '(', ')'] and not inputvar[i].isalpha():
            message = 'The input is not in correct format for calculation!'
            result.update({"message": message})
            return result
        if i+1 < len(inputvar) and ((inputvar[i].isalpha() and inputvar[i+1] not in ["+", "*", "'", ')', '(']) or (inputvar[i] in ["+", "*"] and (not inputvar[i+1].isalpha() and inputvar[i+1] != '(')) or (inputvar[i] == ')' and inputvar[i+1] not in ['+', '*', '\'']) or (inputvar[i] == '\'' and inputvar[i+1] not in ['+', '*', ')']) or (inputvar[i] == '(' and not inputvar[i+1].isalpha())): 
            message = 'The input is not in correct format for calculation!'
            result.update({"message": message})
            return result
    variables = []
    for i in inputvar:
        if i !="(" and i!=")" and i!="+" and i!="*" and i!="'" and i!="1" and i!="0" and variables.count(i)==0:
            variables.append(i)
    perm = permutate(variables)
    steps = []
    final = []
    key_order = []
    for i in perm:
        inputa = list(inputvar)
        for j in range(len(variables)):
            for character in range(len(inputa)):
                if inputa[character]==variables[j]: 
                    inputa[character]=i[j]
        steps.append(listToString(inputa))
        final.append(calculate(listToString(inputa)))

    for i in range(len(variables)):
        temp_li = []
        key_order.append(variables[i])
        for j in range(len(perm)):
            temp_li.append(int(perm[j][i]))
            result.update({
                variables[i] : temp_li
            })
    key_order.append('"'+inputvar+'"')
    key_order.append('result')
    result.update({
        "\""+inputvar+"\"": steps, 
        'result' : final,
        "key_order": key_order
    })
    return result