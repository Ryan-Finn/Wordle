from cProfile import Profile
from csv import reader
from joblib import Parallel, delayed
from pstats import Stats, SortKey

from lib import getPattern, filterPoss


def func(guess1, wordle, possible, fullDict):
    if guess1 == wordle:
        return

    pattern = getPattern(guess1, wordle)
    possible2 = filterPoss(possible, guess1, pattern)

    if len(possible2) == 1 and possible2[0] == wordle:
        return guess1

    for guess2 in fullDict:
        if guess2 == wordle:
            continue

        pattern = getPattern(guess2, wordle)
        possible3 = filterPoss(possible2, guess2, pattern)

        if len(possible3) == 1 and possible3[0] == wordle:
            return

    return guess1


def main():
    openers = set()
    fullDict = []
    solutions = []
    possible = []

    try:
        with open("words.csv") as file:
            for line in reader(file):
                for word in line:
                    solutions.append(word)
                    possible.append(word)
    except IOError as err:
        print(err)
        return

    try:
        with open("words2.csv") as file:
            for line in reader(file):
                for word in line:
                    openers.add(word)
                    fullDict.append(word)
    except IOError as err:
        print(err)
        return

    i = 0
    print(len(openers))
    with Parallel(n_jobs=8, backend='multiprocessing') as parallel:
        for wordle in solutions:
            i += 1

            toRemove = parallel(delayed(func)(guess, wordle, possible, fullDict)
                                for guess in openers)

            for word in filter(lambda el: el is not None, toRemove):
                openers.discard(word)

            print(len(openers), wordle, i)
            if len(openers) == 0:
                break

    print(openers)


if __name__ == "__main__":
    with Profile() as pf:
        main()

    stats = Stats(pf)
    stats.sort_stats(SortKey.TIME)
    stats.print_stats()
