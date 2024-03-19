import sys
import scipy


def load_data(file_path):
    data = []
    
    with open(file_path, 'r') as file:
        data.append(file.readline().strip()) # Count of undefined.
        data.append(file.readline().strip().replace(' ', '')) # Goal funktion.
        data.append([])
        while line := file.readline().strip().replace(' ', ''): # Limits.
            data[2].append(line)
    
    return tuple(data)


def get_coef(count_of_undef, goal_fun, limits):
    def get_neighbors(array, index):
        """
            return the neighbors of the element under index.
        """
        return (array[index - 1], array[index + 1])
    
    def get_coef_from(array, stop_sign=None):
        coef_array = [0 for _ in range(count_of_undef)]
        for i in range(len(array)):
            if array[i] == stop_sign:
                break
            
            if array[i] == 'x':
                (coef, num_undef) = get_neighbors(array, i)
                # if coef is not a number it means we have 1 near by x.
                try:
                    coef = int(coef)
                except:
                    coef = 1

                if array[i - 2] == '-' or array[i - 1] == '-':
                    coef_array[int(num_undef) - 1] = -coef
                else:
                    coef_array[int(num_undef) - 1] = coef
                i += 2
        return coef_array
    
    func_coef = get_coef_from(goal_fun)
    a_ub = []
    b_ub = []
    for limit in limits:
        a_ub.append(get_coef_from(limit, '<'))
        b_part = limit[limit.find("=") + 1:]
        b_ub.append(int(b_part))
    
    return (func_coef, a_ub, b_ub)


def main():
    if len(sys.argv) != 2:
        print("I take not enough param!!!")
        sys.exit(-1)
    
    (count_of_undef, goal_fun, limits) = load_data(sys.argv[1])
    (func_coef, a_ub, b_ub) = get_coef(int(count_of_undef), goal_fun[0 : goal_fun.rfind('-') ], limits)

    isMax = False
    if "max" in goal_fun: # Convert to min.
        func_coef = [item * (-1) for item in func_coef]
        isMax = True

    result = scipy.optimize.linprog(
        func_coef,
        A_ub=a_ub,
        b_ub=b_ub
    )   

    if result.success:
        print("x:", result.x)
        print("value of goal func:", end='')
        print(result.fun if not isMax else -result.fun)
    else:
        print("Could not found.")


if __name__ == "__main__":
    main()