import random
import time
import os
from matcher import read_tokens, parse_instance, build_student_rank, gale_shapley
from verifier import verify

def generate_random_input(n):
    lines = []
    lines.append(str(n))
    
    # Hospital preferences
    for i in range(n):
        prefs = list(range(1, n + 1))
        random.shuffle(prefs)
        parts = []
        for x in prefs:
            parts.append(str(x))
        line = " ".join(parts)
        lines.append(line)
    
    # Student preferences
    for i in range(n):
        prefs = list(range(1, n + 1))
        random.shuffle(prefs)
        parts = []
        for x in prefs:
            parts.append(str(x))
        line = " ".join(parts)
        lines.append(line)

    return "\n".join(lines)

def write_file(path, content):
    f = open(path, "w")
    f.write(content)
    f.close()

def run_benchmark():
    sizes = [1, 2, 4, 8, 16, 32, 64, 128, 256, 512]
    matcher_times = []
    verifier_times = []

    print("Running benchmarks\n")
    print("n\t\tMatcher\tVerifier")
    print("-" * 45)
    for n in sizes:
        # Generate random input
        input_content = generate_random_input(n)
        input_path = "temp_input.txt"
        write_file(input_path, input_content)
        
        # Parse input
        tokens = read_tokens(input_path)
        n_parsed, hospital_preferences, student_preferences = parse_instance(tokens)
        student_rank = build_student_rank(n_parsed, student_preferences)
        
        # Time matcher
        start = time.time()
        match_h = gale_shapley(n_parsed, hospital_preferences, student_rank)
        end = time.time()
        matcher_time = end - start
        matcher_times.append(matcher_time)
        matching = {}
        for h in range(1, n_parsed + 1):
            matching[h] = match_h[h]
        
        # Time verifier
        start = time.time()
        success, message = verify(n_parsed, matching, hospital_preferences, student_preferences)
        end = time.time()
        verifier_time = end - start
        verifier_times.append(verifier_time)
        
        # Print result
        print(str(n) + "\t\t" + str(round(matcher_time, 6)) + "\t" + str(round(verifier_time, 6)))
        
        # Verify the matching correct
        if not success:
            print("WARNING: Matching failed verification for n=" + str(n) + ": " + message)
    
    os.remove(input_path)
    
    print("\nBenchmark complete")

def main():
    run_benchmark()

if __name__ == "__main__":
    main()