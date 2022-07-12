from math import log2
from csv import reader

show = False
table = dict()


def getPattern(word, word2):
    if word == word2:
        return " 00000"

    global table
    if f"{word}{word2}" in table:
        return table[f"{word}{word2}"]

    pattern = [" ", 2, 2, 2, 2, 2]
    inds = [0, 1, 2, 3, 4]
    inds2 = [0, 1, 2, 3, 4]

    for i in range(0, 5):
        if word[i] == word2[i]:
            pattern[i + 1] = 0
            inds.remove(i)
            inds2.remove(i)

    while True:
        fail = False

        for i in inds:
            for j in inds2:
                if word[i] == word2[j]:
                    pattern[i + 1] = 1
                    inds.remove(i)
                    inds2.remove(j)
                    fail = True
                    break

            if fail:
                break

        if not fail:
            break

    table[f"{word}{word2}"] = ''.join(map(str, pattern))

    return table[f"{word}{word2}"]


def bestGuess(dictionary, possible):
    k = 0
    length = len(dictionary)
    length2 = len(possible)
    lgLength = log2(length2)
    best = 0
    guess = possible[0]
    global table

    if length2 == 1:
        return guess

    for word in dictionary:
        if len(table) >= 40000000:
            table = dict()

        if show:
            if k % (length // 10 + 1) == 0:
                print(f"{100 * k // length}%")
            k += 1

        entropy = 0
        patterns = dict()

        for word2 in possible:
            pattern = getPattern(word, word2)

            if pattern in patterns:
                patterns[pattern] += 1.0
            else:
                patterns[pattern] = 1.0

        for _, count in patterns.items():
            entropy += count * log2(count)
        entropy = lgLength - entropy / length2

        if best < entropy:
            best = entropy
            guess = word

    if show:
        print("100%")

    return guess


def filterGray(oldPoss, word, pattern):
    possible = []
    counts = dict()
    atLeast = True
    exactly = False

    for letter in word:
        if letter in counts:
            counts[letter][1] += 1
        else:
            counts[letter] = [atLeast, 1]

    for ind, state in enumerate(pattern):
        if ind != 0 and state == "2":
            counts[word[ind - 1]][0] = exactly
            counts[word[ind - 1]][1] -= 1

    for word2 in oldPoss:
        if word == word2:
            continue

        counts2 = dict()
        for letter in counts:
            if letter not in counts2:
                counts2[letter] = 0

            for i in range(0, 5):
                if letter == word2[i]:
                    counts2[letter] += 1

        fail = False
        for letter, count in counts.items():
            if count[0]:
                if count[1] > counts2[letter]:
                    fail = True
                    break
            else:
                if count[1] != counts2[letter]:
                    fail = True
                    break

        if not fail:
            possible.append(word2)

    return possible


def filterGold(oldPoss, word, pattern):
    possible = []

    for word2 in oldPoss:
        fail = False

        for i in range(0, 5):
            if pattern[i + 1] == "1" and word[i] == word2[i]:
                fail = True
                break

        if not fail:
            possible.append(word2)

    return possible


def filterGreen(oldPoss, word, pattern):
    possible = []

    for word2 in oldPoss:
        allGreen = True

        for i in range(0, 5):
            if pattern[i + 1] == "0":
                if word[i] != word2[i]:
                    allGreen = False

        if allGreen:
            possible.append(word2)

    return possible


def filterPoss(oldPoss, word, pattern):
    possible = filterGray(oldPoss, word, pattern)
    possible = filterGold(possible, word, pattern)
    possible = filterGreen(possible, word, pattern)

    if show:
        print(possible)
        print()

    return possible


def think(dictionary, possible, wordle):
    guess = bestGuess(dictionary, possible)
    dictionary.remove(guess)
    pattern = getPattern(guess, wordle)

    if show:
        print("Guess:", guess, pattern)

    possible = filterPoss(possible, guess, pattern)

    return guess, possible


def play(dictionary, possible, wordle):
    # guess = "raise"  # 3.674750974447813
    # guess = "soare"  #
    guess = "tares"  # 4.169770463404071
    dictionary.remove(guess)
    pattern = getPattern(guess, wordle)
    if show:
        print("Guess:", guess, pattern)

    possible = filterPoss(possible, guess, pattern)
    score = 1

    while len(possible) > 0:
        if len(possible) == 2:
            dictionary = possible

        guess, possible = think(dictionary, possible, wordle)
        score += 1

    if guess != wordle:
        print("OOF:", wordle)
        return 0

    if show:
        print("Answer:", guess)
        print("Score:", score)

    return score


def main():
    dictionary = []
    solutions = []
    possible = []

    try:
        with open("words2.csv") as file:
            for line in reader(file):
                for word in line:
                    solutions.append(word)
    except IOError as err:
        print(err)
        return

    try:
        with open("words2.csv") as file:
            for line in reader(file):
                for word in line:
                    dictionary.append(word)
                    possible.append(word)
    except IOError as err:
        print(err)
        return

    # wordle = "antar"
    # play(dictionary, possible, wordle)
    # print()

    # print(bestGuess(dictionary, solutions))

    i = 0
    avgScore = 0
    length = len(solutions)
    for wordle in solutions:
        if i % (length // 100 + 1) == 0:
            print(f"{100 * i // length}%")
        i += 1

        print(wordle)
        score = play(dictionary.copy(), possible.copy(), wordle)
        if score == 0:
            length -= 1

        avgScore += score

    print(avgScore / length)


if __name__ == "__main__":
    main()
