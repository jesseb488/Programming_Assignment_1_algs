import sys



def read_tokens(path):
    f = open(path, "r")
    data = f.read()
    f.close()
    return data.split()

def parse_instance(tokens):
    if len(tokens) == 0:
        raise ValueError("Empty Input")
    
    n = int(tokens[0])

    if n == 0:
        return 0, [], []
    
    numbers = []
    i = 1
    while i < len(tokens):
        numbers.append(int(tokens[i]))
        i += 1

    expected = 2 * n * n
    if len(numbers) != expected:
        raise ValueError("Input doesn't have the right amount of numbers")
    
    hospital_preferences = []
    index = 0
    count = 0
    while count < n:
        line = numbers[index:index + n]
        hospital_preferences.append(line)
        index += n
        count += 1

    student_preferences = []
    count = 0
    while count < n:
        line = numbers[index:index + n]
        student_preferences.append(line)
        index += n
        count += 1

    return n, hospital_preferences, student_preferences


def build_student_rank(n, student_preferences):
    student_rank = []
    s = 0
    while s <= n:
        row = [0] * (n+1)
        student_rank.append(row)
        s += 1

    s = 1
    while s <= n:
        preferences = student_preferences[s-1]
        index_2 = 0
        while index_2 < n:
            h = preferences[index_2]
            student_rank[s][h] = index_2
            index_2 += 1
        s += 1

    return student_rank


