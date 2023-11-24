#%%
from pathlib import Path

DATA_PATH = Path("data/")

with (DATA_PATH / "input.txt").open() as infile:
    data = infile.read()
    data = data.split("\n")
    data = list(map(int, data))


decryption_key = 811589153
data = [num * decryption_key for num in data]

#%%


def shift(idx, num):

    if num == 0:
        pass

    enc_idx = encrypted.index((idx, num))
    enc = encrypted.pop(enc_idx)

    new_idx = enc_idx + num
    if (new_idx > len(encrypted)) or (new_idx <= 0):
        new_idx = new_idx % len(encrypted)
    else:
        new_idx = enc_idx + num

    encrypted.insert(new_idx, enc)


#%%

encrypted = [(idx, num) for idx, num in enumerate(data)]

for _ in range(10):
    for idx, num in enumerate(data):
        shift(idx, num)


#%%

solution = []
i = 0
while True:
    i += 1
    enc = encrypted.pop(0)
    encrypted.append(enc)
    if enc[1] == 0:
        print("index of zero: ", i)
        break

#%%

coordinates = []
for i in range(0, 3001):
    enc = encrypted.pop(0)
    encrypted.append(enc)
    if i in [999, 1999, 2999]:
        coordinates.append(enc[1])

#%%

print(coordinates)
print(sum(coordinates))

#%%
