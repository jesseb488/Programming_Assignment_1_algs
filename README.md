# Programming_Assignment_1_algs

## Team Members
- Giuliano Di Lorenzo
- UFID: 85720434

- Jesse Bloom
- UFID: 30570694

## Requirements
Python 3.x
matplotlib (for benchmark graphing, install with: pip install matplotlib)

IMPORTANT: On Windows, run all commands in Command Prompt (cmd), not PowerShell. PowerShell causes issues with file output.

## How to Run

All commands should be run from the root of the repository

Matcher:
python src/matcher.py data/example.in

Verifier:
python src/verifier.py data/example.in data/example.out

Benchmark:
cd src
python bench.py

## Running Tests

From the root directory, you can run our test files:

Valid matching tests:
python src/verifier.py data/test_n1.in data/test_n1_valid.out
python src/verifier.py data/test_n2.in data/test_n2_valid.out
python src/verifier.py data/test_n3.in data/test_n3_valid.out

Invalid matching tests:
python src/verifier.py data/test_n2.in data/test_n2_invalid_duplicate.out
python src/verifier.py data/test_n2.in data/test_n2_invalid_missing.out
python src/verifier.py data/test_n3.in data/test_n3_invalid_duplicate.out

Unstable matching tests:
python src/verifier.py data/test_n2.in data/test_n2_unstable.out
python src/verifier.py data/test_n3.in data/test_n3_unstable.out

Matcher tests:
python src/matcher.py data/test_n0.in
python src/matcher.py data/test_n1.in
python src/matcher.py data/test_n2.in
python src/matcher.py data/test_n3.in

## Example Usage

Run the matcher and save output:
python src/matcher.py data/example.in > data/example.out

Verify the output is valid and stable:
python src/verifier.py data/example.in data/example.out

Expected output: VALID STABLE

## Input Format
Line 1: integer n
Next n lines: hospital preference lists
Next n lines: student preference lists

Example (data/example.in):
3
1 2 3
2 3 1
2 1 3
2 1 3
1 2 3
1 2 3

## Output Format

Matcher outputs n lines where each line is "hospital student":
1 1
2 2
3 3

Verifier outputs one of:
VALID STABLE
INVALID: (reason)
UNSTABLE: Blocking pair found - Hospital X and Student Y

## Files
src/matcher.py - Gale-Shapley matching algorithm
src/verifier.py - Validity and stability checker
src/bench.py - Benchmarking
data/example.in - Example input
data/example.out - Example output
data/test_n0.in - Edge case test input for n=0
data/test_n1.in - Edge case test input for n=1
data/test_n1_valid.out - Valid output for n=1
data/test_n2.in - Test input for n=2
data/test_n2_valid.out - Valid output for n=2
data/test_n2_invalid_duplicate.out - Invalid output (duplicate student)
data/test_n2_invalid_missing.out - Invalid output (missing match)
data/test_n2_unstable.out - Unstable output (blocking pair)
data/test_n3.in - Test input for n=3
data/test_n3_valid.out - Valid output for n=3
data/test_n3_invalid_duplicate.out - Invalid output (duplicate student)
data/test_n3_unstable.out - Unstable output (blocking pair)
benchmark_graph.png - Performance graph

## Assumptions
Input files are well formed with valid integers.
Preference lists are complete permutations of 1 to n.
Equal number of hospitals and students.

## Task C: Scalability Analysis

We benchmarked the matcher and verifier for n = 1, 2, 4, 8, 16, 32, 64, 128, 256, 512.

See benchmark_graph.png for the graph.

![Benchmark Graph](benchmark_graph.png)

Observations:
Both algorithms show O(n^2) time complexity. The verifier is slower than the matcher because it must check all n^2 hospital-student pairs for blocking pairs. The matcher is faster because Gale-Shapley often terminates before exploring all possible proposals.