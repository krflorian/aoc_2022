# %%
from pathlib import Path

with Path("data.txt").open() as infile:
    data = infile.read()
    data = data.split("\n")

data = [row.split(":")[1].split("|") for row in data]


winning, cards = [], []
for win, card in data:
    win = win.split(" ")
    winning.append(set([num for num in win if num != ""]))
    card = card.split(" ")
    cards.append(set([num for num in card if num != ""]))


# %%
# part 1
point_list = [0, 1, 2, 4, 8, 16, 32, 64, 128, 128 * 2, 128 * 2 * 2, 128 * 2 * 2 * 2]

points = 0
for win, card in zip(winning, cards):
    winning_numbers = win.intersection(card)
    points += point_list[len(list(winning_numbers))]

points

# %%
# part 2

scratch_cards = {idx: 1 for idx in range(len(cards))}
for idx, (win, card) in enumerate(zip(winning, cards)):
    winning_numbers = win.intersection(card)
    for i in range(1, len(list(winning_numbers)) + 1):
        scratch_cards[idx + i] += scratch_cards[idx]
scratch_cards

# %%

all_cards = 0
for kex, val in scratch_cards.items():
    all_cards += val

all_cards

# %%
