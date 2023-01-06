#%%
from pathlib import Path
from dataclasses import dataclass, field

DATA_PATH = Path("19/data/")

with (DATA_PATH / "input.txt").open() as infile:
    data = infile.read()
    data = data.split("\n")

blueprints = []
for row in data:
    blueprint = {}
    _, ore, clay, obsidian, geode = row.split("Each")

    blueprint["ore"] = {"ore": int(ore.split()[-2])}
    blueprint["clay"] = {"ore": int(clay.split()[-2])}
    blueprint["obsidian"] = {
        "ore": int(obsidian.split()[-5]),
        "clay": int(obsidian.split()[-2]),
    }
    blueprint["geode"] = {
        "ore": int(geode.split()[-5]),
        "obsidian": int(geode.split()[-2]),
    }

    blueprints.append(blueprint)

blueprints[0]
#%%


def create_robots():
    return {
        "ore": {"quantity": 1, "ressources": 0},
        "clay": {"quantity": 0, "ressources": 0},
        "obsidian": {"quantity": 0, "ressources": 0},
        "geode": {"quantity": 0, "ressources": 0},
    }


#%%
# main loop
from uuid import uuid4, UUID


@dataclass
class State:
    robots: dict
    timestep: int
    next_robot: str
    first_geode: int = 0
    id: UUID = field(default_factory=uuid4)

    def build_robot(self, blueprint):
        if all(
            [
                self.robots[ressource]["ressources"] >= quantity
                for ressource, quantity in blueprint[self.next_robot].items()
            ]
        ):
            for ressource, quantity in blueprint[self.next_robot].items():
                self.robots[ressource]["ressources"] -= quantity
            return True
        return False

    def add_robot(self):
        self.robots[self.next_robot]["quantity"] += 1


possible_robot_choice = [
    ["ore", "clay"],
    ["ore", "clay", "obsidian"],
    ["ore", "clay", "obsidian", "geode"],
]

solution = []
max_timesteps = 32
for blueprint_id in range(len(blueprints[:3])):

    blueprint = blueprints[blueprint_id]
    print(f"starting blueprint {blueprint_id}")
    best_state = State(robots=create_robots(), timestep=0, next_robot="ore")

    queue = [
        State(robots=create_robots(), timestep=0, next_robot="ore"),
        State(robots=create_robots(), timestep=0, next_robot="clay"),
    ]

    i = 0
    while queue:
        i += 1
        if i % 1000000 == 0:
            n_geodes = best_state.robots["geode"]["ressources"]
            print(f"iteration {i} - score: {n_geodes} - queue lenght {len(queue)}")

        state = queue.pop()
        state.timestep += 1

        # build robots
        built_robot = state.build_robot(blueprint)
        if built_robot and state.next_robot == "geode":
            if state.robots["geode"]["quantity"] == 0:
                state.first_geode = state.timestep

        # gather ressources
        for robot in state.robots.values():
            robot["ressources"] += robot["quantity"]

        # check if better
        if (
            state.robots["geode"]["ressources"]
            > best_state.robots["geode"]["ressources"]
        ):
            best_state = state

        # send back to queue
        remaining_time = max_timesteps - state.timestep
        if remaining_time == 0:
            continue

        upper_bound = (
            state.robots["geode"]["ressources"]
            + (remaining_time) * state.robots["geode"]["quantity"]
            + sum(range(1, remaining_time + 1))
        )

        if upper_bound > best_state.robots["geode"]["ressources"]:
            # add new robots
            if built_robot:

                state.add_robot()

                # select new robot to buy:
                if state.robots["obsidian"]["quantity"] > 0:
                    possible_robots = possible_robot_choice[2]
                elif state.robots["clay"]["quantity"] > 0:
                    possible_robots = possible_robot_choice[1]
                else:
                    possible_robots = possible_robot_choice[0]

                for next_robot in possible_robots:

                    robots = {}
                    for robot in state.robots:
                        robots[robot] = {}
                        robots[robot]["quantity"] = state.robots[robot]["quantity"]
                        robots[robot]["ressources"] = state.robots[robot]["ressources"]

                    new_state = State(
                        robots=robots,
                        timestep=state.timestep,
                        next_robot=next_robot,
                    )
                    queue.append(new_state)
            else:
                queue.append(state)

    max_geodes = best_state.robots["geode"]["ressources"]
    print(f"number of geodes = {max_geodes}")
    # print(f"quality level of blueprint {(blueprint_id+1) * max_geodes}")
    # solution.append((blueprint_id + 1) * max_geodes)
    solution.append(max_geodes)

#%%

sum(solution[0] * solution[1] * solution[2])

#%%
