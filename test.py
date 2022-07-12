from csv import reader
from joblib import Memory
from multiprocessing import Pool

show = False
memory = Memory("./cache", compress=True, verbose=False)


@memory.cache
def getPattern(word, word2):
    if word == word2:
        return " 00000"

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

    return ''.join(map(str, pattern))


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


def func(args):
    guess = args[0]
    wordle = args[1]
    possible = args[2]

    if guess == wordle:
        return False
    return len(filterPoss(possible, guess, getPattern(guess, wordle))) == 1


class iterable(object):
    def __init__(self, start, dictionary, wordle, possible):
        self.i = 0
        self.index = range(start, len(dictionary))
        self.sz = len(self.index)
        self.dictionary = dictionary
        self.wordle = wordle
        self.possible = possible

    def __iter__(self):
        return self

    def __next__(self):
        self.i += 1

        if self.i >= self.sz:
            raise StopIteration
        else:
            return self.dictionary[self.index[self.i - 1]], self.wordle, self.possible


def main():
    dictionary2 = []
    solutions = []
    possible = []

    try:
        with open("words.csv") as file:
            for line in reader(file):
                for word in line:
                    solutions.append(word)
    except IOError as err:
        print(err)
        return

    try:
        with open("words.csv") as file:
            for line in reader(file):
                for word in line:
                    dictionary2.append(word)
                    possible.append(word)
    except IOError as err:
        print(err)
        return

    dictionary = ['cigar', 'rebut', 'sissy', 'humph', 'awake', 'blush', 'focal', 'evade', 'naval', 'serve', 'heath',
                  'dwarf', 'model', 'karma', 'stink', 'grade', 'quiet', 'bench', 'abate', 'feign', 'major', 'death',
                  'fresh', 'crust', 'stool', 'colon', 'abase', 'marry', 'react', 'batty', 'pride', 'floss', 'helix',
                  'croak', 'staff', 'paper', 'unfed', 'whelp', 'trawl', 'outdo', 'adobe', 'crazy', 'sower', 'repay',
                  'digit', 'crate', 'cluck', 'spike', 'mimic', 'pound', 'maxim', 'linen', 'unmet', 'flesh', 'booby',
                  'forth', 'first', 'stand', 'belly', 'ivory', 'seedy', 'print', 'yearn', 'drain', 'bribe', 'stout',
                  'panel', 'crass', 'flume', 'offal', 'agree', 'error', 'swirl', 'argue', 'bleed', 'delta', 'flick',
                  'totem', 'wooer', 'front', 'shrub', 'parry', 'biome', 'lapel', 'start', 'greet', 'goner', 'golem',
                  'lusty', 'loopy', 'round', 'audit', 'lying', 'gamma', 'labor', 'islet', 'civic', 'forge', 'corny',
                  'moult', 'basic', 'salad', 'agate', 'spicy', 'spray', 'essay', 'fjord', 'spend', 'kebab', 'guild',
                  'aback', 'motor', 'alone', 'hatch', 'hyper', 'thumb', 'dowry', 'ought', 'belch', 'dutch', 'pilot',
                  'tweed', 'comet', 'jaunt', 'enema', 'steed', 'abyss', 'growl', 'fling', 'dozen', 'boozy', 'erode',
                  'world', 'gouge', 'click', 'briar', 'great', 'altar', 'pulpy', 'blurt', 'coast', 'duchy', 'groin',
                  'fixer', 'group', 'rogue', 'badly', 'smart', 'pithy', 'gaudy', 'chill', 'heron', 'vodka', 'finer',
                  'surer', 'radio', 'rouge', 'perch', 'retch', 'wrote', 'clock', 'tilde', 'store', 'prove', 'bring',
                  'solve', 'cheat', 'grime', 'exult', 'usher', 'epoch', 'triad', 'break', 'rhino', 'viral', 'conic',
                  'masse', 'sonic', 'vital', 'trace', 'using', 'peach', 'champ', 'baton', 'brake', 'pluck', 'craze',
                  'gripe', 'weary', 'picky', 'acute', 'ferry', 'aside', 'tapir', 'troll', 'unify', 'rebus', 'boost',
                  'truss', 'siege', 'tiger', 'banal', 'slump', 'crank', 'gorge', 'query', 'drink', 'favor', 'abbey',
                  'tangy', 'panic', 'solar', 'shire', 'proxy', 'point', 'robot', 'prick', 'wince', 'crimp', 'knoll',
                  'sugar', 'whack', 'mount', 'perky', 'could', 'wrung', 'light', 'those', 'moist', 'shard', 'pleat',
                  'aloft', 'skill', 'elder', 'frame', 'humor', 'pause', 'ulcer', 'ultra', 'robin', 'cynic', 'aroma',
                  'caulk', 'shake', 'dodge', 'swill', 'tacit', 'other', 'thorn', 'trove', 'bloke', 'vivid', 'spill',
                  'chant', 'choke', 'rupee', 'nasty', 'mourn', 'ahead', 'brine', 'cloth', 'hoard', 'sweet', 'month',
                  'lapse', 'watch', 'today', 'focus', 'smelt', 'tease', 'cater', 'movie', 'saute', 'allow', 'renew',
                  'their', 'slosh', 'purge', 'chest', 'depot', 'epoxy', 'nymph', 'found', 'shall', 'stove', 'lowly',
                  'snout', 'trope', 'fewer', 'shawl', 'natal', 'comma', 'foray', 'scare', 'stair', 'black', 'squad',
                  'royal', 'chunk', 'mince', 'shame', 'cheek', 'ample', 'flair', 'foyer', 'cargo', 'oxide', 'plant',
                  'olive', 'inert', 'askew', 'heist', 'shown', 'zesty', 'trash', 'larva', 'forgo', 'story', 'hairy',
                  'train', 'homer', 'badge', 'midst', 'canny', 'shine', 'gecko', 'farce', 'slung', 'tipsy', 'metal',
                  'yield', 'delve', 'being', 'scour', 'glass', 'gamer', 'scrap', 'money', 'hinge', 'album', 'vouch',
                  'asset', 'tiara', 'crept', 'bayou', 'atoll', 'manor', 'creak', 'showy', 'phase', 'froth', 'depth',
                  'gloom', 'flood', 'trait', 'girth', 'piety', 'goose', 'float', 'donor', 'atone', 'primo', 'apron',
                  'blown', 'loser', 'input', 'gloat', 'awful', 'brink', 'smite', 'beady', 'rusty', 'retro', 'droll',
                  'gawky', 'hutch', 'pinto', 'egret', 'sever', 'field', 'fluff', 'agape', 'voice', 'stead', 'berth',
                  'night', 'bland', 'liver', 'wedge', 'roomy', 'wacky', 'flock', 'angry', 'trite', 'aphid', 'tryst',
                  'midge', 'power', 'elope', 'cinch', 'motto', 'stomp', 'upset', 'bluff', 'cramp', 'coyly', 'youth',
                  'rhyme', 'buggy', 'alien', 'smear', 'unfit', 'patty', 'cling', 'glean', 'label', 'hunky', 'khaki',
                  'poker', 'gruel', 'twice', 'twang', 'shrug', 'treat', 'waste', 'merit', 'woven', 'needy', 'clown',
                  'irony', 'ruder', 'gauze', 'chief', 'onset', 'prize', 'fungi', 'charm', 'gully', 'inter', 'whoop',
                  'taunt', 'leery', 'theme', 'lofty', 'booze', 'alpha', 'thyme', 'doubt', 'parer', 'chute', 'trice',
                  'alike', 'recap', 'saint', 'glory', 'grate', 'brisk', 'soggy', 'scorn', 'leave', 'twine', 'sting',
                  'bough', 'marsh', 'sloth', 'dandy', 'howdy', 'enjoy', 'ionic', 'equal', 'floor', 'catch', 'spade',
                  'stein', 'exist', 'denim', 'grove', 'spiel', 'mummy', 'fault', 'foggy', 'flout', 'carry', 'sneak',
                  'libel', 'waltz', 'aptly', 'piney', 'inept', 'aloud', 'photo', 'dream', 'stale', 'unite', 'snarl',
                  'baker', 'there', 'glyph', 'pooch', 'hippy', 'spell', 'folly', 'louse', 'gulch', 'godly', 'threw',
                  'fleet', 'grave', 'inane', 'shock', 'crave', 'spite', 'valve', 'rainy', 'pique', 'daddy', 'arise',
                  'aging', 'valet', 'avert', 'recut', 'mulch', 'genre', 'plume', 'rifle', 'count', 'incur', 'total',
                  'wrest', 'mocha', 'deter', 'study', 'lover', 'safer', 'rivet', 'smoke', 'mound', 'undue', 'sedan',
                  'swine', 'guile', 'equip', 'tough', 'canoe', 'chaos', 'covet', 'udder', 'lunch', 'stray', 'melee',
                  'lefty', 'paste', 'octet', 'risen', 'groan', 'leaky', 'grind', 'carve', 'loose', 'sadly', 'apple',
                  'honey', 'final', 'minty', 'derby', 'wharf', 'spelt', 'coach', 'erupt', 'price', 'spawn', 'fairy',
                  'jiffy', 'filmy', 'chose', 'sleep', 'ardor', 'nanny', 'woozy', 'handy', 'grace', 'stank', 'cream',
                  'diode', 'angle', 'ninja', 'muddy', 'reply', 'prone', 'spoil', 'heart', 'shade', 'diner', 'arson',
                  'onion', 'sleet', 'dowel', 'couch', 'palsy', 'bowel', 'smile', 'evoke', 'lance', 'eagle', 'siren',
                  'embed', 'award', 'dross', 'annul', 'goody', 'frown', 'laden', 'humid', 'elite', 'lymph', 'edify',
                  'reset', 'purse', 'crock', 'write', 'loath', 'chaff', 'slide', 'venom', 'sorry', 'acorn', 'aping',
                  'tamer', 'hater', 'mania', 'awoke', 'brawn', 'swift', 'exile', 'birch', 'lucky', 'risky', 'ghost',
                  'plier', 'lunar', 'winch', 'snare', 'nurse', 'house', 'borax', 'nicer', 'lurch', 'exalt', 'about',
                  'savvy', 'toxin', 'tunic', 'pried', 'inlay', 'lanky', 'eater', 'elude', 'cycle', 'kitty', 'boule',
                  'moron', 'place', 'lobby', 'plush', 'index', 'blink', 'clung', 'croup', 'clink', 'juicy', 'nerve',
                  'flier', 'shaft', 'crook', 'clean', 'china', 'ridge', 'vowel', 'gnome', 'spiny', 'snail', 'flown',
                  'prose', 'thank', 'fiber', 'moldy', 'kneel', 'track', 'caddy', 'quell', 'paler', 'swore', 'rebar',
                  'flyer', 'horny', 'mason', 'doing', 'amply', 'molar', 'ovary', 'cliff', 'truce', 'sport', 'fritz',
                  'edict', 'twirl', 'range', 'whisk', 'hovel', 'rehab', 'spout', 'sushi', 'dying', 'fetid', 'brain',
                  'scion', 'candy', 'chord', 'basin', 'march', 'crowd', 'arbor', 'gayly', 'stain', 'dally', 'bless',
                  'bravo', 'title', 'ruler', 'kiosk', 'blond', 'ennui', 'layer', 'fluid', 'score', 'cutie', 'zebra',
                  'barge', 'bluer', 'aider', 'shook', 'privy', 'betel', 'frisk', 'begun', 'azure', 'sound', 'glove',
                  'braid', 'wryly', 'rover', 'bloom', 'irate', 'later', 'woken', 'silky', 'wreck', 'dwelt', 'slate',
                  'solid', 'hazel', 'wrist', 'jolly', 'globe', 'flint', 'rouse', 'relax', 'cover', 'alive', 'beech',
                  'vocal', 'often', 'dolly', 'joker', 'diver', 'poser', 'worst', 'alley', 'creed', 'anime', 'leafy',
                  'dunce', 'stare', 'waive', 'choir', 'spoke', 'delay', 'bilge', 'ideal', 'seize', 'hotly', 'laugh',
                  'block', 'grape', 'hardy', 'shied', 'drawl', 'daisy', 'strut', 'burnt', 'idyll', 'furor', 'cough',
                  'naive', 'shoal', 'stork', 'bathe', 'prime', 'brass', 'outer', 'furry', 'elect', 'evict', 'imply',
                  'demur', 'quota', 'swear', 'crump', 'dough', 'gavel', 'salon', 'nudge', 'harem', 'pitch', 'sworn',
                  'excel', 'cabin', 'unzip', 'trout', 'polyp', 'earth', 'storm', 'until', 'taper', 'enter', 'child',
                  'minor', 'fatty', 'brave', 'filet', 'slime', 'glint', 'tread', 'steal', 'regal', 'murky', 'share',
                  'spore', 'hoist', 'inner', 'otter', 'level', 'donut', 'arena', 'scrub', 'fancy', 'slimy', 'pearl',
                  'silly', 'porch', 'dingo', 'sepia', 'amble', 'shady', 'bread', 'friar', 'reign', 'dairy', 'cross',
                  'brood', 'tuber', 'shear', 'posit', 'blank', 'freak', 'fecal', 'shell', 'would', 'algae', 'large',
                  'bushy', 'copse', 'knife', 'pouch', 'plane', 'crown', 'urban', 'snide', 'relay', 'abide', 'viola',
                  'rajah', 'straw', 'crash', 'third', 'trick', 'grief', 'beach', 'comic', 'clued', 'caste', 'graze',
                  'frock', 'lurid', 'buyer', 'utile', 'smell', 'trade', 'modal', 'enact', 'adorn', 'roast', 'grunt',
                  'party', 'touch', 'mafia', 'crest', 'cyber', 'adore', 'tardy', 'swami', 'notch', 'hitch', 'align',
                  'strap', 'puree', 'swarm', 'diary', 'dryly', 'drank', 'acrid', 'heady', 'shalt', 'piano', 'lodge',
                  'suing', 'coral', 'ramen', 'worth', 'infer', 'overt', 'mayor', 'glide', 'randy', 'prank', 'ether',
                  'drove', 'idler', 'swath', 'apply', 'slang', 'tarot', 'credo', 'canon', 'timer', 'three', 'blunt',
                  'fluke', 'boxer', 'lunge', 'short', 'flirt', 'conch', 'agile', 'arose', 'broil', 'along', 'snaky',
                  'tramp', 'spurn', 'medal', 'flank', 'learn', 'nadir', 'remit', 'cause', 'stern', 'rocky', 'spire',
                  'grope', 'truly', 'uncle', 'preen', 'lemur', 'curly', 'dirge', 'horde', 'drool', 'crypt', 'stock',
                  'locus', 'wider', 'deign', 'logic', 'renal', 'brief', 'mouse', 'fiery', 'trunk', 'koala', 'super',
                  'grill', 'owner', 'smock', 'shaky', 'faint', 'haunt', 'chair', 'burly', 'stoic', 'jerky', 'lyric',
                  'brash', 'saucy', 'honor', 'route', 'sharp', 'trial', 'brick', 'shark', 'drier', 'chalk', 'cruel',
                  'nerdy', 'syrup', 'afire', 'shirt', 'grout', 'torch', 'again', 'bride', 'scaly', 'canal', 'prism',
                  'orbit', 'dance', 'paint', 'liner', 'cloak', 'navel', 'clash', 'crisp', 'leant', 'maker', 'broke']

    i = 0
    p = Pool(2)
    # print(active_children())
    # p2 = Pool(2)
    # p.terminate()
    # print(active_children())
    memory.clear(warn=False)
    for wordle in solutions:
        i += 1
        toRemove = []

        for j, guess in enumerate(dictionary):
            print(j, guess)
            if guess == wordle:
                continue

            possible2 = filterPoss(possible, guess, getPattern(guess, wordle))
            start = dictionary2.index(guess) + 1

            noBranches = True
            for result in p.imap_unordered(func, iterable(start, dictionary2, wordle, possible2), chunksize=3):
                if result:
                    noBranches = False
                    break

            if noBranches:
                toRemove.append(guess)

        for word in toRemove:
            dictionary.remove(word)
        memory.clear(warn=False)

        print(dictionary, len(dictionary), wordle, i)
        if len(dictionary) == 0:
            break

    p.close()


if __name__ == "__main__":
    main()
