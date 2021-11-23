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

['a','y','h','p','e','o','l','l']

Length = 8

### Running on a classical computer

On a classical computer, we would iterate through the array in order to search for each letter. For the first letter, 'h', we search up to index `3` to locate the letter. However, for letter 'l' we need to search through the entire array to locate the letter at index `7`. In the worst-case scenario, this algorithm requires searching through all elements, thus it has a time complexity of O(n).

### Running on a quantum computer

On a quantum computer, we can represent each index within the array using enough qubits to represent the length of the array. In this example, we have an array of length 8, thus we can represent this number of indices in the array using 3 qubits. This is equivalent to `2^3=8` possibilities for 3 qubits.

In simplified terms, a quantum computer can effectively search through all possibilites of qubit values in a single CPU cycle.

Imagine the 3 qubits in this example 000, 001, 010, 011, etc. being searched simulataneously for the target letter. In this manner, a single CPU cycle on a quantum computer can look in the array at each possible index and determine if the letter is located at that slot. After just 1 cycle, we can return the index `011=3` for the letter 'h'. Likewise, in a single cycle, we can locate the letter 'l' at the last index of `111=7`.

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
