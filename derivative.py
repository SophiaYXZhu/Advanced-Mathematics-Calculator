import re
import matplotlib.pyplot as plt
import numpy as np
from numpy import log as ln
from numpy import sin, cos, tan, arctan, arccos, arcsin

multi_ptn = re.compile(r"(\d+)([(|a-zA-Z])")
log_ptn = re.compile(r"log\((\d+)\)\((.+)\)")

def gen_image(result, variable, title, filename):
    x = np.linspace(-15, 15, 100)
    fig = plt.figure(figsize=(3, 3))
    if result.find(variable) != -1:
        result = log_ptn.sub(r"ln(\2)/ln(\1)", result)
        result = result.replace("^", "**")
        result = result.replace(")(", ")*(")
        # result = result.replace("csc(", "arcsin(")
        # result = result.replace("sec(", "arccos(")
        # result = result.replace("cot(", "arctan(")
        result = multi_ptn.sub(r"\1*\2", result)
        y = eval(result)
    else:
        a = eval(result)
        y=np.array([a] * len(x))
    plt.plot(x, y)
    plt.grid(True, linestyle=':')
    plt.title(title)
    plt.xlabel('x-axis')
    plt.ylabel('y-axis')
    plt.savefig('./static/{}'.format(filename), bbox_inches='tight')
    plt.clf()

