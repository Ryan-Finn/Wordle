from cProfile import Profile
from csv import reader
from joblib import Parallel, delayed, cpu_count
from pstats import Stats, SortKey

from lib import getPattern, filterPoss


def func(guess1, wordle, possible, fullDict):
    if guess1 == wordle:
        return

    pattern = getPattern(guess1, wordle)
    possible2 = filterPoss(possible, guess1, pattern)

    if len(possible2) == 1:
        return

    for guess2 in fullDict:
        if guess2 == wordle or guess2 == guess1:
            continue

        pattern = getPattern(guess2, wordle)
        possible3 = filterPoss(possible2, guess2, pattern)

        if len(possible3) == 1:
            return

    return guess1


def main():
    openers = set()
    fullDict = []
    solutions = []
    possible = []
    i = 0
    try:
        with open("words.csv") as file:
            for line in reader(file):
                for word in line:
                    i += 1
                    if i >= 2153:
                        solutions.append(word)
                    possible.append(word)
                    fullDict.append(word)
    except IOError as err:
        print(err)
        return

    # known 2153

    try:
        with open("words.csv") as file:
            for line in reader(file):
                for word in line:
                    openers.add(word)
                    fullDict.append(word)
    except IOError as err:
        print(err)
        return

    i = 0
    print("Processors:", cpu_count())
    print("Openers:", len(openers))
    with Parallel(n_jobs=cpu_count(), backend='multiprocessing') as parallel:
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
