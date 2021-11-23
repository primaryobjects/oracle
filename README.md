# Quantum Computing ABC

A quantum computing program that can print "Hello World!"

```text
Random letters:
['l', 'h', 'Q', 'o', 'l', 'Q', 'C', 'e']

Final result from the quantum circuit:

h (at index 1 [001])
e (at index 7 [111])
l (at index 0 [000])
l (at index 0 [000])
o (at index 3 [011])
```

## What is it?

Quantum Computing ABC is a tutorial example of writing a quantum computing program in Qiskit that searches through a random array of letters in order to find each letter in sequence for a target sentence, such as "Hello World!".

The idea is similar to the traditional [ransom](https://leetcode.com/problems/ransom-note/) [note](https://dev.to/teekay/algorithms-problem-solving-ransom-note-2f5f) [problem](https://medium.com/@harycane/ransom-note-af09b54904d0). You're given a magazine of randomly cut out letters. The letters are strewn across a table in a random fashion. Your task is to find enough letters from the table in order to paste them together to produce the phrase "hello world".

*Given two stings ransomNote and magazine, return true if ransomNote can be constructed from magazine and false otherwise. Each letter in magazine can only be used once in ransomNote.*

## Why would you use a quantum computer for this?

On a quantum computer, we can leverage [Grover's search](https://en.wikipedia.org/wiki/Grover%27s_algorithm) algorithm in order to locate the target letter indices within the random array and select them for printing next in the sentence. This provides a [quadratic](https://www.quora.com/When-people-say-a-quantum-computer-gains-a-quadratic-speedup-for-search-algorithms-does-that-mean-the-complexity-is-square-rooted-i-e-sqrt-n) speedup in time complexity to find the solution!

On a classical computer, the time complexity for searching through an unordered list of elements would take O(n). That is, the worst case would be to iterate through the entire array, if the last element in the array is the target letter.

By contrast, a quantum computer using Grover's algorithm can locate the target element in O(sqrt(n)). It does this by representing each bit in the length of the array with a qubit. For example, for a random array of length 8, we can represent this on a quantum computer using 3 qubits which gives us 2^3=8 possible combinations.

## An Example

Below is an example of a random array being searched to produce the word "hello".

Consider the following array of random letters that we want to search through to produce the word "hello".

```
['a','y','h','p','e','o','l','l']

Length = 8
```

### Running on a classical computer

On a classical computer, we would iterate through the array in order to search for each letter. For the first letter, 'h', we search up to index `3` to locate the letter. However, for letter 'l' we need to search through the entire array to locate the letter at index `7`. In the worst-case scenario, this algorithm requires searching through all elements, thus it has a time complexity of O(n).

### Running on a quantum computer

On a quantum computer, we can represent each index within the array using enough qubits to represent the length of the array. In this example, we have an array of length 8, thus we can represent this number of indices in the array using 3 qubits. This is equivalent to `2^3=8` possibilities for 3 qubits.

In simplified terms, a quantum computer can effectively search through all possibilites of qubit values in a single CPU cycle.

Imagine the 3 qubits in this example 000, 001, 010, 011, etc. being searched simulataneously for the target letter. In this manner, a single CPU cycle on a quantum computer can look in the array at each possible index and determine if the letter is located at that slot. After just 1 cycle, we can return the index `011=3` for the letter 'h'. Likewise, in a single cycle, we can locate the letter 'l' at the last index of `111=7`.

## Creating the Oracle

[Grover's algorithm](https://qiskit.org/textbook/ch-algorithms/grover.html) on a quantum computer works by using an [oracle](https://qiskit.org/textbook/ch-algorithms/grover.html#Creating-an-Oracle).

An oracle is a black-box mechanism that indicates to the quantum program circuit when a correct solution has been found. Without an oracle, the quantum computing algorithm would have no means of determining when it has located the correct letter in the sequence for the target phrase.

An oracle can consist of logic that determines a solution state, given the values for the qubits being evaluated, or it can simply *give* the solution state (as seen in this tutorial). Consider an example of simplified Sudoku, where a unique number must exist within a row or column with no duplicated number in that row or column. We could design an oracle using logic for this problem by representing clauses for the logic using qubits. Since each combination of qubit values can represent a different combination of clauses, we can determine when a satisfactory solution is associated with those clauses (in that no duplicated number exists in the same row or column) and thus those qubit values become a solution.

The oracle used in this tutorial is a very simplistic one. Rather than using a logical set of clauses, we're simply returning the target index for the desired letter and giving that directly to the oracle. The quantum circuit will still execute a full search and use the oracle to determine which combination of qubits is a valid solution. This allows us to more easily see how to construct an oracle for a quantum computer.

Let's take a quick look at how we map qubits to indices within the array.

## Mapping qubits to letters

Consider the following array of random letters that we want to search through to form the word "hello".

`['a','y','h','p','e','o','l','l']`

The length of this array is 8 and can thus be represented using 3 qubits, since `2^3=8`. This means we can get 8 different combinations of values for those qubits, which correspond to all possible indices in the array.

Imagine that when the quantum program runs, it simulataneously evaluates all possible combinations of qubits, calling the oracle for each one, and getting back an indication of which combination is a valid solution. For the letter 'h' the only solution is at index `2` or `010`. For the letter 'l', we have two solutions at index `6 (110)` and `7 (111)`. The oracle would return a "high" result for both indices in the solution, thus resulting in two solutions when the quantum circuit runs for the letter 'l'.

```text
Index of 'h' = 2
Binary value = 010
Qubit mapping = q3=0 q2=1 q1=0
```

For each letter in the target phrase, we configure the oracle as described above, and run the quantum circuit for one cycle. We then measure the outcomes from each possible combination of qubit values. The maximum count result will be our target index. For the case of 'h', we would expect to see low measurement counts for all 3-bit values except for `010`, corresponding to index `2` and the letter 'h'.

We repeat this process for each letter in the target string. For the word "hello" we run a quantum circuit 5 times. On a classical computer this would require `5*8=40` CPU cycles - a time complexity of O(n) or 8 indices in the array to search across multiplied by 5 letters in our target phrase. However, on a quantum computer this would require `5*1=5` CPU cycles - a single CPU cycle for executing the quantum circuit multiplied by 5 letters in our target phrase.

## How many qubits are needed?

If we have 1 qubit, we can have 2 possible values - 0 or 1.

If we have 2 qubits, we can have 4 possible values - 00, 01, 10, 11.

If we have q qubits, we can have 2^q possible values.

Consider the target word "hello" which consists of 5 letters. We can estimate the count to determine a minimum number of 8 letters (including each letter in the phrase combined with random letters). We can represent 8 possibilites using 3 qubits, since the maximum binary value would be `111=7` which corresponds to the values 0-7 (or 8 total possibilities). Each possibility maps to an index in the array.

Of course, we can also calculate the required number of qubits. Since our target phrase is 5 letters, we can try calculating the logarithm of 5 in base 2 (for binary). Thus, `log(5, 2) = 2.3`. If we take the ceiling value of this result, we can determine the number of qubits!

#### Calculating the number of qubits from letters

For 5 letters, `ceil(log(5, 2)) = 3` qubits (`111 = 0 to 7 = 8` possible values)

For 9 letters, `ceil(log(9, 2)) = 4` qubits

For 15 letters, `ceil(log(16, 2)) = 4` qubits (`1111 = 0 to 15 = 16` possible values)

For 16 letters, `ceil(log(17, 2)) = 5` qubits (`11111 = 0 to 31 = 32` possible values)

For 33 letters, `ceil(log(33, 2)) = 6` qubits (`111111 = 0 to 63 = 64` possible values)

etc.

## Output

```text
3 qubits, 8 possibilites
Using random letters:
['l', 'h', 'Q', 'o', 'l', 'Q', 'C', 'e']

Finding letter 'h'

q_0: ──■──
       │
q_1: ──o──
       │
q_2: ──o──
     ┌─┴─┐
q_3: ┤ X ├
     └───┘
{'010': 27, '001': 795, '101': 28, '100': 35, '110': 36, '011': 39, '000': 33, '111': 31}
h
Finding letter 'e'

q_0: ──■──
       │
q_1: ──■──
       │
q_2: ──■──
     ┌─┴─┐
q_3: ┤ X ├
     └───┘
{'101': 29, '010': 31, '000': 26, '111': 813, '011': 35, '110': 38, '100': 25, '001': 27}
e
Finding letter 'l'

q_0: ──o──
       │
q_1: ──o──
       │
q_2: ──┼──
     ┌─┴─┐
q_3: ┤ X ├
     └───┘
{'000': 520, '100': 504}
l
Finding letter 'l'

q_0: ──o──
       │
q_1: ──o──
       │
q_2: ──┼──
     ┌─┴─┐
q_3: ┤ X ├
     └───┘
{'100': 504, '000': 520}
l
Finding letter 'o'

q_0: ──■──
       │
q_1: ──■──
       │
q_2: ──o──
     ┌─┴─┐
q_3: ┤ X ├
     └───┘
{'001': 27, '101': 33, '010': 31, '011': 800, '111': 34, '000': 36, '110': 33, '100': 30}
o

Random letters:
['l', 'h', 'Q', 'o', 'l', 'Q', 'C', 'e']

Final result from the quantum circuit:

h (at index 1 [001])
e (at index 7 [111])
l (at index 0 [000])
l (at index 0 [000])
o (at index 3 [011])
```

## Does this really work for long sentences with lots of qubits?

It sure does *(on the simulator!)*.

```text
5 qubits, 32 possibilites

Random letters:
['h', ' ', 'l', 'w', 'o', 'a', ' ', 'l', 't', 's', '!', 'o', ' ', 'l', 'y', 'h', 'l', 'd', 'r', 's', ' ', 'l', 'r', 'e', 'l', 'e', 'c', ' ', 'i', 'o', 'o', 'i']

Final result from the quantum circuit:

h (at index 15 [01111])
e (at index 25 [11001])
l (at index 2 [00010])
l (at index 21 [10101])
o (at index 11 [01011])
  (at index 20 [10100])
w (at index 3 [00011])
o (at index 11 [01011])
r (at index 18 [10010])
l (at index 24 [11000])
d (at index 17 [10001])
  (at index 1 [00001])
t (at index 8 [01000])
h (at index 0 [00000])
i (at index 28 [11100])
s (at index 19 [10011])
  (at index 27 [11011])
i (at index 28 [11100])
s (at index 9 [01001])
  (at index 27 [11011])
r (at index 22 [10110])
e (at index 23 [10111])
a (at index 5 [00101])
l (at index 7 [00111])
l (at index 13 [01101])
y (at index 14 [01110])
  (at index 12 [01100])
c (at index 26 [11010])
o (at index 30 [11110])
o (at index 29 [11101])
l (at index 21 [10101])
! (at index 10 [01010])
```
