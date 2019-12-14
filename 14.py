import math


class Chemical:
    def __init__(self, symbol, quantity):
        self.symbol = symbol
        self.quantity = quantity


class Reaction:
    def __init__(self, input_chemicals, output_chemical):
        self.input_chemicals = input_chemicals
        self.output_chemical = output_chemical


def parse_chemical(text):
    split = text.split(" ")
    return Chemical(split[1], int(split[0]))


def parse_reactions(data):
    for line in data:
        split = line.split(" => ")
        input_chemicals = list(map(parse_chemical, split[0].split(", ")))
        output_chemical = parse_chemical(split[1])
        yield Reaction(input_chemicals, output_chemical)


def get_ore(quantity, symbol, reactions, surplus):
    if symbol == "ORE":
        return quantity

    if symbol in surplus:
        use_surplus = min(quantity, surplus[symbol])
        quantity -= use_surplus
        surplus[symbol] -= use_surplus

    if quantity == 0:
        return 0

    reaction = reactions[symbol]
    num_reactions = math.ceil(quantity / reaction.output_chemical.quantity)

    ore = 0

    for i in reaction.input_chemicals:
        ore += get_ore(i.quantity * num_reactions, i.symbol, reactions, surplus)

    s = num_reactions * reaction.output_chemical.quantity - quantity
    surplus[symbol] = surplus.get(symbol, 0) + s

    return ore



fp = open("14.txt")
data = fp.read().splitlines()
reactions = parse_reactions(data)

reaction_dict = dict()
for r in reactions:
    reaction_dict[r.output_chemical.symbol] = r

fuel = get_ore(1, "FUEL", reaction_dict, dict())

print(fuel)
