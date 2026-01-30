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
    
    os.remove(input_path)
    
    return sizes, matcher_times, verifier_times

def create_graph(sizes, matcher_times, verifier_times):
    try:
        import matplotlib.pyplot as plt
        
        plt.figure(figsize=(10, 6))
        plt.plot(sizes, matcher_times, marker='o', label='Matcher')
        plt.plot(sizes, verifier_times, marker='s', label='Verifier')
        
        plt.xlabel('n (number of hospitals/students)')
        plt.ylabel('Running Time (seconds)')
        plt.title('Gale-Shapley Matcher and Verifier Performance')
        plt.legend()
        plt.grid(True)
        plt.xscale('log', base=2)
        plt.ticklabel_format(axis='y', style='plain', useOffset=False)
        plt.gca().yaxis.set_major_formatter(plt.FormatStrFormatter('%.6f'))
        
        plt.savefig('benchmark_graph.png')
        print("\n**************************************************")
        print("Graph saved to benchmark_graph.png (In SRC Folder)")
        print("**************************************************")
        
    except ImportError:
        print("matplotlib not installed. Run: pip install matplotlib")

def main():
    sizes, matcher_times, verifier_times = run_benchmark()
    create_graph(sizes, matcher_times, verifier_times)

if __name__ == "__main__":
    main()