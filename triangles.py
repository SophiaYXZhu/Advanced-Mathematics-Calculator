# from flask import Flask, render_template, request, redirect
import math
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
import os

matplotlib.use('Agg')

if not os.path.exists("./static"):
    os.mkdir("./static")

def calculate(request):
    Two = False
    result = dict()
    decimals = request.form.get("decimals")
    result.update({"decimals": decimals})
    angle_a = request.form.get("angle_a")
    angle_b = request.form.get("angle_b")
    angle_c = request.form.get("angle_c")
    angles = [angle_a, angle_b, angle_c]
    result.update({ "angle_a": angle_a, "angle_b": angle_b, "angle_c": angle_c})
    side_a = request.form.get("side_a")
    side_b = request.form.get("side_b")
    side_c = request.form.get("side_c")
    sides = [side_a, side_b, side_c]
    result.update({"side_a": side_a, "side_b": side_b, "side_c": side_c})
    count = 0
    for i in range(3):
        if sides[i] == '':
            count += 1
        if angles[i] == '':
            count += 1
    if count > 3:
        result.update({"message": 'You have to enter at least 3 values for a triangle calculation!'})
        return result
    try:
        decimals = int(decimals)
    except ValueError:
        result.update({"message":'Please enter valid places of decimals to keep for your answers!'})
        return result
    for i in range(len(angles)):
        try:
            float(angles[i])
            is_float = True
        except ValueError:
            is_float = False
        if angles[i] == '':
            continue
        elif not is_float:
            result.update({"message": 'The measure of an angle must be an integer or float!!!'})
            return result
        elif float(angles[i]) <= 0 or float(angles[i]) >= 180:
            result.update({"message": 'The angle must be greater than zero or smaller than 180!!!'})
            return result
        else:
            angles[i] = float(angles[i])*math.pi/180

    for i in range(len(sides)):
        try:
            float(sides[i])
            is_float = True
        except:
            is_float = False
        if sides[i] == '':
            continue
        elif not is_float:
            result.update({"message": 'The length of a side must be an integer or float!!!'})
            return result
        elif float(sides[i]) <= 0:
            result.update({"message": 'The length of a side must be greater than zero!!!'})
            return result
        else:
            sides[i] = float(sides[i])
    if isinstance(sides[0], float) and isinstance(sides[1], float) and isinstance(sides[2], float) and (sides[0] + sides[1] <= sides[2] or sides[1] + sides[2] <= sides[0] or sides[2] + sides[0] <= sides[1]):
        result.update({"message": "The triangle's sides are impossible to form a triangle!!!"})
        return result
    part_angle_sum = 0
    count = 0
    for i in range(3):
        if isinstance(angles[i], float):
            part_angle_sum += angles[i]
            count += 1
    if count < 3 and (round(part_angle_sum, 3) < 0 or round(part_angle_sum, 3) >= math.pi):
        result.update({'message': "The triangle's angles are impossible to form a triangle!!!"})
        return result
    elif isinstance(angles[0], float) and isinstance(angles[1], float) and isinstance(angles[2], float) and round(angles[0]+angles[1]+angles[2], 3) != round(math.pi, 3):
        result.update({"message": "The triangle's angles are impossible to form a triangle!!!"})
        return result
    SAS = False
    SSA = False
    ASA = False
    SSS = False
    AAS = False
    AAA = False
    count = 0
    for i in angles:
        if isinstance(i, float):
            count += 1
    countb = 0
    for i in sides:
        if i == '':
            countb += 1
    if count == 3 and countb == 3:
        AAA = True
        result.update({"message": 'It is impossible to known from the given information!!!'})
        return result
    # SSS : cosine rule
    if isinstance(sides[2], float) and isinstance(sides[0], float) and isinstance(sides[1], float):
        SSS = True
    # SAS : cosine rule
    elif (isinstance(angles[0], float) and isinstance(sides[1], float) and isinstance(sides[2], float)) or (isinstance(angles[1], float) and isinstance(sides[0], float) and isinstance(sides[2], float)) or (isinstance(angles[2], float) and isinstance(sides[0], float) and isinstance(sides[1], float)):
        SAS = True
    # SSA : sine rule
    elif (isinstance(angles[0], float) and isinstance(sides[0], float) and isinstance(sides[2], float)) or (isinstance(angles[0], float) and isinstance(sides[0], float) and isinstance(sides[1], float)) or (isinstance(angles[1], float) and isinstance(sides[0], float) and isinstance(sides[1], float)) or (isinstance(angles[1], float) and isinstance(sides[2], float) and isinstance(sides[1], float)) or (isinstance(angles[2], float) and isinstance(sides[0], float) and isinstance(sides[2], float)) or (isinstance(angles[1], float) and isinstance(sides[2], float) and isinstance(sides[1], float)):
        SSA = True
    # ASA : sine rule
    elif (isinstance(angles[0], float) and isinstance(angles[2], float) and isinstance(sides[1], float)) or (isinstance(angles[1], float) and isinstance(angles[0], float) and isinstance(sides[2], float)) or (isinstance(angles[2], float) and isinstance(angles[1], float) and isinstance(sides[0], float)):
        ASA = True
    # AAS : sine rule
    elif (isinstance(angles[0], float) and isinstance(angles[1], float) and isinstance(sides[0], float)) or (isinstance(angles[0], float) and isinstance(angles[1], float) and isinstance(sides[1], float)) or (isinstance(angles[1], float) and isinstance(angles[2], float) and isinstance(sides[1], float)) or (isinstance(angles[1], float) and isinstance(angles[2], float) and isinstance(sides[2], float)) or (isinstance(angles[2], float) and isinstance(angles[0], float) and isinstance(sides[2], float)) or (isinstance(angles[2], float) and isinstance(angles[0], float) and isinstance(sides[0], float)):
        AAS = True
    ABC = ['A', 'B', 'C']
    abc = ['a', 'b', 'c']
    if SSS:
        unknown_angle = []
        known_angle = []
        for i in range(3):
            if angles[i] == '':
                unknown_angle.append(i)
            else:
                known_angle.append((i, round(angles[i]*180/math.pi, decimals)))
        angles[0] = math.acos(
            (sides[1]**2+sides[2]**2-sides[0]**2)/(2*sides[1]*sides[2]))
        angles[1] = math.acos(
            (sides[0]**2+sides[2]**2-sides[1]**2)/(2*sides[0]*sides[2]))
        angles[2] = math.acos(
            (sides[1]**2+sides[0]**2-sides[2]**2)/(2*sides[1]*sides[0]))
        for i in range(len(angles)):
            angles[i] = round(angles[i]*180/math.pi, decimals)
        for i in range(len(known_angle)):
            if angles[known_angle[i][0]] != known_angle[i][1]:
                message='Angle ' + ABC[known_angle[i][0]] + ' given does not match the sides given. It is not possible for a valid triangle to form.'
                result.update({"message": message})
                return result
        total = ''
        # what angles are not given
        steps = []
        steps.append("The cosine rule is used to solve this triangle.")
        steps.append("Since the three sides of the triangle are known, we can simple use the formula cos(A) = (b^2+c^2-a^2)/(2bc) to calculate the angles of the triangle.")
        for i in range(len(unknown_angle)):
            other_than_i = []
            for j in range(3):
                if j != i:
                    other_than_i.append(j)
            total = 'cos(' + ABC[unknown_angle[i]] + ') = ' + str(sides[other_than_i[0]]**2)+' + ' + str(sides[other_than_i[1]]**2) + \
                ' - ' + str(sides[i]**2) + ' / (2 * ' + str(sides[other_than_i[0]]
                                                            ) + ' * ' + str(sides[other_than_i[1]]) + ')'
            steps.append(total)
        steps.append("Finally, the result is being calculated.")
        # steps = 'The cosine rule is used to solve this triangle. <br/>Since the three sides of the triangle are known, we can simple use the formula cos(A) = (b^2+c^2-a^2)/(2bc) to calculate the angles of the triangle.<br>' + \
        #     total + 'Finally, the result is being calculated.'
    elif SAS:
        known_sides = []
        for i in range(len(sides)):
            if sides[i] == '':
                empty_side = i
            else:
                known_sides.append(i)
        entered_angle_values = []
        unknown_angles = []
        for i in range(3):
            if angles[i] != '' and i != empty_side:
                entered_angle_values.append((i, angles[i]))
            elif angles[i] == '':
                unknown_angles.append(i)
        unknown_side = math.sqrt(sides[known_sides[0]]**2 + sides[known_sides[1]]**2 -
                                 2*sides[known_sides[0]]*sides[known_sides[1]]*math.cos(angles[empty_side]))
        sides[empty_side] = unknown_side
        unknown_angle_a = math.asin(
            math.sin(angles[empty_side])/unknown_side*sides[known_sides[0]])
        unknown_angle_b = math.asin(
            math.sin(angles[empty_side])/unknown_side*sides[known_sides[1]])
        angles[known_sides[0]] = unknown_angle_a
        angles[known_sides[1]] = unknown_angle_b
        for i in range(len(angles)):
            angles[i] = round(angles[i]*180/math.pi, decimals)
        for i in range(len(sides)):
            sides[i] = round(sides[i], decimals)
        # check if there is already entered value that is wrong
        for i in entered_angle_values:
            if round(i[1]*180/math.pi, decimals) != angles[i[0]]:
                message='Angle ' + ABC[i[0]] + ' given does not match the sides given. It is not possible for a valid triangle to form.'
                result.update({"message": message})
                return result
        if len(entered_angle_values) > 1:
            plural = 's'
        else:
            plural = ''
        solve_angles = ''
        steps = []
        msg =  'The triangle is solved by first applying the cosine rule to side ' + abc[empty_side] + ', which can be expressed by the formula: ' + abc[empty_side] + \
            '^2 = ' + abc[known_sides[0]] + '^2 + ' + abc[known_sides[1]] + '^2 - 2 * ' + \
                abc[known_sides[0]] + ' * ' + abc[known_sides[1]] + \
            ' * cos(' + ABC[empty_side] + ')'
        msg2 = 'cos(' + str(sides[empty_side]) + ')^2 = ' + str(sides[known_sides[0]]) + \
            '^2 + ' + str(sides[known_sides[1]]) + '^2 - 2 * ' + str(sides[known_sides[0]]) + \
            ' * ' + str(sides[known_sides[1]]) + \
            ' * cos(' + str(angles[empty_side]) + ')'
        msg3 = "Now having obtained all the values of the sides, the values of the " + str(len(
                unknown_angles)) + ' unknown angle' + plural + ' can be calculated by applying the sine rule.'
        msg4 = 'Finally, we obtain the ' + str(len(unknown_angles)) + ' two unknown angle' + plural + '.'
        steps.append("msg")
        steps.append("Then, simply substitute the values of the sides.")
        steps.append("msg2")
        steps.append("So, the unknown side's length is " + str(sides[empty_side]))
        steps.append(msg3)

        for i in range(len(unknown_angles)):
            solve_angles = 'sin(' + \
                ABC[unknown_angles[i]] + ') / ' + abc[unknown_angles[i]] + \
                ' = sin(' + ABC[empty_side] + ') / ' + abc[empty_side] + '    ||    sin(' + str(angles[unknown_angles[i]]) + ') / ' + str(sides[unknown_angles[i]]) + ' = sin(' + str(
                    angles[empty_side]) + ') / ' + str(sides[empty_side]) 
            steps.append(solve_angles)
        steps.append(msg4)
        # steps = 'The triangle is solved by first applying the cosine rule to side ' + abc[empty_side] + ', which can be expressed by the formula: ' + abc[empty_side] + \
        #     '^2 = ' + abc[known_sides[0]] + '^2 + ' + abc[known_sides[1]] + '^2 - 2 * ' + \
        #         abc[known_sides[0]] + ' * ' + abc[known_sides[1]] + \
        #     ' * cos(' + ABC[empty_side] + ')<br>Then, simply substitute the values of the sides.<br>cos(' + str(sides[empty_side]) + ')^2 = ' + str(sides[known_sides[0]]) + \
        #     '^2 + ' + str(sides[known_sides[1]]) + '^2 - 2 * ' + str(sides[known_sides[0]]) + \
        #     ' * ' + str(sides[known_sides[1]]) + \
        #     ' * cos(' + str(angles[empty_side]) + ')<br>So, the unknown side\'s length is ' + str(sides[empty_side]) + '<br>Now having obtained all the values of the sides, the values of the ' + str(len(
        #         unknown_angles)) + ' unknown angle' + plural + ' can be calculated by applying the sine rule.<br>' + solve_angles + 'Finally, we obtain the ' + str(len(unknown_angles)) + ' two unknown angle' + plural + '.'
    elif SSA:
        angle_init = angles.copy()
        side_init = sides.copy()
        known_sides = []
        for i in range(len(sides)):
            if sides[i] == '':
                empty_side = i
            else:
                known_sides.append(i)
        ang = [0, 1, 2]
        for i in range(len(angles)):
            if isinstance(angles[i], float):
                known_angle = i
                ang.remove(known_angle)
                break
        empty_angles = ang
        known_sides.remove(known_angle)
        different_side = known_sides[0]
        if math.sin(angles[known_angle])/sides[known_angle]*sides[known_sides[0]] > 1 or math.sin(angles[known_angle])/sides[known_angle]*sides[known_sides[0]] < 0:
            result.update({"message":'The three values entered cannot form a valid triangle.' })
            return result
        changeable_angle = math.asin(
            math.sin(angles[known_angle])/sides[known_angle]*sides[known_sides[0]])
        passive_angle = math.pi - changeable_angle - angles[known_angle]
        unknown_side = sides[known_angle] / \
            math.sin(angles[known_angle])*math.sin(passive_angle)
        sides[empty_side] = unknown_side
        angles[known_sides[0]] = changeable_angle
        empty_angles.remove(known_sides[0])
        angles[empty_angles[0]] = passive_angle
        # check wrong angles and sides
        empty_angles = []
        for i in range(len(angle_init)):
            if angle_init[i] == '':
                empty_angles.append(i)
            else:
                known_angle = i
        known_sides = []
        for i in range(3):
            if side_init[i] == '':
                empty_side = i
            else:
                known_sides.append(i)
        if round(angle_init[known_angle], 3) != round(angles[known_angle], 3):
            message='Angle ' + ABC[known_angle] + ' given does not match the sides given. It is not possible for a valid triangle to form.'
            result.update({"message": message})
            return result
        if side_init[known_sides[0]] != sides[known_sides[0]]:
            message='Angle ' + abc[known_sides[0]] + ' given does not match the sides given. It is not possible for a valid triangle to form.'
            result.update({"message": message})
            return result
        if side_init[known_sides[1]] != sides[known_sides[1]]:
            message='Angle ' + abc[known_sides[0]] + ' given does not match the sides given. It is not possible for a valid triangle to form.'
            result.update({"message": message})
            return result
        steps = []
        msg = 'The triangle is given two sides, ' + abc[known_sides[0]] + ' and ' + abc[known_sides[1]] + ', and an angle,' + ABC[known_angle] + ', forming the S-S-A model. It is possible for the triangle to have two possible structures in this model.'
        steps.append(msg)
        if angle_init[different_side] == '':
            steps.append("First, the sine rule can be used to find out the measure of angle "+ ABC[different_side]+".")
            msg2='sin(' + ABC[known_angle] + ')/' + abc[known_angle] + ' = sin(' + ABC[different_side] + ')/' + abc[different_side] + '    ||    ' + 'sin(' + str(round(angles[known_angle]*180/math.pi, decimals)) + ')/' + str(round(sides[known_angle], decimals)) + ' = sin(' + str(
                round(angles[different_side]*180/math.pi, decimals)) + ')/' + str(round(sides[different_side], decimals))
            steps.append(msg2)
            msg3 = 'Now, we can simply calculate the measure of angle ' + ABC[empty_side] + '. The measurement of ' + ABC[empty_side] + ' is ' + str(round(angles[empty_side]*180/math.pi, decimals)) + '. Then, we can use the cosine rule to solve the unknown side ' + abc[empty_side] + '.'
            steps.append(msg3)
            # different = '<br>First, the sine rule can be used to find out the measure of angle ' + ABC[different_side] + '.<br>sin(' + ABC[known_angle] + ')/' + abc[known_angle] + ' = sin(' + ABC[different_side] + ')/' + abc[different_side] + '    ||    ' + 'sin(' + str(round(angles[known_angle]*180/math.pi, decimals)) + ')/' + str(round(sides[known_angle], decimals)) + ' = sin(' + str(
            #     round(angles[different_side]*180/math.pi, decimals)) + ')/' + str(round(sides[different_side], decimals)) + '<br>Now, we can simply calculate the measure of angle ' + ABC[empty_side] + '. The measurement of ' + ABC[empty_side] + ' is ' + str(round(angles[empty_side]*180/math.pi, decimals)) + '. Then, we can use the cosine rule to solve the unknown side ' + abc[empty_side] + '.'
        else:
            msg = 'As angle ' + ABC[different_side] + 'is already known, the measure of angle' + ABC[empty_side] + ' can be calculated by simply subtracting the measurement of the two other angles from 180, for the sum of interior angles of a triangle is 180 degrees.'
            steps.append(msg)
            msg2 = 'The measure of angle ' + \
                ABC[empty_side] + ' is ' + str(round(angles[empty_side]*180/math.pi, decimals)) + \
                '. Then, we can use the cosine rule to solve the unknown side ' + \
                abc[empty_side] + '.'
            steps.append(msg2)
            # different = '<br>As angle ' + ABC[different_side] + 'is already known, the measure of angle' + ABC[empty_side] + ' can be calculated by simply subtracting the measurement of the two other angles from 180, for the sum of interior angles of a triangle is 180 degrees.<br>The measure of angle ' + \
            #     ABC[empty_side] + ' is ' + str(round(angles[empty_side]*180/math.pi, decimals)) + \
            #     '. Then, we can use the cosine rule to solve the unknown side ' + \
            #     abc[empty_side] + '.'
        msg = abc[empty_side] + '^2 = ' + abc[known_sides[0]] + '^2 + ' + abc[known_sides[1]] + '^2 - 2*' + abc[known_sides[0]] + '*' + abc[known_sides[1]] + '*cos(' + ABC[empty_side] + ')    ||    ' + abc[empty_side] + '^2 = ' + str(
            round(sides[known_sides[0]], decimals)) + '^2 + ' + str(round(sides[known_sides[1]], decimals)) + '^2 - 2*' + str(round(sides[known_sides[0]], decimals)) + '*' + str(round(sides[known_sides[1]], decimals)) + '*cos(' + str(round(angles[empty_side]*180/math.pi, decimals)) + ')'
        steps.append(msg)
        msg='Therefore, the value of ' + abc[empty_side] + ' can be calculated: ' + str(round(sides[empty_side], decimals)) + '.'
        steps.append(msg)
        # steps = 'The triangle is given two sides, ' + abc[known_sides[0]] + ' and ' + abc[known_sides[1]] + ', and an angle,' + ABC[known_angle] + ', forming the S-S-A model. It is possible for the triangle to have two possible structures in this model.' + different + '<br>' + abc[empty_side] + '^2 = ' + abc[known_sides[0]] + '^2 + ' + abc[known_sides[1]] + '^2 - 2*' + abc[known_sides[0]] + '*' + abc[known_sides[1]] + '*cos(' + ABC[empty_side] + ')    ||    ' + abc[empty_side] + '^2 = ' + str(
        #     round(sides[known_sides[0]], decimals)) + '^2 + ' + str(round(sides[known_sides[1]], decimals)) + '^2 - 2*' + str(round(sides[known_sides[0]], decimals)) + '*' + str(round(sides[known_sides[1]], decimals)) + '*cos(' + str(round(angles[empty_side]*180/math.pi, decimals)) + ')<br>Therefore, the value of ' + abc[empty_side] + ' can be calculated: ' + str(round(sides[empty_side], decimals)) + '.'

        # check the side opposite to the angle to see if there can be a second triangle
        unchangeable = known_sides[0]
        # the empty angle that is free to move, not between two fixed sides.
        change_angle_idx = angles.index(changeable_angle)
        pos_changeable_angle = math.pi - changeable_angle
        pos_passive_angle = math.pi - \
            angles[known_angle] - pos_changeable_angle
        if pos_changeable_angle > 0 and pos_passive_angle > 0 and round(pos_changeable_angle + pos_passive_angle + angles[known_angle], 3) == round(math.pi, 3):
            Two = True
            angles1 = angles.copy()
            sides1 = sides.copy()
            changed_side = sides[known_angle] / \
                math.sin(angles[known_angle])*math.sin(pos_passive_angle)
            sides1[empty_side] = changed_side
            angles1[change_angle_idx] = pos_changeable_angle
            angles1[empty_side] = pos_passive_angle
            steps1 = []
            msg = 'Already knowing 1 possiblity of angles and sides, it is possible for angle ' + ABC[change_angle_idx] + ' to also have the value of (180-' + str(round(angles[change_angle_idx]*180/math.pi, decimals)) + '), which is ' + str(round(angles1[change_angle_idx]*180/math.pi, decimals)) + '.'
            steps1.append(msg)
            msg = 'Therefore, angle ' + ABC[empty_side] + ' can also be calculated by using the sum of triangle\'s interior angles, 180 degrees, to subtract the measure of two other angles. Therefore, angle ' + ABC[empty_side] + ' is known to be ' + str(round(
                angles1[empty_side]*180/math.pi, decimals)) + ' degrees.'
            steps1.append(msg)
            msg = 'Now, substituting the sine rule, the length of the unknown side can be obtained.'
            steps1.append(msg)
            msg = 'sin(' + ABC[empty_side] + ')/' + abc[empty_side] + ' = sin(' + ABC[change_angle_idx] + ')/' + abc[change_angle_idx] + '    ||    sin(' + str(round(angles1[empty_side]*180/math.pi, decimals)) + ')/' + str(round(sides1[empty_side], decimals)) + ' = sin(' + str(round(angles1[change_angle_idx]*180/math.pi, decimals)) + ')/' + str(round(sides1[change_angle_idx], decimals))
            steps1.append(msg)
            msg = 'So the value of side ' + abc[empty_side] + ' is ' + str(round(sides1[empty_side], decimals)) + '.'
            steps1.append(msg)

            # steps1 = 'Already knowing 1 possiblity of angles and sides, it is possible for angle ' + ABC[change_angle_idx] + ' to have the value of (180-' + str(round(angles[change_angle_idx]*180/math.pi, decimals)) + '). The second possible value is calculated as ' + str(round(angles1[change_angle_idx]*180/math.pi, decimals)) + '.<br>Therefore, angle ' + ABC[empty_side] + ' can also be calculated by using the sum of triangle\'s interior angles, 180 degrees, to subtract the measure of two other angles. Therefore, angle ' + ABC[empty_side] + ' is known to be ' + str(round(
            #     angles1[empty_side]*180/math.pi, decimals)) + ' degrees.<br> Now, substituting the sine rule, the length of the unknown side can be obtained.<br>sin(' + ABC[empty_side] + ')/' + abc[empty_side] + ' = sin(' + ABC[change_angle_idx] + ')/' + abc[change_angle_idx] + '    ||    sin(' + str(round(angles1[empty_side]*180/math.pi, decimals)) + ')/' + str(round(sides1[empty_side], decimals)) + ' = sin(' + str(round(angles1[change_angle_idx]*180/math.pi, decimals)) + ')/' + str(round(sides1[change_angle_idx], decimals)) + '<br>So the value of side ' + abc[empty_side] + ' is ' + str(round(sides1[empty_side], decimals)) + '.'
        # end
        for i in range(len(angles)):
            angles[i] = round(angles[i]*180/math.pi, decimals)
            sides[i] = round(sides[i], decimals)
            if Two:
                angles1[i] = round(angles1[i]*180/math.pi, decimals)
                sides1[i] = round(sides1[i], decimals)
    elif ASA:
        angle_init = angles.copy()
        sie_init = sides.copy()
        empty_sides = []
        for i in range(len(sides)):
            if isinstance(sides[i], float):
                known_side = i
            else:
                empty_sides.append(i)
        known_angles = []
        # only if the angle is opposite to the already known side, it can be considered to be an empty angle
        for i in range(len(angles)):
            if i == known_side:
                empty_angle = i
            elif isinstance(angles[i], float):
                known_angles.append(i)
        unknown_angle = math.pi - \
            angles[known_angles[0]] - angles[known_angles[1]]
        angles[empty_angle] = unknown_angle
        side_a = sides[known_side] / \
            math.sin(angles[known_side])*math.sin(angles[empty_sides[0]])
        side_b = sides[known_side] / \
            math.sin(angles[known_side])*math.sin(angles[empty_sides[1]])
        sides[empty_sides[0]] = side_a
        sides[empty_sides[1]] = side_b
        for i in range(len(angles)):
            angles[i] = round(angles[i]*180/math.pi, decimals)
            sides[i] = round(sides[i], decimals)
        empty = True
        if angle_init[empty_angle] != '':
            empty = False
        steps = []
        if empty:
            calculate_angle = 'First, we calculate the measure of the unknown angle. '
            steps.append(calculate_angle)
            calculate_angle = '180 - ' + ABC[known_angles[0]] + ' - ' + ABC[known_angles[1]] + ' = 180 - ' + str(
                angles[known_angles[0]]) + ' - ' + str(angles[known_angles[1]]) + ' = ' + str(angles[empty_angle]) + '.'
            steps.append(calculate_angle)
            calculate_angle = 'Then, the '
        elif not empty:
            if round(angle_init[empty_angle]*180/math.pi, decimals) != angles[empty_angle]:
                result.update({"message": 'The given angles are not able to form a triangle.'})
                return result
            calculate_angle = 'Since all three angles are already known, the '
        steps.append(calculate_angle+'length of the other two sides can be calculated by the sine rule.')
        msg = abc[empty_sides[0]] + ' / sin(' + ABC[empty_sides[0]] + ') = ' + abc[known_side] + ' / sin(' + ABC[known_side] + ')    ||    ' + str(sides[empty_sides[0]]) + ' / sin(' + str(angles[empty_sides[0]]) + ') = ' + str(
            sides[known_side]) + ' / sin(' + str(angles[known_side]) +')'
        steps.append(msg)
        msg = abc[empty_sides[1]] + ' / sin(' + ABC[empty_sides[1]] + ') = ' + abc[known_side] + '/ sin(' + ABC[known_side] + ')    ||    ' + str(sides[empty_sides[1]]) + ' / sin(' + str(angles[empty_sides[1]]) + ') = ' + str(sides[known_side]) + ' / sin(' + str(angles[known_side]) + ')'
        steps.append(msg)
        # steps = calculate_angle + 'length of the other two sides can be calculated by the sine rule.<br>' + abc[empty_sides[0]] + ' / sin(' + ABC[empty_sides[0]] + ') = ' + abc[known_side] + ' / sin(' + ABC[known_side] + ')    ||    ' + str(sides[empty_sides[0]]) + ' / sin(' + str(angles[empty_sides[0]]) + ') = ' + str(
        #     sides[known_side]) + ' / sin(' + str(angles[known_side]) + ')<br>' + abc[empty_sides[1]] + ' / sin(' + ABC[empty_sides[1]] + ') = ' + abc[known_side] + '/ sin(' + ABC[known_side] + ')    ||    ' + str(sides[empty_sides[1]]) + ' / sin(' + str(angles[empty_sides[1]]) + ') = ' + str(sides[known_side]) + ' / sin(' + str(angles[known_side]) + ')'
    elif AAS:
        known_angles = []
        for i in range(len(angles)):
            if angles[i] == '':
                empty_angle = i
            else:
                known_angles.append(i)
        angles[empty_angle] = math.pi - angles[known_angles[0]] - angles[known_angles[1]]
        unknown_sides = []
        for i in range(len(sides)):
            if sides[i] == '':
                unknown_sides.append(i)
            else:
                known_side = i
        empty_side_a = sides[known_side] / \
            math.sin(angles[known_side]) * math.sin(angles[unknown_sides[0]])
        empty_side_b = sides[known_side] / \
            math.sin(angles[known_side]) * math.sin(angles[unknown_sides[1]])
        sides[unknown_sides[0]] = empty_side_a
        sides[unknown_sides[1]] = empty_side_b
        for i in range(len(angles)):
            angles[i] = round(angles[i]*180/math.pi, decimals)
            sides[i] = round(sides[i], decimals)
        steps = []
        msg = 'Already knowing two of the angles in the triangle, the unknown angle ' + ABC[empty_angle] + ' can be calculated by 180 - ' + ABC[known_angles[0]] + ' - ' + ABC[known_angles[1]] + ' = ' + str(angles[empty_angle])
        steps.append(msg)
        steps.append('Then, the two sides that are not known is calculated by using the sine rule.')
        msg = abc[unknown_sides[0]] + ' / sin(' + ABC[unknown_sides[0]] + ') = ' + abc[known_side] + ' / sin(' + ABC[known_side] + ')    ||    ' + str(sides[unknown_sides[0]]) + ' / sin(' + str(angles[unknown_sides[0]]) + ') = ' + str(sides[known_side]) + ' / sin(' + str(angles[known_side]) + ')'
        steps.append(msg)
        msg = abc[unknown_sides[1]] + ' / sin(' + ABC[unknown_sides[1]] + ') = ' + abc[known_side] + ' / sin(' + ABC[known_side] + ')    ||    ' + str(sides[unknown_sides[1]]) + ' / sin(' + str(angles[unknown_sides[1]]) + ') = ' + str(sides[known_side]) + ' / sin(' + str(angles[known_side]) + ')'
        steps.append(msg)

        # steps = 'Already knowing two of the angles in the triangle, the unknown angle ' + ABC[empty_angle] + ' can be calculated by 180 - ' + ABC[known_angles[0]] + ' - ' + ABC[known_angles[1]] + ' = ' + str(angles[empty_angle]) + '<br>Then, the two sides that are not known is calculated by using the sine rule.<br>' + abc[unknown_sides[0]] + ' / sin(' + ABC[unknown_sides[0]] + ') = ' + abc[known_side] + ' / sin(' + ABC[known_side] + ')    ||    ' + str(sides[unknown_sides[0]]) + ' / sin(' + str(angles[unknown_sides[0]]) + ') = ' + str(sides[known_side]) + ' / sin(' + str(angles[known_side]) + ')<br>' + abc[unknown_sides[1]] + ' / sin(' + ABC[unknown_sides[1]] + ') = ' + abc[known_side] + ' / sin(' + ABC[known_side] + ')    ||    ' + str(sides[unknown_sides[1]]) + ' / sin(' + str(angles[unknown_sides[1]]) + ') = ' + str(sides[known_side]) + ' / sin(' + str(angles[known_side]) + ')' 
    
    result.update({
        "sides": sides,
        "angles": angles,
    })
    
    if Two:
        s = (sides[0] + sides[1] + sides[2]) / 2
        area = round(
            math.sqrt(s*(s-sides[0])*(s-sides[1])*(s-sides[2])), decimals)
        height_a = round(area*2/sides[0], decimals)
        height_b = round(area*2/sides[1], decimals)
        height_c = round(area*2/sides[2], decimals)
        A = [1,1]
        B = [1+sides[2],1]
        y = 1+height_c
        x = 1+math.sqrt(sides[1]**2-(y-1)**2)
        C = [x,y]
        pts = np.array([A, B, C])
        p = Polygon(pts, closed=True, ec="red", fc="white")
        ax = plt.gca()
        ax.set_aspect('equal', adjustable='box')
        ax.add_patch(p)
        if B[0] > C[0]:
            ax.set_xlim(0, B[0]+1)
        else:
            ax.set_xlim(0, C[0]+1)
        ax.set_ylim(0, C[1]+1)
        ax.annotate('A', A, color = 'g')
        ax.annotate('B', B, color = 'g')
        ax.annotate('C', C, color = 'g')
        c = ((A[0]+B[0])/2, (A[1]+B[1])/2)
        a = ((C[0]+B[0])/2, (C[1]+B[1])/2)
        b = ((A[0]+C[0])/2, (A[1]+C[1])/2)
        ax.annotate('a', a, color = 'b')
        ax.annotate('b', b, color = 'b')
        ax.annotate('c', c, color = 'b')
        plt.savefig('./static/foo.png', bbox_inches='tight')
        plt.clf()

        s1 = (sides1[0] + sides1[1] + sides1[2]) / 2
        area1 = round(
            math.sqrt(s1*(s1-sides1[0])*(s1-sides1[1])*(s1-sides1[2])), decimals)
        height_a1 = round(area1*2/sides1[0], decimals)
        height_b1 = round(area1*2/sides1[1], decimals)
        height_c1 = round(area1*2/sides1[2], decimals)
        A = [1,1]
        B = [1+sides1[2],1]
        y = 1+height_c1
        x = 1+math.sqrt(sides1[1]**2-(y-1)**2)
        C = [x,y]
        pts = np.array([A, B, C])
        p = Polygon(pts, closed=True, ec="red", fc="white")
        ax = plt.gca()
        ax.set_aspect('equal', adjustable='box')
        ax.add_patch(p)
        if B[0] > C[0]:
            ax.set_xlim(0, B[0]+1)
        else:
            ax.set_xlim(0, C[0]+1)
        ax.set_ylim(0, C[1]+1)
        ax.annotate('A', A, color = 'g')
        ax.annotate('B', B, color = 'g')
        ax.annotate('C', C, color = 'g')
        c = ((A[0]+B[0])/2, (A[1]+B[1])/2)
        a = ((C[0]+B[0])/2, (C[1]+B[1])/2)
        b = ((A[0]+C[0])/2, (A[1]+C[1])/2)
        ax.annotate('a', a, color = 'b')
        ax.annotate('b', b, color = 'b')
        ax.annotate('c', c, color = 'b')
        plt.savefig('./static/foo1.png', bbox_inches='tight')
        plt.clf()
        result.update({
            "sides": sides,
            "angles": angles,
            "height_a": height_a,
            "height_b": height_b,
            "height_c": height_c,
            "area": area,
            "steps": steps,
            "sides1": sides1,
            "angles1": angles[1],
            "height_a1": height_a1, 
            "height_b1": height_b1,
            "height_c1": height_c1,
            "area1": area1,
            "steps1": steps1

        })
        return result
    else:
        s = (sides[0] + sides[1] + sides[2]) / 2
        area = round(
            math.sqrt(s*(s-sides[0])*(s-sides[1])*(s-sides[2])), decimals)
        height_a = round(area*2/sides[0], decimals)
        height_b = round(area*2/sides[1], decimals)
        height_c = round(area*2/sides[2], decimals)
        A = [1,1]
        B = [1+sides[2],1]
        y = 1+height_c
        x = 1+math.sqrt(sides[1]**2-(y-1)**2)
        C = [x,y]
        pts = np.array([A, B, C])
        p = Polygon(pts, closed=True, ec="red", fc="white")
        ax = plt.gca()
        ax.set_aspect('equal', adjustable='box')
        ax.add_patch(p)
        if B[0] > C[0]:
            ax.set_xlim(0, B[0]+1)
        else:
            ax.set_xlim(0, C[0]+1)
        ax.set_ylim(0, C[1]+1)
        ax.annotate('A', A, color = 'g')
        ax.annotate('B', B, color = 'g')
        ax.annotate('C', C, color = 'g')
        c = ((A[0]+B[0])/2, (A[1]+B[1])/2)
        a = ((C[0]+B[0])/2, (C[1]+B[1])/2)
        b = ((A[0]+C[0])/2, (A[1]+C[1])/2)
        ax.annotate('a', a, color = 'b')
        ax.annotate('b', b, color = 'b')
        ax.annotate('c', c, color = 'b')
        plt.savefig('./static/foo.png', bbox_inches='tight')
        plt.clf()
        result.update({
            "sides": sides,
            "angles": angles,
            "height_a": height_a,
            "height_b": height_b,
            "height_c": height_c,
            "area": area,
            "steps": steps
        })
        return (result)