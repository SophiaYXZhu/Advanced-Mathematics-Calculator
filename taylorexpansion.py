import math
import re

def listToString(lis): # from Cynthia
    string = ""
    for i in lis:
        string +=i
    return string
def stringToList(string):
    lis = []
    for i in string:
        lis.append(i)
    return lis

def factorial(n):
    product = 1
    if n >= 2:
        for i in range(2, n+1):
            product *= i
    return product

def strToFloat(a:str): # make sure when a1 or a2 = ""
    if a == "":
        a = 0.0
    else:
        a = float(a)
    return a

def derivative(item, variable):
    ### STRIP
    first_half = 0
    strip = False
    if item[0] == '(' and item[len(item)-1] == ')':
        strip = True
        for i in range(len(item)):
            if item[i] == '(':
                first_half += 1
            elif item[i] == ')':
                first_half -= 1
                if (i != len(item)-1 and first_half == 0):
                    strip = False
    # if item[0] == '(' and item[len(item)-1] == ')':
    if strip:
        item = item[1:len(item)-1]
    ###
    try:
        int(item)
        constant = True
    except ValueError:
        constant = False
    if constant:
        item = ''
        return item
    elif not constant:
        result_string = ''
        coefficient = re.match(r"-?\d+",item)
        if coefficient != None and coefficient.group(0) == item[:len(coefficient.group(0))] and (item[len(coefficient.group(0))] == variable or item[len(coefficient.group(0))] == '('):
            coefficient = coefficient.group(0)
            coefficient_exist = True
        elif item[0] == '-' and not item[1].isdigit():
            coefficient = '-1'
            coefficient_exist = '-1'
        else:
            coefficient = '1'
            coefficient_exist = False
        ### QUOETIENT
        quotient = False
        if '/' in item:
            quotient = True
            for i in range(len(item)):
                if item[i] == '/':
                    break
            denominator = item[i+1:]
            numerator = item[:i]
            item = numerator+'('+denominator+')^(-1)'
        ### PRODUCT RULE
        product = False
        if '*' in item:
            product = True
        if product:
            if coefficient_exist:
                item = item.strip(coefficient)
            elif coefficient_exist == '-1':
                item = item.strip('-')
            item_result = ''
            parts = item.split('*')
            for i in range(len(parts)):
                temp = parts.copy()
                temp.remove(parts[i])
                # combine the other parts together
                temp = '*'.join(temp)
                if i != len(parts)-1:
                    item_result += derivative(parts[i], variable)+'*'+temp+'+'
                else:
                    item_result += derivative(parts[i], variable)+'*'+temp
            if coefficient:
                item_result = '('+coefficient +'('+ item_result + '))'
            elif coefficient == '-1':
                item_result = '(-(' + item_result + '))'
            else:
                item_result = '('+item_result+')'
            return item_result
        ###
        # a(bx^c) / a(b/(x^c))
        check_exp = re.match(r"(\()?(-)?\d*(\.)?\d*.*[\^]*\d*(\))?", item)
        # aln(x)
        check_ln = re.match(r"(\()?(-)?\d*(\.)?\d*(ln\(){1}.*[\)]{1}(\))?", item)
        # log(a)(x)
        check_loga = re.match(r"(\()?(-)?\d*(\.)?\d*(log\(){1}\d+(\)\(){1}.*[\)]{1}(\))?", item)
        # a(b^x)
        check_ax = re.match(r"(-)?\d*(.)?\d*(\()\d+(.)?\d*(\)\^\().*(\))", item)
        # a(e^x)
        check_ex = re.match(r"(\()?(-)?\d*(\.)?\d*(\()?(e\^){1}.*[\)]{1}(\))?", item)
        # sin(x)
        check_sin = re.match(r"(\()?(-)?\d*(\.)?\d*(sin\(){1}.*(\)){1}(\))?", item)
        # cos(x)
        check_cos = re.match(r"(\()?(-)?\d*(\.)?\d*(cos\(){1}.*(\)){1}(\))?", item)
        # tan(x)
        check_tan = re.match(r"(\()?(-)?\d*(\.)?\d*(tan\(){1}.*(\)){1}(\))?", item)
        # sec(x)
        check_sec = re.match(r"(\()?(-)?\d*(\.)?\d*(sec\(){1}.*(\)){1}(\))?", item)
        # csc(x)
        check_csc = re.match(r"(\()?(-)?\d*(\.)?\d*(csc\(){1}.*(\)){1}(\))?", item)
        # cot(x)
        check_cot = re.match(r"(\()?(-)?\d*(\.)?\d*(cot\(){1}.*(\)){1}(\))?", item)
        # arcsin(x)
        check_asin = re.match(r"(\()?(-)?\d*(\.)?\d*(arcsin\(){1}.*(\)){1}(\))?", item)
        # arccos(x)
        check_acos = re.match(r"(\()?(-)?\d*(\.)?\d*(arccos\(){1}.*(\)){1}(\))?", item)
        # arctan(x)
        check_atan = re.match(r"(\()?(-)?\d*(\.)?\d*(arctan\(){1}.*(\)){1}(\))?", item)
        # arcsec(x)
        check_asec = re.match(r"(\()?(-)?\d*(\.)?\d*(arcsec\(){1}.*(\)){1}(\))?", item)
        # arccsc(x)
        check_acsc  =re.match(r"(\()?(-)?\d*(\.)?\d*(arccsc\(){1}.*(\)){1}(\))?", item)
        # arccot(x)
        check_acot = re.match(r"(\()?(-)?\d*(\.)?\d*(arccot\(){1}.*(\)){1}(\))?", item)
        ln_model = False
        loga_model = False
        exponent_model = False
        ax_model = False
        ex_model = False
        multiply_rule = False
        quotient_rule = False
        sin_model = False
        cos_model = False
        tan_model = False
        sec_model = False
        csc_model = False
        cot_model = False
        asin_model = False
        acos_model = False
        atan_model = False
        asec_model = False
        acsc_model = False
        acot_model = False
        if check_ln != None:
            ln_model = True
        elif check_loga != None:
            loga_model = True
        elif check_ax != None:
            ax_model = True
        elif check_ex != None:
            ex_model = True
        elif check_sin != None:
            sin_model = True
        elif check_cos != None:
            cos_model = True
        elif check_tan != None:
            tan_model = True
        elif check_sec != None:
            sec_model = True
        elif check_csc != None:
            csc_model = True
        elif check_cot != None:
            cot_model = True
        elif check_asin != None:
            asin_model = True
        elif check_acos != None:
            acos_model = True
        elif check_atan != None:
            atan_model = True
        elif check_asec != None:
            asec_model = True
        elif check_acsc != None:
            acsc_model = True
        elif check_acot != None:
            acot_model = True
        elif check_exp != None:
            exponent_model = True
        if ln_model:
            if coefficient_exist == True:
                ln = item[len(coefficient):]
            elif coefficient_exist == '-1':
                ln = item[1:]
            else:
                ln = item
            in_ln = ln.strip('ln(')
            in_ln = in_ln.strip(')')
            part_b = derivative(in_ln, variable)
            if coefficient != '1':
                item = '('+coefficient+'(1/('+in_ln+'))*('+part_b+'))'
            else:
                item = '(1/('+in_ln+'))*('+part_b+')'
        elif loga_model:
            if coefficient_exist == True:
                loga = item[len(coefficient):]
            elif coefficient_exist == '-1':
                loga = item[1:]
            else:
                loga = item
            a = loga.strip('log(')
            a = a[:len(a)-1]
            for i in range(len(a)):
                if a[i] == ')':
                    break
            b = a[:i]
            content = a[i+2:]
            content_de = derivative(content, variable)
            if content == variable:
                item = '('+coefficient+'(1/('+variable+'*ln('+b+')))'
            else:
                item = '('+coefficient+'(1/(('+content+')*ln('+b+')))*'+content_de+')'
        elif ax_model:
            if coefficient_exist == True:
                ax = item[len(coefficient):]
            elif coefficient_exist == '-1':
                ax = item[1:]
            else:
                ax = item
            for i in range(len(ax)):
                if ax[i] == '^':
                    break
            base = ax[:i]
            exponent = ax[i+1:]
            if exponent != variable:
                de_exponent = derivative(exponent, variable)
                item = '('+coefficient+'(ln('+base+')*'+base+'^('+exponent+')*('+de_exponent+')))'
            else:
                item = '('+coefficient+'(ln('+base+')*'+base+'^('+exponent+')))'
        elif ex_model:
            if coefficient_exist == True:
                ex = item[len(coefficient):]
            elif coefficient_exist == '-1':
                ex = item[1:]
            else:
                ex = item
            exponent = ex[2:]
            if exponent == variable:
                item = '('+item+')'
            else:
                de_content = derivative(exponent, variable)
                item = '('+item+'*'+de_content+')'
        elif sin_model:
            if coefficient_exist == True:
                sin = item[len(coefficient):]
            elif coefficient_exist == '-1':
                sin = item[1:]
            else:
                sin = item
            if sin[0] == '(' and sin[len(sin)-1] == ')' and sin[len(sin)-2] == ')':
                sin = sin[1:len(sin)-1]
            content = sin[4:len(sin)-1]
            de_content = derivative(content, variable)
            if content != variable:
                item = '('+coefficient+'(cos('+content+')*('+de_content+')))'
            else:
                item = '('+coefficient+'(cos('+variable+')*('+de_content+'))'
        elif cos_model:
            if coefficient_exist == True:
                cos = item[len(coefficient):]
            elif coefficient_exist == '-1':
                cos = item[1:]
            else:
                cos = item
            if cos[0] == '(' and cos[len(cos)-1] == ')' and cos[len(cos)-1] != ')':
                cos = cos[1:len(cos)-1]
            content = cos[4:len(cos)-1]
            de_content = derivative(content, variable)
            if content != variable:
                item = '('+coefficient+'(-sin('+content+')*('+de_content+')))'
            else:
                item = '('+coefficient+'(-sin('+variable+')*('+de_content+')))'
        elif tan_model:
            if coefficient_exist == True:
                tan = item[len(coefficient):]
            elif coefficient_exist == '-1':
                tan = item[1:]
            else:
                tan = item
            if tan[0] == '(' and tan[len(tan)-1] == ')' and tan[len(tan)-1] != ')':
                tan = tan[1:len(tan)-1]
            content = tan[4:len(tan)-1]
            de_content = derivative(content, variable)
            if content != variable:
                item = '('+coefficient+'(sec('+content+')^2*('+de_content+')))'
            else:
                item = '('+coefficient+'(sec('+variable+')^2*('+de_content+')))'
        elif sec_model:
            if coefficient_exist == True:
                sec = item[len(coefficient):]
            elif coefficient_exist == '-1':
                sec = item[1:]
            else:
                sec = item
            if sec[0] == '(' and sec[len(sec)-1] == ')' and sec[len(sec)-1] != ')':
                sec = sec[1:len(sec)-1]
            content = sec[4:len(sec)-1]
            de_content = derivative(content, variable)
            if content != variable:
                item = '('+coefficient+'(sec('+content+')*tan('+content+')*('+de_content+')))'
            else:
                item = '('+coefficient+'(sec('+variable+')*tan('+variable+')*('+de_content+')))'
        elif csc_model:
            if coefficient_exist == True:
                csc = item[len(coefficient):]
            elif coefficient_exist == '-1':
                csc = item[1:]
            else:
                csc = item
            if csc[0] == '(' and csc[len(csc)-1] == ')' and csc[len(csc)-1] != ')':
                csc = csc[1:len(csc)-1]
            content = csc[4:len(sec)-1]
            de_content = derivative(content, variable)
            if content != variable:
                item = '('+coefficient+'(-csc('+content+')*cot('+content+')*('+de_content+')))'
            else:
                item = '('+coefficient+'(-csc('+variable+')*cot('+variable+')*('+de_content+')))'
        elif cot_model:
            if coefficient_exist == True:
                cot = item[len(coefficient):]
            elif coefficient_exist == '-1':
                cot = item[1:]
            else:
                cot = item
            if cot[0] == '(' and cot[len(cot)-1] == ')' and cot[len(cot)-1] != ')':
                cot = cot[1:len(cot)-1]
            content = cot[4:len(cot)-1]
            de_content = derivative(content, variable)
            if content != variable:
                item = '('+coefficient+'(-csc('+content+')^2*('+de_content+')))'
            else:
                item = '('+coefficient+'(-csc('+variable+')^2*('+de_content+')))'
        elif asin_model:
            if coefficient_exist == True:
                asin = item[len(coefficient):]
            elif coefficient_exist == '-1':
                asin = item[1:]
            else:
                asin = item
            if asin[0] == '(' and asin[len(asin)-1] == ')' and asin[len(asin)-1] != ')':
                asin = asin[1:len(asin)-1]
            content = asin[7:len(asin)-1]
            de_content = derivative(content, variable)
            if content != variable:
                item = '('+coefficient+'((1/(1-('+content+')^2)^(0.5))*('+de_content+')))'
            else:
                item = '('+coefficient+'((1/(1-'+variable+'^2)^(0.5))*('+de_content+')))'
        elif acos_model:
            if coefficient_exist == True:
                acos = item[len(coefficient):]
            elif coefficient_exist == '-1':
                acos = item[1:]
            else:
                acos = item
            if acos[0] == '(' and acos[len(acos)-1] == ')' and acos[len(acos)-1] != ')':
                acos = acos[1:len(acos)-1]
            content = acos[7:len(acos)-1]
            de_content = derivative(content, variable)
            if content != variable:
                item = '('+coefficient+'((-1/(1-('+content+')^2)^(0.5))*('+de_content+')))'
            else:
                item = '('+coefficient+'((-1/(1-'+variable+'^2)^(0.5))*('+de_content+')))'
        elif atan_model: # NOT DONE
            if coefficient_exist == True:
                atan = item[len(coefficient):]
            elif coefficient_exist == '-1':
                atan = item[1:]
            else:
                atan = item
            if atan[0] == '(' and atan[len(atan)-1] == ')' and atan[len(atan)-1] != ')':
                atan = atan[1:len(atan)-1]
            content = atan[7:len(atan)-1]
            de_content = derivative(content, variable)
            if content != variable:
                item = '('+coefficient+'((1/(1+('+content+')^2))*('+de_content+')))'
            else:
                item = '('+coefficient+'((1/(1+'+variable+'^2))*('+de_content+')))'
        elif asec_model:
            if coefficient_exist == True:
                asec = item[len(coefficient):]
            elif coefficient_exist == '-1':
                asec = item[1:]
            else:
                asec = item
            if asec[0] == '(' and asec[len(asec)-1] == ')' and asec[len(asec)-1] != ')':
                asec = asin[1:len(asec)-1]
            content = asec[7:len(asec)-1]
            de_content = derivative(content, variable)
            if content != variable:
                item = '('+coefficient+'((1/(|'+content+'|*('+content+')^2-1)^(0.5)))*('+de_content+')))'
            else:
                item = '('+coefficient+'((1/(|'+variable+'|*(x^2-1)^(0.5))*('+de_content+')))'
        elif acsc_model:
            if coefficient_exist == True:
                acsc = item[len(coefficient):]
            elif coefficient_exist == '-1':
                acsc = item[1:]
            else:
                acsc = item
            if acsc[0] == '(' and acsc[len(acsc)-1] == ')' and acsc[len(acsc)-1] != ')':
                acsc_model = acsc[1:len(acsc)-1]
            content = acsc[7:len(acsc)-1]
            de_content = derivative(content, variable)
            if content != variable:
                item = '('+coefficient+'((-1/(|'+content+'|*(('+content+')^2-1)^(0.5))*('+de_content+')))'
            else:
                item = '('+coefficient+'((-1/(|'+variable+'|*(x^2-1))^(0.5))*('+de_content+')))'
        elif acot_model: # NOT DONE
            if coefficient_exist == True:
                acot = item[len(coefficient):]
            elif coefficient_exist == '-1':
                acot = item[1:]
            else:
                acot = item
            if acot[0] == '(' and acot[len(acot)-1] == ')' and acot[len(acot)-1] != ')':
                acot = acot[1:len(acot)-1]
            content = acot[7:len(acot)-1]
            de_content = derivative(content, variable)
            if content != variable:
                item = '('+coefficient+'((-1/(1+('+content+')^2))*('+de_content+')))'
            else:
                item = '('+coefficient+'((-1/(1+'+variable+'^2))*('+de_content+')))'
        elif exponent_model:
            exponent_idx = False
            for i in range(len(item)):
                if item[i] == '^':
                    exponent_idx = i # the last '^'
            if exponent_idx != False:
                exponent = item[exponent_idx+1:]
                exponent = exponent.strip(')')
                exponent = exponent.strip('(')
            else:
                return coefficient
            if exponent == '1':
                return coefficient
            if coefficient_exist:
                content_init = list(item)[len(coefficient):exponent_idx]
            elif not coefficient_exist:
                content_init = list(item)[:exponent_idx]
            content = ''
            for i in content_init:
                content += i
            # calculate derivative
            new_co = str(int(exponent)*int(coefficient))
            if str(int(exponent)-1)[0] == '-':
                new_ex = '^('+str(int(exponent)-1)+')'
            elif str(int(exponent)-1)[0].isdigit():
                new_ex = '^'+str(int(exponent)-1)
            if content != variable:
                new_content = derivative(content,variable)
                item = '('+new_co+'('+content+')'+new_ex+'*('+new_content+'))'
            else:
                item = '('+new_co+variable+new_ex+')'
        return item

