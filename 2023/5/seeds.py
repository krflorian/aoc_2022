# %%

from pathlib import Path

with Path("data.txt").open() as infile:
    data = infile.read()
    data = data.split("\n")

map_titles = [
    "seed-to-soil map:",
    "soil-to-fertilizer map:",
    "fertilizer-to-water map:",
    "water-to-light map:",
    "light-to-temperature map:",
    "temperature-to-humidity map:",
    "humidity-to-location map:",
]

seeds = list(map(int, data[0].split()[1:]))

mappings = []
for row in data[2:]:
    if row == "":
        continue
    elif row in map_titles:
        mappings.append([])
    else:
        mappings[-1].append(list(map(int, row.split())))


# %%
# part 2

seed_ranges = []
last_idx = 0
for idx in range(2, len(seeds) + 1, 2):
    start, seed_range = seeds[last_idx:idx]
    last_idx = idx
    seed_ranges.append(range(start, start + seed_range - 1))

seed_ranges


# %%

source_ranges = []
destination_ranges = []
for mapping in mappings:
    source_ranges.append([])
    destination_ranges.append([])
    for destination_start, source_start, _range in mapping:
        destination_end = destination_start + _range - 1
        source_end = source_start + _range - 1

        destination_ranges[-1].append(range(destination_start, destination_end))
        source_ranges[-1].append(range(source_start, source_end))

source_ranges
# %%

"""
positions = seed_ranges[:]
sources = source_ranges[0]
destinations = destination_ranges[0]


positions = [range(5, 20)]
sources = [range(5, 20)]
destinations = [range(15, 30)]
"""

positions = seed_ranges[:]
for sources, destinations in zip(source_ranges, destination_ranges):
    new_positions = []
    while positions:
        position = positions.pop(0)
        added_position = False
        for source, destination in zip(sources, destinations):
            # position in range of source
            if position.start >= source.start and position.stop <= source.stop:
                print("position in source range", position, source)
                offset = position.start - source.start
                new_position = range(
                    destination.start + offset,
                    destination.start + offset + (position.stop - position.start),
                )
                new_positions.append(new_position)
                added_position = True
                break
            # position overlaps on right
            elif (
                position.start >= source.start
                and position.start <= source.stop
                and position.stop > source.stop
            ):
                print("position overlaps on right", position, source)
                offset = position.start - source.start
                new_position = range(destination.start + offset, destination.stop)
                new_positions.append(new_position)
                # TODO check for other sources
                new_position = range(source.stop + 1, position.stop)
                positions.append(new_position)
                added_position = True
                break
            # position overlaps on left
            elif (
                position.start < source.start
                and position.stop >= source.start
                and position.stop <= source.stop
            ):
                print("position overlaps on left", position, source)
                # TODO check for other sources
                new_position = range(position.start, source.start - 1)
                positions.append(new_position)

                offset = position.stop - source.start
                new_position = range(destination.start, destination.start + offset)
                new_positions.append(new_position)
                added_position = True
                break
            # source in position
            elif position.start < source.start and position.stop > source.stop:
                print("position around source", position, source)
                new_position = range(position.start, source.start - 1)
                positions.append(new_position)
                new_position = range(source.stop + 1, position.stop)
                positions.append(new_position)

                new_position = range(destination.start, destination.stop)
                new_positions.append(new_position)
                added_position = True
                break
        if not added_position:
            new_positions.append(position)

    # reset positions
    positions = new_positions[:]


# %%
# solution
sorted(positions, key=lambda x: x.start)[0].start

# %%
