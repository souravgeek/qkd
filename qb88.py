import random
import matplotlib.pyplot as plt

# --------------- Helper Functions ---------------

def random_bits(length):
    return [random.randint(0, 1) for _ in range(length)]

def random_bases(length):
    return [random.choice(['+', 'x']) for _ in range(length)]

def encode_qubits(bits, bases):
    # Representation only; real qubits aren't stored this way
    return list(zip(bits, bases))

def eve_intercepts(qubits):
    eve_bases = random_bases(len(qubits))
    intercepted_qubits = []

    for i, (bit, base) in enumerate(qubits):
        if eve_bases[i] == base:
            intercepted_qubits.append((bit, base))  # same basis, bit unchanged
        else:
            # Eve chooses a wrong basis, guesses randomly
            intercepted_qubits.append((random.randint(0, 1), eve_bases[i]))
    return intercepted_qubits

def bob_measures(qubits, bob_bases):
    results = []
    for (bit, a_base), b_base in zip(qubits, bob_bases):
        if a_base == b_base:
            results.append(bit)  # Correct measurement
        else:
            results.append(random.randint(0, 1))  # Random guess
    return results

def extract_key(bits_a, bits_b, bases_a, bases_b):
    return [a for a, b, ba, bb in zip(bits_a, bits_b, bases_a, bases_b) if ba == bb]

def compute_qber(alice_key, bob_key):
    errors = sum([a != b for a, b in zip(alice_key, bob_key)])
    return (errors / len(alice_key)) * 100 if alice_key else 0

def print_visual_tracker(bits, a_bases, b_bases):
    print("Alice Bits:  ", bits)
    print("Alice Bases: ", a_bases)
    print("Bob Bases:   ", b_bases)
    matches = ['✅' if a == b else '❌' for a, b in zip(a_bases, b_bases)]
    print("Basis Match: ", matches)

# --------------- Simulation Parameters ---------------

NUM_BITS = 100
simulate_eve = True  # Toggle Eve

# --------------- Step 1: Alice generates bits and bases ---------------
alice_bits = random_bits(NUM_BITS)
alice_bases = random_bases(NUM_BITS)
qubits = encode_qubits(alice_bits, alice_bases)

# --------------- Step 2: Eve intercepts ---------------
if simulate_eve:
    qubits = eve_intercepts(qubits)  # Eve modifies the qubits

# --------------- Step 3: Bob measures ---------------
bob_bases = random_bases(NUM_BITS)
bob_bits = bob_measures(qubits, bob_bases)

# --------------- Step 4: Extract shared key ---------------
shared_alice_key = extract_key(alice_bits, bob_bits, alice_bases, bob_bases)
shared_bob_key = extract_key(bob_bits, bob_bits, alice_bases, bob_bases)
qber = compute_qber(shared_alice_key, shared_bob_key)

# --------------- Step 5: Print & Visualize ---------------
print_visual_tracker(alice_bits, alice_bases, bob_bases)
print("\nRaw Key (Alice):", shared_alice_key)
print("Raw Key (Bob):  ", shared_bob_key)
print(f"\nQuantum Bit Error Rate (QBER): {qber:.2f}%")

# --------------- Step 6: Plot QBER ---------------
plt.figure(figsize=(6, 4))
plt.bar(['QBER'], [qber], color='orange')
plt.ylim(0, 100)
plt.ylabel('QBER (%)')
plt.title('Quantum Bit Error Rate with' + (' Eve' if simulate_eve else 'out Eve'))
plt.grid(axis='y')
plt.tight_layout()
plt.show()