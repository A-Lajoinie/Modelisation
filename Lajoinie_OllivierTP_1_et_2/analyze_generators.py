import csv
import math

def load_data(filepath):
    """
    Loads the CSV file and concatenates the binary strings into a single bit string.
    """
    try:
        full_bit_string = ""
        with open(filepath, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            # Skip header if present. The file has 'Index,Number'
            header = next(reader, None)
            
            for row in reader:
                if len(row) >= 2:
                    # The second column contains the 128-bit string
                    full_bit_string += row[1].strip()
                    
        return full_bit_string
    except Exception as e:
        print(f"Error loading {filepath}: {e}")
        return None

def monobit_test(bit_string):
    """
    Test 1: Frequency (Monobit) Test
    Checks if the number of 0s and 1s are approximately equal.
    """
    n = len(bit_string)
    n0 = bit_string.count('0')
    n1 = bit_string.count('1')
    
    print(f"  [Monobit] Total bits: {n}")
    print(f"  [Monobit] 0s: {n0}, 1s: {n1}")
    
    statistic = ((n0 - n1) ** 2) / n
    passed = statistic < 3.8415
    
    return {
        "test": "Monobit (Frequence)",
        "statistic": statistic,
        "passed": passed,
        "n0": n0,
        "n1": n1
    }

def runs_test(bit_string):
    """
    Test 2: Runs Test (Wald-Wolfowitz)
    Checks if the number of runs (sequences of identical bits) is as expected.
    """
    n = len(bit_string)
    n0 = bit_string.count('0')
    n1 = bit_string.count('1')
    
    # Count runs
    runs = 1
    for i in range(1, n):
        if bit_string[i] != bit_string[i-1]:
            runs += 1
            
    # Expected mean and variance
    expected_runs = 1 + (2 * n0 * n1) / n
    variance = (2 * n0 * n1 * (2 * n0 * n1 - n)) / (n * n * (n - 1))
    
    z_stat = (runs - expected_runs) / math.sqrt(variance)
    
    print(f"  [Runs] Total runs: {runs}")
    print(f"  [Runs] Runs attendus: {expected_runs:.2f}")
    
    # Critical value for alpha=0.05 (two-tailed) is 1.96
    passed = abs(z_stat) < 1.96
    
    return {
        "test": "Runs (Suites)",
        "statistic": z_stat,
        "passed": passed,
        "runs": runs,
        "expected": expected_runs
    }

def block_frequency_test(bit_string, M=128):
    """
    Test 2: Frequency Test within a Block
    Partitions the sequence into N = n/M blocks.
    Checks if the proportion of 1s in each block is approx 1/2.
    """
    n = len(bit_string)
    N = n // M # Number of blocks
    
    sum_chi = 0
    for i in range(N):
        block = bit_string[i*M : (i+1)*M]
        pi = block.count('1') / M
        sum_chi += (pi - 0.5) ** 2
        
    statistic = 4 * M * sum_chi
    
    z_score = (statistic - N) / math.sqrt(2 * N)
    
    passed = abs(z_score) < 1.96 
    
    return {
        "test": f"Frequence par Bloc (M={M})",
        "statistic": statistic,
        "z_score": z_score,
        "passed": passed
    }

def longest_run_ones_in_block_test(bit_string, M=128):
    """
    Test 4: Longest Run of Ones in a Block
    """
    n = len(bit_string)
    N = n // M
    
    # Classes for M=128 (K=6 bins)
    # Expected probabilities for M=128 (from NIST)
    pi = [0.1174, 0.2430, 0.2493, 0.1752, 0.1027, 0.1124]
    
    counts = [0] * 6
    
    for i in range(N):
        block = bit_string[i*M : (i+1)*M]
        
        # Find longest run of 1s
        max_run = 0
        current_run = 0
        for bit in block:
            if bit == '1':
                current_run += 1
                if current_run > max_run:
                    max_run = current_run
            else:
                current_run = 0
        
        # Binning
        if max_run <= 4:
            counts[0] += 1
        elif max_run == 5:
            counts[1] += 1
        elif max_run == 6:
            counts[2] += 1
        elif max_run == 7:
            counts[3] += 1
        elif max_run == 8:
            counts[4] += 1
        else: # >= 9
            counts[5] += 1
            
    # Chi-square
    chi_sq = 0
    for i in range(6):
        expected = N * pi[i]
        chi_sq += ((counts[i] - expected) ** 2) / expected
        
    passed = chi_sq < 11.0705
    
    return {
        "test": f"Suite la plus longue (M={M})",
        "statistic": chi_sq,
        "passed": passed,
        "counts": counts
    }

def main():
    files = [
        r"generator1.csv",
        r"generator2.csv"
    ]
    
    for filepath in files:
        print(f"\n{'='*40}")
        print(f"Analyse de {filepath}...")
        bit_string = load_data(filepath)
        if bit_string:
            results = []
            
            # Test 1: Monobit
            results.append(monobit_test(bit_string))
            
            # Test 2: Block Frequency (M=128)
            results.append(block_frequency_test(bit_string, M=128))
            
            # Test 3: Runs (Suites de 0s et 1s)
            results.append(runs_test(bit_string))
            
            # Test 4: Longest Run of Ones in a Block (M=128)
            results.append(longest_run_ones_in_block_test(bit_string, M=128))
            
            print("-" * 20)
            print("Resume:")
            all_passed = True
            for res in results:
                status = "SUCCES" if res['passed'] else "ECHEC"
                if not res['passed']:
                    all_passed = False
                stat_val = res['statistic']
                print(f"{res['test']:<30} : {status} (Stat: {stat_val:.4f})")
            
            print("-" * 20)
            if all_passed:
                print("CONCLUSION: Tous les tests sont passes. C'est probablement aleatoire.")
            else:
                print("CONCLUSION: Certains tests ont echoue. Ce n'est pas aleatoire.")

if __name__ == "__main__":
    main()
