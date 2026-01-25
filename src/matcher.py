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


def print_matchings(n, match_h):
    h = 1
    while h <= n:
        print(str(h) + " " + str(match_h[h]))
        h += 1


def gale_shapley(n, hospital_preferences, student_rank):
    match_h = [0] * (n + 1)
    match_s = [0] * (n + 1)
    next_option = [0] * (n + 1)

    free_hospitals = []
    h = 1
    while h <= n:
        free_hospitals.append(h)
        h += 1

    i = 0
    while i < len(free_hospitals):
        h = free_hospitals[i]
        i += 1

        if next_option[h] >= n:
            continue

        s = hospital_preferences[h - 1][next_option[h]]
        next_option[h] += 1

        if match_s[s] == 0:
            match_h[h] = s
            match_s[s] = h
        else:
            current_h = match_s[s]
            if student_rank[s][h] < student_rank[s][current_h]:
                match_h[h] = s
                match_s[s] = h
                match_h[current_h] = 0
                free_hospitals.append(current_h)
            else:
                if next_option[h] < n:
                    free_hospitals.append(h)

    return match_h

def main():
    try:
        if len(sys.argv) !=2:
            print("Incorrect input, usage: python src/matcher.py <input file>")
            return
        
        path = sys.argv[1]
        tokens = read_tokens(path)
        n, hospital_preferences, student_preferences = parse_instance(tokens)


        if n == 0:
            return
        
        student_rank = build_student_rank(n, student_preferences)
        match_h = gale_shapley(n, hospital_preferences, student_rank)
        print_matchings(n, match_h)
    
    except Exception as e:
        print("Error:", e)
        return


if __name__ == "__main__":
    main()