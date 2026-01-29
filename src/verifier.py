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

def parse_matching(tokens):
    if len(tokens) == 0:
        return {}
    
    if len(tokens) % 2 != 0:
        raise ValueError("Matching file has odd number of tokens")
    
    matching = {}
    i = 0
    while i < len(tokens):
        h = int(tokens[i])
        s = int(tokens[i + 1])
        if h in matching:
            raise ValueError("Hospital " + str(h) + " appears multiple times")
        matching[h] = s
        i += 2
    
    return matching

def build_rank_table(n, preferences):
    rank = []
    i = 0
    while i <= n:
        row = [0] * (n + 1)
        rank.append(row)
        i += 1
    
    i = 1
    while i <= n:
        prefs = preferences[i - 1]
        pos = 0
        while pos < n:
            item = prefs[pos]
            rank[i][item] = pos
            pos += 1
        i += 1
    
    return rank

def check_validity(n, matching):
    # Check for right number of matches
    if len(matching) != n:
        return False, "INVALID: Expected " + str(n) + " matches, got " + str(len(matching))
    
    # Check all hospitals are present
    for h in range(1, n + 1):
        if h not in matching:
            return False, "INVALID: Hospital " + str(h) + " is not matched"
    
    # Check all students are matched once
    matched_students = list(matching.values())
    
    # Check for duplicates
    seen_students = set()
    for s in matched_students:
        if s in seen_students:
            return False, "INVALID: Student " + str(s) + " is matched to multiple hospitals"
        seen_students.add(s)
    
    # Check all students are present
    for s in range(1, n + 1):
        if s not in seen_students:
            return False, "INVALID: Student " + str(s) + " is not matched"
    
    # Check student in valid range
    for s in matched_students:
        if s < 1 or s > n:
            return False, "INVALID: Student " + str(s) + " is out of range [1, " + str(n) + "]"
        
    # Check hospitals in valid range
    for h in matching:
        if h < 1 or h > n:
            return False, "INVALID: Hospital " + str(h) + " is out of range [1, " + str(n) + "]"
    
    return True, ""

def check_stability(n, matching, hospital_preferences, student_preferences):
    # Build rank tables
    hospital_rank = build_rank_table(n, hospital_preferences)
    student_rank = build_rank_table(n, student_preferences)
    
    # Build reverse matching
    student_to_hospital = {}
    for h, s in matching.items():
        student_to_hospital[s] = h
    
    # Check all pairs
    for h in range(1, n + 1):
        current_student = matching[h]
        
        for s in range(1, n + 1):
            # Skip if already matched
            if matching[h] == s:
                continue
            
            current_hospital = student_to_hospital[s]
            
            # Does h prefer s over current match?
            h_prefers_s = hospital_rank[h][s] < hospital_rank[h][current_student]
            
            # Does s prefer h over current match?
            s_prefers_h = student_rank[s][h] < student_rank[s][current_hospital]
            
            if h_prefers_s and s_prefers_h:
                return False, "UNSTABLE: Blocking pair found - Hospital " + str(h) + " and Student " + str(s)
    
    return True, ""

def verify(n, matching, hospital_preferences, student_preferences):
    # n=0 edge case
    if n == 0:
        if len(matching) == 0:
            return True, "VALID STABLE"
        else:
            return False, "INVALID: Expected empty matching for n=0"
    
    # Check validity 
    valid, message = check_validity(n, matching)
    if not valid:
        return False, message
    
    # Check stability
    stable, message = check_stability(n, matching, hospital_preferences, student_preferences)
    if not stable:
        return False, message
    
    return True, "VALID STABLE"

def main():
    try:
        if len(sys.argv) != 3:
            print("Usage: python verifier.py <input file> <matching file>")
            return
        
        input_path = sys.argv[1]
        matching_path = sys.argv[2]
        
        # Parse preferences
        input_tokens = read_tokens(input_path)
        n, hospital_preferences, student_preferences = parse_instance(input_tokens)
        
        # Parse matching
        matching_tokens = read_tokens(matching_path)
        matching = parse_matching(matching_tokens)
        
        # Verify
        success, message = verify(n, matching, hospital_preferences, student_preferences)
        print(message)
        
    except Exception as e:
        print("Error:", e)
        return


if __name__ == "__main__":
    main()