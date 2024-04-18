import random
import re
import numpy

def roll_calc(roll_data):
    roll_result = 0                                                     #sets default value of variable
    separated_values = roll_data.split('d')                         #splits message into [# of rolls, # of faces + proficiency bonus]
    separated_values_last = separated_values.pop()                      #pops the number of die faces + proficiency bonus
    separated_values_last = separated_values_last.replace('-','+-')     #allows for negative proficiency bonus
    separated_values_last = separated_values_last.split('+')            # splits number of faces and proficiency bonus
    separated_values.extend(separated_values_last)                      #combines everything back into one list

    if len(separated_values) == 3:                                                              # true in instances like 3d10 + 6 and d10 + 6. 
        if separated_values[0] == '':                                                           # true in instances like d10 + 6
            roll_result = random.randint(1,int(separated_values[1])) + int(separated_values[2])
        else:                                                                                   # true in instances like 3d10
            for i in range(1,int(separated_values[0]) + 1):
                roll_result += random.randint(1,int(separated_values[1]))
            roll_result += int(separated_values[2])
    else:                                                                                       # true in instances like 3d10 and d10
        if separated_values[0] == '':                                                           # true in instances like d10
            roll_result = random.randint(1,int(separated_values[1]))
        else:                                                                                   # true in instances like 3d10
            for i in range(1,int(separated_values[0]) + 1):
                roll_result += random.randint(1,int(separated_values[1]))
    return str(roll_result)                 #returns die roll with added proficiency

def resource_sort(unsortedfile):
    url_reg_expression =r"(?i)\b((?:[a-z][\w-]+:(?:/{1,3}|[a-z0-9%])|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    with open(unsortedfile,'r') as resource_list:
        sorted_resource_list_unclean = []
        for line in resource_list:
            sorted_resource_list_unclean += re.split(url_reg_expression,line)
        resource_list.close()

    sorted_resource_list_cleaned = list(filter(lambda item: item is not None, sorted_resource_list_unclean))

    with open(unsortedfile,'w') as test_text:
        for i in range(1,len(sorted_resource_list_cleaned)):
            test_text.write(f'{sorted_resource_list_cleaned[i]}')
def create_tier_list(server_id):
    with (f'data/at_everyone_{server_id}.txt','a') as tier_list:
        message = ""
        for line in tier_list:
            message += line
        tier_list.close()
    return message

def tier_list(server_id):
    message = []
    with (f'data/at_everyone_{server_id}.txt','r') as tier_list:
        for line in tier_list:
            message.append(line)
    tier_list.close()
    return message
    