def derivative(item, variable):
    # STRIP
    first_half = 0
    strip = False
    print(item)
    if item[0] == '(' and item[len(item)-1] == ')':
        strip = True
        for i in range(len(item)):
            if item[i] == '(':
                first_half += 1
            elif item[i] == ')':
                first_half -= 1
                if (i != len(item)-1 and first_half == 0):
                    strip = False
    if strip:
        item = item[1:len(item)-1]
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
        coefficient = re.match(r"-?\d+", item)
        if coefficient != None and coefficient.group(0) == item[:len(coefficient.group(0))] and (item[len(coefficient.group(0))] == variable or item[len(coefficient.group(0))] == '(' or  item[len(coefficient.group(0))] == '/' or item[len(coefficient.group(0)):len(coefficient.group(0))+3] in ['sin', 'cos', 'tan', 'cot', 'sec', 'csc'] or item[len(coefficient.group(0)):len(coefficient.group(0))+6] in ['arcsin', 'arccos', 'arctan', 'arccot', 'arccsc', 'arcsec']):
            coefficient = coefficient.group(0)
            coefficient_exist = True
        elif item[0] == '-' and not item[1].isdigit():
            coefficient = '-1'
            coefficient_exist = '-1'
        else:
            coefficient = '1'
            coefficient_exist = False
        # QUOETIENT
        quotient = False
        if '/' in item:
            quotient = True
            for i in range(len(item)):
                if item[i] == '/':
                    break
            denominator = item[i+1:]
            numerator = item[:i]
            item = numerator+'('+denominator+')^(-1)'
        # PRODUCT RULE
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
                item_result = '('+coefficient + '(' + item_result + '))'
            elif coefficient == '-1':
                item_result = '(-(' + item_result + '))'
            else:
                item_result = '('+item_result+')'
            return item_result
        ###
        # a(bx^c) / a(b/(x^c))
        check_exp = re.match(r"(\()?(-)?\d*(\.)?\d*.*[\^]*\d*(\))?", item)
        # aln(x)
        check_ln = re.match(
            r"(\()?(-)?\d*(\.)?\d*(ln\(){1}.*[\)]{1}(\))?", item)
        # log(a)(x)
        check_loga = re.match(
            r"(\()?(-)?\d*(\.)?\d*(log\(){1}\d+(\)\(){1}.*[\)]{1}(\))?", item)
        # a(b^x)
        check_ax = re.match(
            r"(-)?\d*(.)?\d*(\()\d+(.)?\d*(\)\^\().*(\))", item)
        # a(e^x)
        check_ex = re.match(
            r"(\()?(-)?\d*(\.)?\d*(\()?(e\^){1}.*[\)]{1}(\))?", item)
        # sin(x)
        check_sin = re.match(
            r"(\()?(-)?\d*(\.)?\d*(sin\(){1}.*(\)){1}(\))?", item)
        # cos(x)
        check_cos = re.match(
            r"(\()?(-)?\d*(\.)?\d*(cos\(){1}.*(\)){1}(\))?", item)
        # tan(x)
        check_tan = re.match(
            r"(\()?(-)?\d*(\.)?\d*(tan\(){1}.*(\)){1}(\))?", item)
        # sec(x)
        check_sec = re.match(
            r"(\()?(-)?\d*(\.)?\d*(sec\(){1}.*(\)){1}(\))?", item)
        # csc(x)
        check_csc = re.match(
            r"(\()?(-)?\d*(\.)?\d*(csc\(){1}.*(\)){1}(\))?", item)
        # cot(x)
        check_cot = re.match(
            r"(\()?(-)?\d*(\.)?\d*(cot\(){1}.*(\)){1}(\))?", item)
        # arcsin(x)
        check_asin = re.match(
            r"(\()?(-)?\d*(\.)?\d*(arcsin\(){1}.*(\)){1}(\))?", item)
        # arccos(x)
        check_acos = re.match(
            r"(\()?(-)?\d*(\.)?\d*(arccos\(){1}.*(\)){1}(\))?", item)
        # arctan(x)
        check_atan = re.match(
            r"(\()?(-)?\d*(\.)?\d*(arctan\(){1}.*(\)){1}(\))?", item)
        # arcsec(x)
        check_asec = re.match(
            r"(\()?(-)?\d*(\.)?\d*(arcsec\(){1}.*(\)){1}(\))?", item)
        # arccsc(x)
        check_acsc = re.match(
            r"(\()?(-)?\d*(\.)?\d*(arccsc\(){1}.*(\)){1}(\))?", item)
        # arccot(x)
        check_acot = re.match(
            r"(\()?(-)?\d*(\.)?\d*(arccot\(){1}.*(\)){1}(\))?", item)
        ln_model = False
        loga_model = False
        exponent_model = False
        ax_model = False
        ex_model = False
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
                print(coefficient, variable, b, 'loga')
                item = '('+coefficient+'(1/('+variable+'*ln('+b+'))))'
            else:
                item = '('+coefficient + \
                    '(1/(('+content+')*ln('+b+')))*'+content_de+')'
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
                item = '('+coefficient+'(ln('+base+')*'+base + \
                    '^('+exponent+')*('+de_exponent+')))'
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
                item = '('+coefficient+'(cos('+variable+')))'
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
                item = '('+coefficient+'(-sin('+variable+')))'
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
                item = '('+coefficient+'(sec('+variable+')^2))'
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
                item = '('+coefficient + \
                    '(sec('+content+')*tan('+content+')*('+de_content+')))'
            else:
                item = '('+coefficient+'(sec('+variable + \
                    ')*tan('+variable+')))'
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
                item = '('+coefficient+'(-csc('+content + \
                    ')*cot('+content+')*('+de_content+')))'
            else:
                item = '('+coefficient+'(-csc('+variable + \
                    ')*cot('+variable+')))'
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
                item = '('+coefficient+'(-csc('+variable+')^2))'
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
                item = '('+coefficient + \
                    '((1/((1-('+content+')^2)^(0.5)))*('+de_content+')))'
            else:
                item = '('+coefficient + \
                    '((1/((1-'+variable+'^2)^(0.5)))))'
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
                item = '('+coefficient + \
                    '((-1/((1-('+content+')^2)^(0.5)))*('+de_content+')))'
            else:
                item = '('+coefficient + \
                    '((-1/((1-'+variable+'^2)^(0.5)))))'
        elif atan_model:
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
                item = '('+coefficient + \
                    '((1/(1+('+content+')^2))*('+de_content+')))'
            else:
                item = '('+coefficient + \
                    '((1/(1+'+variable+'^2))))'
        elif asec_model:
            if coefficient_exist == True:
                asec = item[len(coefficient):]
            elif coefficient_exist == '-1':
                asec = item[1:]
            else:
                asec = item
            if asec[0] == '(' and asec[len(asec)-1] == ')' and asec[len(asec)-1] != ')':
                asec = asec[1:len(asec)-1]
            content = asec[7:len(asec)-1]
            de_content = derivative(content, variable)
            if content != variable:
                item = '('+coefficient+'((1/((|'+content + '|*('+content+')^2-1)^(0.5))))*('+de_content+')))'
            else:
                item = '('+coefficient + '((1/(|'+variable+'|*(x^2-1)^(0.5))))'
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
                item = '('+coefficient+'((-1/((|'+content + '|*(('+content+')^2-1))^(0.5)))*('+de_content+')))'
            else:
                item = '('+coefficient + '(-1/((|'+variable+'|*(x^2-1))^(0.5))))'
        elif acot_model:
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
                item = '('+coefficient + '((-1/(1+('+content+')^2))*('+de_content+')))'
            else:
                item = '('+coefficient + '((-1/(1+'+variable+'^2))))'
        elif exponent_model:
            exponent_idx = False
            for i in range(len(item)):
                if item[i] == '^':
                    exponent_idx = i  # the last '^'
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
            new_co = str(float(exponent)*float(coefficient))
            if str(float(exponent)-1)[0] == '-':
                new_ex = '^('+str(float(exponent)-1)+')'
            elif str(float(exponent)-1)[0].isdigit():
                new_ex = '^'+str(float(exponent)-1)
            if content != variable:
                new_content = derivative(content, variable)
                item = '('+new_co+'('+content+')'+new_ex+'*('+new_content+'))'
            else:
                item = '('+new_co+variable+new_ex+')'
        print(item)
        return item

