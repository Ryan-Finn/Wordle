def getPattern(word, word2):
    pattern = [2, 2, 2, 2, 2]
    inds = [0, 1, 2, 3, 4]
    inds2 = [0, 1, 2, 3, 4]

    for i in range(0, 5):
        if word[i] == word2[i]:
            pattern[i] = 0
            inds.remove(i)
            inds2.remove(i)

    while True:
        fail = False

        for i in inds:
            for j in inds2:
                if word[i] == word2[j]:
                    pattern[i] = 1
                    inds.remove(i)
                    inds2.remove(j)
                    fail = True
                    break

            if fail:
                break

        if not fail:
            break

    pattern = ''.join(map(str, pattern))
    return pattern


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
        if state == "2":
            counts[word[ind]][0] = exactly
            counts[word[ind]][1] -= 1

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
            if pattern[i] == "1" and word[i] == word2[i]:
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
            if pattern[i] == "0" and word[i] != word2[i]:
                allGreen = False
                break

        if allGreen:
            possible.append(word2)

    return possible


def filterPoss(oldPoss, word, pattern):
    possible = filterGray(oldPoss, word, pattern)
    possible = filterGold(possible, word, pattern)
    possible = filterGreen(possible, word, pattern)

    return possible