def wordle(wordle):
    wordle = wordle.split(',')
    print(wordle)
    for i in range(1,len(wordle)):
        wordle[i] = wordle[i].strip()
    print(wordle)
    if len(wordle) > 1:
        user_tries = wordle[1:]
    user_guess = wordle[0]





    user_guess = list(user_guess)
    possible_solution_template = ['_', '_', '_', '_', '_']
    yellow_letters = []

    def permutationtostring(permutation):
        out =""
        for row in permutation:
            for c in row:
                out += str(c)
            out+= "\n"
        return out


    def spots_remaining(matrix):
        spots_remaining = 0
        for column in matrix[0, :]:
            if column == '_':
                spots_remaining += 1
        return (spots_remaining)


    def trim(matrix):
        b = 0
        empty_array = numpy.array(['', '', '', '', ''])
        for row in matrix:
            if all(row == empty_array):
                matrix = numpy.delete(matrix, b, axis=0)
            else:
                b += 1
        return matrix


    def eliminate_permutations(user_tries, matrix):

        for previous_guesses in user_tries:     
            incorrect_positions = ['','','','','']
            previous_guess_as_list = []
            invalid_rows = []
            print('currently testing guess: ' + previous_guesses)
            for char in previous_guesses:
                previous_guess_as_list.append(char)
            print(previous_guess_as_list)

            
            
            i = 0
            j = 0

            while j <= (len(previous_guess_as_list) - 1):
                #print('entered')   
                if previous_guess_as_list[j].isalpha():
                    #print('Alpha character spotted. Checking to see if letter is followed by a #.')
                    if j < (len(previous_guess_as_list) - 1):
                        if previous_guess_as_list[j+1] == '#':
                            #print('Letter was followed up by a #. Letter is in the correct spot, and will be replaced with an underscore')
                            incorrect_positions[i] = ('')
                            i+= 1
                            j+= 2
                        else:
                            incorrect_positions[i] = previous_guess_as_list[j]
                            #print('Yellow letter in incorrect place spotted.')                        
                            i+= 1
                            j+= 1
                    else:
                        incorrect_positions[i] = previous_guess_as_list[j]
                        #print('Yellow letter in incorrect place spotted.')
                        i+= 1
                        j+= 1
                else:
                        incorrect_positions[i] = ('')
                        #print('underscore spotted. incrementing j and moving on.')
                        i+= 1
                        j+= 1
            #print('the yellow letters are confirmed to not be in positions: ')
            print(incorrect_positions)
            
            b = 0
            invalid_permuation_found = False
            for row in matrix:
                k = 0
                print(row)
                for k in range(5):
                    if row[k] == incorrect_positions[k]:
                        print('match found: ' + row[k] + ' = ' + incorrect_positions[k])
                        invalid_permuation_found = True
                        print('this one is an invalid permutation:')
                        print(row)
                    #else:
                    #    print('match not found: ' + row[k] + ' != ' + incorrect_positions[k])
                        
                if invalid_permuation_found == True:
                    invalid_rows.append(b)
                    print('value appended, b =' + str(b))
                    invalid_permuation_found = False
                    b+= 1
                else:
                    b += 1
                    print('value not appended, b =' + str(b))
            
            print('invalid rows at pos ' + str(invalid_rows))                
            matrix = numpy.delete(matrix, invalid_rows, axis=0)
            print(matrix)
        return matrix

    i = 0
    j = 0
    while i < len(user_guess):
        if user_guess[i] == '_':
            i += 1
            j += 1
        else:

            if user_guess[i].isalpha and i <= (len(user_guess) - 1):
                if i != (len(user_guess) - 1):
                    if user_guess[i + 1] == '#':
                        possible_solution_template[j] = user_guess[i]
                        i += 1
            yellow_letters.append(user_guess[i])
            i += 1
            j += 1

    while '#' in yellow_letters:
        yellow_letters.remove('#')

    if len(yellow_letters) >= 1:
        first_permutation = numpy.chararray((5, 5), unicode=True)
        if len(yellow_letters) >= 2:
            second_permutation = numpy.chararray((20, 5), unicode=True)
            if len(yellow_letters) >= 3:
                third_permutation = numpy.chararray((60, 5), unicode=True)
                if len(yellow_letters) >= 4:
                    fourth_permutation = numpy.chararray((120, 5), unicode=True)
                    if len(yellow_letters) == 5:
                        fifth_permutation = numpy.chararray((120, 5), unicode=True)

    if len(yellow_letters) > 0:
        k = 0
        l = 0
        for i in range(0, 5):
            for j in range(0, 5):
                first_permutation[j, i] = possible_solution_template[i % 5]

        empty_spots = spots_remaining(first_permutation)

    else:
        empty_spots = 0

    if len(yellow_letters) > 0:
        for row in range(0, empty_spots):
            for column in range(0, 5):
                if first_permutation[row, column] == '_':
                    if k == l:
                        first_permutation[row, column] = yellow_letters[0]
                        l += 1
                        row += 1
                        k = 0
                        break
                    else:
                        k += 1
            k = 0
        b = 0
        for row in first_permutation:
            if all(row == possible_solution_template):
                first_permutation = numpy.delete(first_permutation, b, axis=0)
            else:
                b += 1

    empty_spots += -1
    permutation_list_adder = 0

    if len(yellow_letters) > 1:

        for i in range(0, first_permutation.shape[0]):

            matrix_permutation_subset = numpy.chararray((empty_spots, 5), unicode=True)
            for row in range(0, empty_spots):
                matrix_permutation_subset[row, :] = first_permutation[i, :]

            k = 0
            l = 0
            for row in range(0, matrix_permutation_subset.shape[0]):
                for column in range(0, 5):
                    if matrix_permutation_subset[row, column] == '_':
                        if k == l:
                            matrix_permutation_subset[row, column] = yellow_letters[1]
                            l += 1
                            row += 1
                            k = 0
                            break
                        else:
                            k += 1
                k = 0

            for j in range(0, matrix_permutation_subset.shape[0]):
                second_permutation[permutation_list_adder, :] = matrix_permutation_subset[j, :]
                permutation_list_adder += 1

    empty_spots += -1
    permutation_list_adder = 0
    if len(yellow_letters) > 2:

        for i in range(0, second_permutation.shape[0]):

            matrix_permutation_subset = numpy.chararray((empty_spots, 5), unicode=True)
            for row in range(0, empty_spots):
                matrix_permutation_subset[row, :] = second_permutation[i, :]

            k = 0
            l = 0
            for row in range(0, matrix_permutation_subset.shape[0]):
                for column in range(0, 5):
                    if matrix_permutation_subset[row, column] == '_':
                        if k == l:
                            matrix_permutation_subset[row, column] = yellow_letters[2]
                            l += 1
                            row += 1
                            k = 0
                            break
                        else:
                            k += 1
                k = 0

            for j in range(0, matrix_permutation_subset.shape[0]):
                third_permutation[permutation_list_adder, :] = matrix_permutation_subset[j, :]
                permutation_list_adder += 1

    empty_spots += -1
    permutation_list_adder = 0
    if len(yellow_letters) > 3:

        for i in range(0, third_permutation.shape[0]):

            matrix_permutation_subset = numpy.chararray((empty_spots, 5), unicode=True)
            for row in range(0, empty_spots):
                matrix_permutation_subset[row, :] = third_permutation[i, :]
            k = 0
            l = 0
            for row in range(0, matrix_permutation_subset.shape[0]):
                for column in range(0, 5):
                    if matrix_permutation_subset[row, column] == '_':
                        if k == l:

                            matrix_permutation_subset[row, column] = yellow_letters[3]
                            l += 1
                            row += 1
                            k = 0
                            break
                        else:

                            k += 1
                k = 0

            for j in range(0, matrix_permutation_subset.shape[0]):
                fourth_permutation[permutation_list_adder, :] = matrix_permutation_subset[j, :]
                permutation_list_adder += 1

    empty_spots += -1
    permutation_list_adder = 0
    if len(yellow_letters) > 4:

        for i in range(0, fourth_permutation.shape[0]):

            matrix_permutation_subset = numpy.chararray((empty_spots, 5), unicode=True)
            for row in range(0, empty_spots):
                matrix_permutation_subset[row, :] = fourth_permutation[i, :]

            l = 0
            for row in range(0, matrix_permutation_subset.shape[0]):
                for column in range(0, 5):
                    if matrix_permutation_subset[row, column] == '_':
                        if k == l:

                            matrix_permutation_subset[row, column] = yellow_letters[4]
                            l += 1
                            row += 1
                            k = 0
                            break
                        else:

                            k += 1
                k = 0

            for j in range(0, matrix_permutation_subset.shape[0]):
                fifth_permutation[permutation_list_adder, :] = matrix_permutation_subset[j, :]
                permutation_list_adder += 1

    if len(yellow_letters) == 0:
        possible_solution_template = permutationtostring(possible_solution_template)
        possible_solution_template = "```\n" + possible_solution_template + "```"        
        return possible_solution_template
    elif len(yellow_letters) == 1:
        first_permutation = trim(first_permutation)
        if len(wordle) > 1:
            first_permutation = eliminate_permutations(user_tries, first_permutation)
        first_permutation = permutationtostring(first_permutation)
        first_permutation = "```\n" + first_permutation + "```"
        return first_permutation
    elif len(yellow_letters) == 2:
        second_permutation = trim(second_permutation)
        if len(wordle) > 1:
            second_permutation = eliminate_permutations(user_tries, second_permutation)
        second_permutation = permutationtostring(second_permutation)
        second_permutation = "```\n" + second_permutation + "```"
        return second_permutation
    elif len(yellow_letters) == 3:
        third_permutation = trim(third_permutation)
        if len(wordle) > 1:
            third_permutation = eliminate_permutations(user_tries, third_permutation)
        third_permutation = permutationtostring(third_permutation)
        third_permutation = "```\n" + third_permutation + "```"
        print(third_permutation)
        return third_permutation
    elif len(yellow_letters) == 4:
        fourth_permutation = trim(fourth_permutation)
        if len(wordle) > 1:
            eliminate_permutations(user_tries, fourth_permutation)
        fourth_permutation = permutationtostring(fourth_permutation)
        fourth_permutation = "```\n" + fourth_permutation + "```"
        return fourth_permutation
    else:
        fifth_permutation = trim(fifth_permutation)
        if len(wordle) > 1:
            fifth_permutation = eliminate_permutations(user_tries, fifth_permutation)
        fifth_permutation = permutationtostring(fifth_permutation)
        fifth_permutation = "```\n" + fifth_permutation + "```"
        print(wordle    )
        return fifth_permutation

