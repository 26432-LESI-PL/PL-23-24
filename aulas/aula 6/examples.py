import re

# findall           ->      Returns a list containing all matches
# search            ->      Returns a Match object if there is a match anywhere in the string
# split	            ->      Returns a list where the string has been split at each match
# sub               ->      Replaces one or many matches with a string

regex : list = ["ab?c", "[+-]?[0-9]+", "ab{2,4}c", "[a-c][x-z]", "[a-cx-z]{2}", "abc[abc]"]


text : str  =   "a, b, c, ab, ac, ba, bc, ca, cb, abc, acb, bac, cab, cba " + \
                "0, 1, 2, +1, +11, -3, -33, +0.51, 074, -123.2, acx, acyyyy, azzzz, acac, acacacac, abc, abca, abcc, abcbbb"

for exp in regex:
    output_findall : list = re.findall(exp, text)
    print(f"For regex '{exp}' results are: {output_findall}")