def combine(item, variable):
    for i in range(len(item)):
        pre_able = True
        post_able = True
        if i-1 >= 0:
            try:
                int(item[i-1])
            except ValueError:
                pre_able = False
        if i+1 < len(item):
            try:
                int(item[i+1])
            except ValueError:
                post_able = False
        if item[i] == '-' and ((i-1 >= 0 and (item[i-1] == variable or item[i-1] == ')')) or pre_able) and ((i+1 < len(item) and (item[i+1] == variable or item[i+1] == '(')) or post_able):
            part_a = item[:i]
            part_b = item[i+1:]
            mid = '+-'
            item = part_a+mid+part_b
    item_init = item.split('+')
    for i in item_init:
        if i == '':
            item_init.remove(i)
    ### OUTPUT DERIVATIVE
    item = []
    for i in item_init:
        item.append(derivative(i, variable))
    result = ''
    for i in range(len(item)):
        if i != 0 and item[i] != '':
            result += '+'+item[i]
        elif i == 0:
            result += item[i]
    return result



def calculation(exp):
    # calculated = False
    # while not calculated:
    i = 0
    rec = exp
    while i < len(exp):
        count = 0
        if exp[i] == "(":
            i += 1
            calc = ""
            while i < len(exp) and (exp[i] != ")" or count != 0): # calculating the things inside the parenthesis
                if exp[i] == "(":  # record the parentheses inside the parenthesis
                    count += 1
                if exp[i] == ")":
                    count -= 1
                calc += exp[i]
                i += 1
            # print("calc: "+calc)
            check = False # check if inside the parenthesis is just a number
            for j in range(len(calc)): # if the parenthesis contains not only a number
                if not (ord(calc[j])>=48 and ord(calc[j])<=57 or calc[j] == "." or calc[j]=="-" and j == 0):
                    check = True
            if ord(exp[i-len(calc)-2])>=97 and ord(exp[i-len(calc)-2])<=122:
                check = False
            if check == True:
                replacement = calculation(calc)
                if ord(exp[i-len(calc)-2])>=97 and ord(exp[i-len(calc)-2])<=122 or exp[i-len(calc)-2]=="(":
                    rec = rec.replace(calc, replacement)
                else:
                    rec = rec.replace(("("+calc+")"), replacement)
                exp = rec
                i = 0
            elif i >= 2+len(calc): # e.g. sin((x))
                if exp[i-len(calc)-1]=="(" and (not (ord(exp[i-len(calc)-3])>=97 and ord(exp[i-len(calc)-3])<=122)):
                #     rec = rec.replace(("("+calc+")"), calc)
                # # if not (ord(exp[i-len(calc)-2])>=97 and ord(exp[i-len(calc)-2])<=122) or exp[i-len(calc)-2]=="(": # if it is only a number w/ ()
                #     print("rec_before: "+rec)
                    rec = stringToList(rec) # replacing
                    insert = []
                    for j in calc:
                        insert.append(j)
                    # print(insert)
                    index = i-len(calc)-1
                    # print("index: "+str(index))
                    while insert != []:
                        rec[index] = insert[0]
                        insert.pop(0)
                        index += 1
                    rec.pop(index)
                    rec.pop(index)
                    rec = listToString(rec)
                    # print("rec_after: "+rec)
                    exp = rec
                #     i = 0

                # rec = rec.replace(("("+calc+")"), calc)
        i += 1
        # calculated = True
        # for j in rec:
        # 	if not (ord(j)>=48 and ord(j)<=57) and (j == "-" and rec.index(j) != 0) and not j==".":
        # 		calculated = False



    i = 0
    while i < len(exp)-4:
        a1 = ""
        a2 = ""
        if exp[i] == "l" and exp[i+1] == "o": # log
            i2 = i + 4
            while exp[i2] != ")":
                a1 += exp[i2]
                i2 += 1
            i2 += 2
            while exp[i2] != ")":
                a2 += exp[i2]
                i2 += 1
            i = i2
            b1 = strToFloat(a1)
            b2 = strToFloat(a2)
            if b2 <= 0 or b1 <= 0:
                return "Input error!"
            else:
                sub_result = round(math.log(b2, b1), 5)
                rec = rec.replace(("log("+a1+")("+a2+")"), str(sub_result))
                exp = rec
                i = 0

        if exp[i] == "l" and exp[i+1] == "n": # ln
            i2 = i + 3
            while exp[i2] != ")":
                a1 += exp[i2]
                i2 += 1
            i = i2
            b1 = strToFloat(a1)
            if b1 <= 0:
                return "Input error!"
            else:
                sub_result = round(math.log(b1, math.e), 5)
                rec = rec.replace(("ln("+a1+")"), str(sub_result))
                exp = rec
                i = 0

        if exp[i] == "c" and exp[i+2] == "s": # cos
            if exp[i+3] == "(":
                i2 = i+4
                # print(exp)
                while exp[i2] != ")":
                    if ord(exp[i2])>=48 and ord(exp[i2])<= 57 or exp[i2]==".":
                        a1 += exp[i2]
                    i2 += 1
                i = i2
                b1 = strToFloat(a1)
                sub_result = round(math.cos(b1), 5)
                rec = rec.replace(("cos("+a1+")"), str(sub_result))
                exp = rec
                i = 0
            else:
                i2 = i+3
                while i2<len(exp) and ord(exp[i2])>=48 and ord(exp[i2])<=57 or exp[i2]==".":
                    a1 += exp[i2]
                    i2 += 1
                i = i2
                b1 = strToFloat(a1)
                sub_result = round(math.cos(b1), 5)
                rec = rec.replace(("cos"+a1), str(sub_result))
                exp = rec

        if exp[i] == "s" and exp[i+1] == "i": # sin
            i2 = i+4
            while exp[i2] != ")":
                a1 += exp[i2]
                i2 += 1
            i = i2
            b1 = strToFloat(a1)
            sub_result = round(math.sin(b1), 5)
            rec = rec.replace(("sin("+a1+")"), str(sub_result))
            exp = rec
            i = 0

        if exp[i] == "t": # tan
            i2 = i+4
            while exp[i2] != ")":
                a1 += exp[i2]
                i2 += 1
            i = i2
            b1 = strToFloat(a1)
            sub_result = round(math.tan(b1), 5)
            rec = rec.replace(("tan("+a1+")"), str(sub_result))
            exp = rec
            i = 0

        if exp[i] == "c" and exp[i+2] == "t": # cot
            i2 = i+4
            while exp[i2] != ")":
                a1 += exp[i2]
                i2 += 1
            i = i2
            b1 = strToFloat(a1)
            sub_result = round((1/(math.tan(b1))), 5)
            rec = rec.replace(("cot("+a1+")"), str(sub_result))
            exp = rec
            i = 0


        if exp[i] == "s" and exp[i+1] == "e": # sec
            i2 = i+4
            while exp[i2] != ")":
                a1 += exp[i2]
                i2 += 1
            i = i2
            b1 = strToFloat(a1)
            sub_result = round((1/(math.cos(b1))), 5)
            rec = rec.replace(("sec("+a1+")"), str(sub_result))
            exp = rec
            i = 0

        if exp[i] == "c" and exp[i+2] == "c": # csc
            i2 = i+4
            while exp[i2] != ")":
                a1 += exp[i2]
                i2 += 1
            i = i2
            b1 = strToFloat(a1)
            sub_result = round((1/(math.sin(b1))), 5)
            rec = rec.replace(("csc("+a1+")"), str(sub_result))
            # print("csc: "+rec)
            exp = rec
            i = 0
        i += 1

    i = 1
    while i < len(exp) - 1:  # check the exponents (first in calculation)
        a1 = ""
        a2 = ""
        if exp[i] == "^":
            if exp[i + 1] == "(":
                i2 = i - 1
                while i2 >= 0 and (ord(exp[i2]) >= 48 and ord(exp[i2]) <= 57 or exp[i2] == "-" or exp[i2] == "."):
                    a1 = exp[i2] + a1
                    i2 -= 1
                i2 = i + 2
                while i2 < len(exp) and exp[i2] != ")" or exp[i2] == "-" or exp[i2] == ".":
                    a2 += exp[i2]
                    i2 += 1
                i = i2
                b1 = strToFloat(a1)
                b2 = strToFloat(a2)
                sub_result = b1 ** b2
                rec = rec.replace((a1 + "^(" + a2 + ")"), str(sub_result))
            else:
                # print("exp: "+exp)
                i2 = i - 1
                while i2 >= 0 and (ord(exp[i2]) >= 48 and ord(exp[i2]) <= 57 or exp[i2] == "-" or exp[i2] == "."):  # record the first number
                    a1 = exp[i2] + a1
                    i2 -= 1
                i2 = i + 1
                while i2 < len(exp) and (ord(exp[i2]) >= 48 and ord(exp[i2]) <= 57 or exp[i2] == "." or exp[i2] == "-"):
                    a2 += exp[i2]
                    i2 += 1
                i = i2
                # print("a1: "+a1)
                # print("a2: "+a2)
                b1 = strToFloat(a1)
                b2 = strToFloat(a2)
                sub_result = b1 ** b2
                rec = rec.replace((a1 + "^" + a2), str(sub_result))
        i += 1
    exp = rec

    exp = rec
    i = 1
    while i < len(exp):
        a1 = ""
        a2 = ""

        if exp[i] == "*": # multiplication
            # print("exp_mult: "+exp)
            i2 = i-1
            while i2 >= 0 and (ord(exp[i2])>=48 and ord(exp[i2])<=57 or exp[i2]=="." or exp[i2]=="-"):
                a1 = exp[i2] + a1
                i2 -= 1
            i2 = i+1
            while i2 < len(exp) and (ord(exp[i2])>=48 and ord(exp[i2])<=57 or exp[i2]=="." or exp[i2]=="-"):
                a2 += exp[i2]
                i2 += 1
            i = i2-1
            bp = 0
            times = 0
            while bp < len(a1) and times < 2: # for getting rid of multiple decimal points
                if a1[bp] == ".": times += 1
                bp += 1
            a1 = a1[:bp+1]
            # print("a1: "+a1)
            bp, times = 0, 0
            while bp < len(a2) and times < 2:
                if a2[bp] == ".": times += 1
                bp += 1
            # print(bp)
            a2 = a2[:bp+1]
            # print("a2: "+a2)
            b1 = strToFloat(a1) # converting and calculating
            b2 = strToFloat(a2)
            sub_result = round((b1*b2), 5)
            rec = rec.replace((a1+"*"+a2), str(sub_result))

        if exp[i] == "/": # division
            i2 = i-1
            while i2 >= 0 and (ord(exp[i2])>=48 and ord(exp[i2])<=57 or exp[i2]=="." or exp[i2] == "-"):
                a1 = exp[i2] + a1
                i2 -= 1
            i2 = i+1
            while i2 < len(exp) and (ord(exp[i2])>=48 and ord(exp[i2])<=57 or exp[i2]=="." or exp[i2] == "-"):
                a2 += exp[i2]
                i2 += 1
            i = i2-1
            b1 = strToFloat(a1)
            b2 = strToFloat(a2)
            if b2 == 0:
                return "Input error!"
            else:
                sub_result = round((b1/b2), 5)
                rec = rec.replace((a1+"/"+a2), str(sub_result))
        i += 1

    exp = rec
    # print("After all m and d" + rec)

    i= 1
    while i < len(exp)-1: # check the operators and calculate
        a1 = ""
        a2 = ""

        if exp[i] == "+": # addition
            i2 = i - 1
            while i2 >= 0 and (ord(exp[i2]) >= 48 and ord(exp[i2])<=57 or exp[i2] == "." or exp[i2] == "-"):  # record the first number
                a1 = exp[i2] + a1
                i2 -= 1
            i2 = i + 1
            while i2 < len(exp) and (ord(exp[i2]) >= 48 and ord(exp[i2]) <= 57 or exp[i2] == "."):
                a2 += exp[i2]
                i2 += 1
            i = i2-1
            b1 = strToFloat(a1)
            b2 = strToFloat(a2)
            sub_result = b1 + b2
            rec = rec.replace((a1 + "+" + a2), str(sub_result))
            exp = rec
            i = 0

        if exp[i] == "-" and i != 0: # subtraction
            i2 = i - 1
            while i2 >= 0 and (ord(exp[i2]) >= 48 and ord(exp[i2]) <= 57 or exp[i2] == "-" or exp[i2] == "."):  # record the first number
                a1 = exp[i2] + a1
                i2 -= 1
            i2 = i + 1
            while i2 < len(exp) and (ord(exp[i2]) >= 48 and ord(exp[i2])<=57 or exp[i2] == "."):
                a2 += exp[i2]
                i2 += 1
            i = i2-1
            b1 = strToFloat(a1)
            b2 = strToFloat(a2)
            sub_result = b1 - b2
            rec = rec.replace((a1 + "-" + a2), str(sub_result))
            exp = rec
            i = 0



        i += 1
    for j in range(len(rec)):
        # print(ord(rec[j]))
        if (ord(rec[j]) < 48 or ord(rec[j])) > 57 and (not rec[j] == ".") and not (rec[j] == "-" and j == 0) or rec[j]=="(" or rec[j]==")":
            rec = rec[0:j] + rec[(j + 1):]

    return rec

