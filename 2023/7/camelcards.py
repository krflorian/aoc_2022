# %%

from pathlib import Path

with Path("data.txt").open() as infile:
    data = infile.read()
    data = data.split("\n")
hands = [hand.split() for hand in data]
hands

# %%
from collections import defaultdict

scores = ["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"]


def is_five_of_a_kind(hand):
    return len(set(hand)) == 1


def is_four_of_a_kind(hand):
    counter = defaultdict(int)
    for val in hand:
        counter[val] += 1
    return any([val == 4 for val in counter.values()])


def is_fullhouse(hand):
    counter = defaultdict(int)
    for val in hand:
        counter[val] += 1
    three = sum([val == 3 for val in counter.values()]) == 1
    two = sum([val == 2 for val in counter.values()]) == 1
    return three and two


def is_three_of_a_kind(hand):
    counter = defaultdict(int)
    for val in hand:
        counter[val] += 1
    return sum([val == 3 for val in counter.values()]) == 1


def is_two_pair(hand):
    counter = defaultdict(int)
    for val in hand:
        counter[val] += 1
    return sum([val == 2 for val in counter.values()]) == 2


def is_pair(hand):
    counter = defaultdict(int)
    for val in hand:
        counter[val] += 1
    return sum([val == 2 for val in counter.values()]) == 1


def is_high_card(hand):
    return len(set(hand)) == 5


hands_analyzed = []
for hand, value in hands:
    if is_five_of_a_kind(hand):
        hands_analyzed.append((hand, value, 0))
    elif is_four_of_a_kind(hand):
        hands_analyzed.append((hand, value, 1))
    elif is_fullhouse(hand):
        hands_analyzed.append((hand, value, 2))
    elif is_three_of_a_kind(hand):
        hands_analyzed.append((hand, value, 3))
    elif is_two_pair(hand):
        hands_analyzed.append((hand, value, 4))
    elif is_pair(hand):
        hands_analyzed.append((hand, value, 5))
    elif is_high_card(hand):
        hands_analyzed.append((hand, value, 6))
    else:
        print("attention! ", hand)


# %%
# order


def sort_key(hand):
    return (
        -hand[2],
        -scores.index(hand[0][0]),
        -scores.index(hand[0][1]),
        -scores.index(hand[0][2]),
        -scores.index(hand[0][3]),
        -scores.index(hand[0][4]),
    )


hands_analyzed = sorted(hands_analyzed, key=lambda x: sort_key(x))

# %%
total_score = 0
for i, hand in enumerate(hands_analyzed):
    total_score += (i + 1) * int(hand[1])

total_score


# %%
# part 2

scores = ["A", "K", "Q", "T", "9", "8", "7", "6", "5", "4", "3", "2", "J"]


hands_analyzed = []
for hand, value in hands:
    if hand == "JJJJJ":
        evaluate_hand = hand
    elif "J" in hand:
        counter = defaultdict(int)
        for val in hand:
            counter[val] += 1
        replace_key = sorted(
            [(key, val) for key, val in counter.items() if key != "J"],
            key=lambda x: -x[1],
        )[0][0]
        evaluate_hand = hand.replace("J", replace_key)
    else:
        evaluate_hand = hand

    if is_five_of_a_kind(evaluate_hand):
        hands_analyzed.append((hand, value, 0, evaluate_hand))
    elif is_four_of_a_kind(evaluate_hand):
        hands_analyzed.append((hand, value, 1, evaluate_hand))
    elif is_fullhouse(evaluate_hand):
        hands_analyzed.append((hand, value, 2, evaluate_hand))
    elif is_three_of_a_kind(evaluate_hand):
        hands_analyzed.append((hand, value, 3, evaluate_hand))
    elif is_two_pair(evaluate_hand):
        hands_analyzed.append((hand, value, 4, evaluate_hand))
    elif is_pair(evaluate_hand):
        hands_analyzed.append((hand, value, 5, evaluate_hand))
    elif is_high_card(evaluate_hand):
        hands_analyzed.append((hand, value, 6, evaluate_hand))
    else:
        print("attention! ", hand)


hands_analyzed

# %%

hands_analyzed = sorted(hands_analyzed, key=lambda x: sort_key(x))
hands_analyzed
# %%

total_score = 0
for i, hand in enumerate(hands_analyzed):
    total_score += (i + 1) * int(hand[1])

total_score
