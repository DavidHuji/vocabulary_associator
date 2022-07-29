# Vocabulary Associator
Visual associations generator for accelerating foreign vocabulary acquisition. Please read the attached report.pdf file for full description.

![Components:](https://github.com/DavidHuji/vocabulary_associator/blob/main/scheme.png)

## Example of output
![Components:](https://github.com/DavidHuji/vocabulary_associator/blob/main/example.png)


## Running
After pip-install the requirements it is recommended to start with running the test.py file but you can also run the other files for testing each component separately.

## Todo List
Features:
1. Enable to use 2 source languages for bilinguals rather than only one.
2. 

Algorithmic improvements:
1. The bigger the source vocabulary, the better the sounds match. e.g. we try to increase it by adding pairs of short words. Though, it increases the computation time dramatically. So find ways to make the sorting more efficient by preprocessing the data, for example, instead of calculating distance and then sorting, maybe we can try to directly look for the words that we think should match.
2. GPT3's sentences are not always easy to visualize, so try to find a way (maybe a prompt) that will solve it.
3. 