def substitution(item, variable, value): # calculate the function with the value
    lp = 0 # recording the number of parenthesis
    rp = 0
    for i in range(len(item)):
        if item[i] == "(": lp += 1
        if item[i] == ")": rp += 1
    item = stringToList(item)
    i = 0
    while lp > rp:
        if item[i] == "(":
            item.pop(i)
            i -= 1
            lp -= 1
        i += 1
    while rp > lp:
        if item[i] == ")":
            item.pop(i)
            i -= 1
            rp -= 1
        i += 1
    item = listToString(item)
    if value == "pi":
        value = math.pi
    elif value == "e":
        value = math.e
    i = 0
    lst = stringToList(item)
    while i < len(lst)-1: # detect all the hidden multiplication signs
        if (ord(lst[i])>=48 and ord(lst[i])<=57) and (ord(lst[i+1])>=97 and ord(lst[i+1])<=122 or lst[i+1]=="("):	# check if the the multiplication mark is hidden
            lst.insert((i+1), "*")
            i += 1
        if lst[i] == "-" and ((ord(lst[i+1])>=97 and ord(lst[i+1])<=122) or (ord(lst[i+1])>=48 and ord(lst[i+1])<=57) or lst[i+1]=="("): # if it is a hidden "-1*"
            # if lst[i-1] == "^": # if it is in the form of e.g. x^-1
            # 	lst.insert(i, "(")
            # 	i += 3
            # 	while i < len(lst) and (ord(lst[i])>=48 and ord(lst[i])<=57): # detect the number after "-", e.g. 1
            # 		i += 1
            # 	lst.insert(i, ")")
            # else:
            lst.insert((i+1), "1") # other cases with "-"
            lst.insert((i+2), "*")
            i += 2
        i += 1
    item = listToString(lst)

    exp = item.replace(variable, str(value)) # substitute the variables with the value
    # print("Substituted: " + exp)

    return exp