def combine(item, variable, degree):
    # degree = int(degree)
    result_dict = dict()
    expression = item
    result_dict.update({"expression": expression})
    result_dict.update({"variable": variable})
    result = ""
    if not variable or not variable.isalpha() or len(variable) > 1:
        result_dict.update({"message": "Variable can only be 1 letter."})
    item_init = []
    first_par_idx = 0
    while first_par_idx < len(item):
        if item[first_par_idx] == '(':
            second_par = 0
            for j in range(first_par_idx+1, len(item)):
                if item[j] == '(':
                    second_par -= 1
                elif item[j] == ')':
                    second_par += 1
                if second_par == 1:
                    item_init.append(item[first_par_idx+1:j])
                    first_par_idx = j+2
                    break
        else:
            first_par_idx += 1
    #####
    print(item_init, 'item_init')
    for i in item_init:
        if i == '':
            item_init.remove(i)
    # OUTPUT DERIVATIVE
    item = []
    for i in item_init:
        item.append(derivative(i, variable))
    print(item)
    ####### GRAPHING
    result_for_graph = ''
    for i in range(len(item)):
        if i != 0 and item[i] != '':
            result_for_graph += '+'+item[i]
        elif i == 0:
            result_for_graph += item[i]
    try:
        title = "Origin {}".format(expression)
        filename = "derivative_origin.png"
        gen_image(expression, variable, title, filename)
        title = "Derivative of {}".format(expression)
        filename = "derivative_result.png"
        gen_image(result_for_graph, variable, title, filename)
    except Exception as e:
        print("Error gen_image:{}".format(e))
    ############
    ### SYNTAX
    item_li = []
    for k in range(len(item)):
        item_result_flagged = False
        i = 0
        item_result = item[k]
        while i < len(item_result):
            if item_result[i] == '/':
                if item_result[i-1].isdigit():
                    for idx, element in enumerate(item_result[:i][::-1]):
                        if item_result[:i][::-1][idx] == '(':
                            parta = item_result[i-idx:i]
                            big_first = i-idx
                            break
                elif item_result[i-1] == ')':
                    second_half = 0
                    for idx, element in enumerate(item_result[:i-1][::-1]):
                        if item_result[idx] == '(':
                            second_half -= 1
                        elif item_result[idx] == ')':
                            second_half += 1
                        if second_half == -1:
                            # part a is pure content
                            parta = item_result[i-idx-1:i-1] #i-idx-1
                            big_first = i - idx-1
                            break
                first_half = 0
                for j in range(len(item_result[i+2:])):
                    if item_result[i+2:][j] == '(':
                        first_half += 1
                    elif item_result[i+2:][j] == ')':
                        first_half -= 1
                    if first_half == -1:
                        partb = item_result[i+2:i+2+j]  # part b is pure content
                        big_last = i+2 + j
                        break
                # print(item_result[:big_first], parta, partb, item_result[big_last:], big_last, 'end')
                item_result = item_result[:big_first] + '{' + parta + '\over ' + partb + '}' + item_result[big_last+1:]
                item_result_flagged = True
            elif item_result[i] == '^':
                if item_result[i+1].isdigit():
                    for j in range(len(item_result[i+1:])):
                        if item_result[i+1:][j] in ['+', '*', '/', '(', ')']:
                            exponent = item_result[i+1:i+1+j]
                            break
                    if exponent == '1.0':
                        parta = item_result[:i]
                        partb = item_result[i+1+j:]
                        item_result = parta+partb
                    else:
                        check_int_flo = re.match(r"\d+(\.)?\d*", item_result[i+1:])
                        if check_int_flo != None:
                            if len(item_result[i+1:]) > len(check_int_flo.group(0)):
                                item_result = item_result[:i+1]+'{'+check_int_flo.group(0)+'}'+item_result[i+1:][len(check_int_flo.group(0)):]
                            else:
                                item_result = item_result[:i+1]+'{'+check_int_flo.group(0)+'}'
                elif item_result[i+1] == '(':
                    second_half= 0
                    for j in range(len(item_result[i+2:])):
                        if item_result[i+2:][j] == ')':
                            second_half -= 1
                        elif item_result[i+2:][j] == '(':
                            second_half += 1
                        if second_half == -1:
                            big_last = i+2+j
                            exponent = item_result[i+2:big_last]
                            break
                    parta = item_result[:i+1]
                    partb = item_result[big_last+1:]
                    item_result = parta + '{'+exponent+'}'+partb
            elif item_result[i:i+4] == 'log(':
                # UNFINISHED
                part_a = item_result[:i+3]
                for j in range(len(item_result[i+4:])):
                    if item_result[i+4:][j] == ')':
                        end_par = i+4+j
                        break
                base = item_result[i+4:end_par]
                part_b = item_result[end_par:]
                item_result = part_a + '_{'+ base + '}' + partb 
            i += 1
            # Flag item_result with \[ and \]
            item_result_flagged = False
            if item_result[0:2] == '\[' and item_result[len(item_result)-2:len(item_result)] == '\]':
                item_result_flagged = True 
            if not item_result_flagged:
                item_result = "\["+item_result+"\]"
        item_li.append(item_result)
    print(item_li)
    ###################
    for i in range(len(item_li)):
        if i != 0 and item_li[i] != '':
            result += '\[+\]'+item_li[i]
        elif i == 0:
            result += item_li[i]
    result_dict.update({"result": result})
    return result_dict