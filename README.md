# Hangman bot using information theory
Bot who can guess your word in a game of Hangman using Claude Shannon's [information theory](https://en.wikipedia.org/wiki/Information_theory). The game uses a graphical interface built using the pygame library.

## Theory
The algorithm used to guess the player's word is based on a fundamental concept in information theory: entropy. Here we give a brief introduction to the concept of entropy in information theory.

When the bot guesses a letter, it retrieves information about the player's word. For example, if the bot guesses the letter e and the player tells us that his word starts with the letter e and has no other e in the rest of the word, we eliminate from our list any words that don't match this result. We can calculate the probability of obtaining this result by dividing the number of words that match it by the total number of words. 


The unit used to calculate the information is the bit. If an observation halves the space of possibilities, we say it gives us 1 bit of information; if it divides the space of possibilities into 4, it gives us 2 bits of information. More generally, the formula for determining the amount of information obtained by an observation is :
$$
I=-\log_2(p)
$$
Where $p$ represents the probability of obtaining this observation.

We can quantify the average information from a guess using the expected value of information from a guess:
$$
    E[I]=\sum{-p(x)\cdot \log_2(p(x)) }
$$
This formula is called entropy. It's a measure of the average information we'll get guessing a letter.

## Algorithm used
We use a database of the 30000 most common words used in English as the set of possible words. Initially, the player is asked to enter the size of his word, and only words of the right size are kept.

The program will then calculate the entropy, that is, the average amount of information obtained by guessing this letter, for each letter. Let's imagine we want to calculate the entropy of the letter e. The program will consider all possible cases of guessing the letter e. Let's imagine that the player's word contains 5 letters, all possible cases are no letter e, 1 time the letter e at the beginning, 1 time the letter e as the second letter, and so on. In this way, the program determines all possible combinations. Generally speaking, there are:
$$
      n_{combinations}=\sum_{i=0}^{m} {m \choose i}
$$
where m is the lenght of the word and $n_{combinations}$ is the number of combinations. 

The probability of each case is calculated by dividing the number of matching words by the total number of words, and then calculating the entropy associated with that guess. The program finally guesses the letter with the highest entropy, that is, the letter that gives us the most information on average.

The player then enters the result, the list of possible words is updated with only those matching the result, and the previous process is repeated until only one word remains.

## GUI

The user first input the number of letter in his word : 

<img src='ressources\input_letter_lenght.png' width=300 allign=center>
<br />
<br />
The game now starts:
<br />
<br />
<img src='ressources\game_demo.png' width=300 allign=center>
<br />
<br />
The computer gives its guess at the top, the user then enters the result (in the example the word to guess is hello, the user has entered the first l but not yet the second). Once the result has been entered, the player clicks on the green button in the bottom right-hand corner. The bottom left shows the number of matching words, and the left shows the state of the hangman.
<br />
<br />
The computer then gives the answer:
<br />
<br />
<img src='ressources\result.png' width=300 allign=center>