def taylor_series(item, variable, value, degree):
    degree = int(degree)
    result_dict= dict()
    result_dict.update({"expression": item})
    result_dict.update({"variable": variable})
    result_dict.update({"degree": degree})
    result_dict.update({"center": value})
    if degree < 0:
        result_dict.update({"message": "Degree / Center need be a positive number."})
        return reduct_dict
    else:
        result = calculation(substitution(item, variable, value))
        d = item
        for i in range(1, degree+1):
            # print(str(i) + "degree")
            d = combine(d, variable)
            # print("Derivative: " + d)
            # if calculation(substitution(d, variable, value))==0: # ***&&^%&
            # 	result += " + 0*(" + variable + "-" + str(value) + ")^" + str(i)
            # else:
            coeff = calculation(substitution(d, variable, value))

            if coeff == "":
                result += " + 0*(" + variable + "-" + str(value) + ")^" + str(i)
            else:
                coeff = round(float(coeff)/(factorial(i)), 5)
                result += " + " + str(coeff) + "*(" + variable + "-" + str(value) + ")^" + str(i)
            # print("re: "+result)
        result_dict.update({"result": result})
        return result_dict

# def check_parentheses(item, variable):
#     i = 0
#     n = ""
#     single = True
#     l = []
#     r = []
#     rec = item
#     while i < len(item):
#         if item[i] == "(":
#             while item[i] != ")":
#                 if item[i] == "(":
#                     n = ""
#                 else:
#                     n += item[i]
#                 i += 1
#         for j in n:
#             if ord(j)<48 or ord(j)>57 or not j=="-" or not j=="." or not j==variable:
#                 single = False
#
#     while i < len(item) and (r == [] or r[-1] != len(item)):
#         if item[i] == "(":
#             l.append(i)
#         elif item[i] == ")":
#             r.append(i)
#         i += 1
#     while l != [] and r != []:
#         break

print(taylor_series("sin(x)+cos(x)+x^2+0.5x", "x", "1", 2))
# print(taylor_series("tan(x)", "x", "1", 2))
# print(calculation(substitution("(1*(cos(x)*(1))", "x", 1)))
# print(calculation("(1*(cos(1)*(1))"))