import operations
def run(again="y", grade_list=[]):
    print("Welcome to the Grade Shredder 9000x. By Christian Boin.")
    print("Hit enter when inputting grades to cakculate final requirements.")
    print("Input in the following format: 80 0.10")
    while again == "y":
        grade_list.clear()
        grade_list = collect_grades()
        if 1 - operations.total_weights(grade_list) < 0.001: # check if full weight has been reached
            print("Your final grade is: %s" % (calc_current_grade(grade_list)))
        else:
            print("Grade so far: %s" % (calc_current_grade(grade_list)))
            evaluation_weight = collect_eval_weight(grade_list)
            grade_list = calc_remainder_missing(grade_list, evaluation_weight)
            max_grade = compute_maximum(grade_list, evaluation_weight)
            final_set = calc_mark(grade_list, max_grade, evaluation_weight)
            print("To achieve %s you must obtain %s on your evaluation." % (final_set[0], final_set[1]))
        again = input("Type 'y' to calculate another, anything else to quit: ")
    print("Have a nice day!")

def collect_grades(raw_in = " ",grade_list = [], counter = 0, weight_remaining=1):
    while raw_in != "" or counter == 0:
        weight_remaining = round(1 - operations.total_weights(grade_list),2)
        if weight_remaining == 0:
            return grade_list
        if counter == 0:
            raw_in = input("Grade {0} weight {0}..  Weight of {1} remaining: ".format(counter, weight_remaining))
        else:
            raw_in = input("Grade {0} weight {0}.. Avg - {2}, Weight of {1} remaining: ".format(counter, weight_remaining, calc_current_grade(grade_list)))

        if raw_in != "":
            try:
                grade_set = operations.cast_to_types(raw_in.split(' '))
                weightsOverflow = operations.check_weights(grade_list, grade_set[1]) # check to make sure weight doesn't exceed total

                if grade_set[0] < 0:
                    print("Grades must be greater than 0")
                elif grade_set[1] < 0 or grade_set[1] > 1:
                    print("Weights must be greater than 0 or less than 1")
                elif weightsOverflow == False:
                    grade_list.append(grade_set)
                    counter += 1
                elif weightsOverflow == True:
                    print("The sum of your weights over 1. Try again")
            except KeyboardInterrupt:
                raise
            except:
                print("Unexpected input detected. Try again.")


    return grade_list

def calc_current_grade(grade_list):
    current_grade = round(operations.total_product(grade_list)/operations.total_weights(grade_list),2)
    return current_grade

def collect_eval_weight(grade_list):
    total_weights = operations.total_weights(grade_list)
    eval_limit = round(1 - total_weights, 2)

    evaluation_weight = None
    while evaluation_weight == None or evaluation_weight > eval_limit or evaluation_weight <= 0:
        try:
            evaluation_weight = float(input("Enter eval weight - %s Max. (0.xx): " % (eval_limit)))
            if evaluation_weight > eval_limit:
                print("Evaluation weight must be less than %s"%(eval_limit))
            elif evaluation_weight <= 0:
                print("Evaluation weight should be greater than 0 silly.")
        except KeyboardInterrupt:
            raise
        except:
            print("Unexpected input. Try again.")


    return evaluation_weight

def calc_remainder_missing(grade_list, evaluation_weight):
    total_weights = operations.total_weights(grade_list)
    if int(total_weights + evaluation_weight) != 1: # check to ensure that weights and eval equal 1
        missing_weight = round(1 - total_weights - evaluation_weight,2)
        grade_list.append((0,missing_weight))
        print("Full weight of course not reached. Missing weight of {0}. Assigning grade of 0 with weight {0}".format(missing_weight))
        return grade_list
    else:
        return grade_list

def compute_maximum(grade_list, evaluation_weight):
    total_prod = operations.total_product(grade_list)
    return round(total_prod + 100*evaluation_weight, 2) # assume you get 100 on your project grade, what mark could you get

def calc_mark(grade_list, max_grade, evaluation_weight, final_grade=0):
    min_grade = operations.total_product(grade_list)
    while final_grade <= 0 or final_grade > max_grade or final_grade < min_grade:
        try:
            final_grade = float(input("Enter your desired grade -- Max,min grade is %s,%s): "%(max_grade, min_grade)))
            if final_grade <= 0 or final_grade > max_grade:
                print("Wow really shooting for the stars. Try again smart guy.")
        except KeyboardInterrupt:
            raise
        except:
            print("Unexpected input. Try again.")
    grades_ded = 0
    for grade in grade_list:
        grades_ded += grade[0]*grade[1]

    return (final_grade, round((final_grade - grades_ded)/evaluation_weight,2))

if __name__=="__main__":
    run()
