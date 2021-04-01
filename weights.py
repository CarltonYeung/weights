#!/usr/bin/python3
from pprint import pprint
import itertools

BARBELL_IN_LBS = 45


def calculate_total_weight(weight_per_side):
    weight = sum(weight_per_side) * 2 + BARBELL_IN_LBS
    if int(weight) == weight:
        weight = int(weight)
    return weight


def verify(weight_map):
    for total_weight, combos in weight_map.items():
        for combo in combos:
            assert calculate_total_weight(combo) == total_weight, (combo, total_weight)


def verify_jumps_by(weights, jump):
    for i in range(len(weights) - 1):
        if not weights[i+1] <= weights[i] + jump:
            print(f'Jump is larger than desired ({jump}): {weights[i]} -> {weights[i+1]}')


def make_combinations(weight_pairs):
    combos = []
    for n_plates in range(len(weight_pairs) + 1):
        combos.extend(list(itertools.combinations(weight_pairs, n_plates)))
    
    return combos


def make_total_weight_map(weight_pairs):
    combos = make_combinations(weight_pairs)

    weight_tuples = list(map(lambda plates: (plates, sum(plates)), combos))

    weight_map = {}

    for weight_tuple in weight_tuples:
        total_weight = calculate_total_weight(weight_tuple[0])
        if isinstance(total_weight, int):
            total_weight = int(total_weight)
        if total_weight in weight_map:
            weight_map[total_weight].append(weight_tuple[0])
        else:
            weight_map[total_weight] = [weight_tuple[0]]

    for total_weight, weights in weight_map.items():
        sorted_combos = [tuple(sorted(combo, reverse=True)) for combo in weights]
        sorted_combos_by_len = sorted(sorted_combos, key=len)

        deduped_combos = []
        for combo in sorted_combos_by_len:
            if combo not in deduped_combos:
                deduped_combos.append(combo)

        weight_map[total_weight] = deduped_combos 

    for total_weight in sorted(weight_map.keys()):
        formatting = '{:<10}' + ' '.join(['{:<25}' for _ in weight_map[total_weight]])
        print(formatting.format(total_weight, *[str(combo) for combo in weight_map[total_weight]]))

    return weight_map


def main():
    weight_pairs = [10, 10, 25, 35, 45]
    #weight_pairs = [1.25, 2.5, 5, 10, 10, 25, 35, 45]

    weight_map = make_total_weight_map(weight_pairs)

    verify(weight_map)
    verify_jumps_by(sorted(list(weight_map.keys())), 5)


if __name__ == '__main__':
    main()

