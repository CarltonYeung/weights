#!/usr/bin/python3
import argparse
import itertools
import math

from pprint import pprint


BARBELL_IN_LBS = 45
LB_PER_KG = 2.205


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


def make_total_weight_map(weight_pairs, weight_in_lbs):
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

    cols = max([len(combos) for combos in weight_map.values()])
    for total_weight in sorted(weight_map.keys()):
        if not weight_in_lbs or (total_weight in weight_in_lbs):
            formatting = '{:<10}' + '{:<30}'*cols + '{:<10}'

            combos = [str(combo) for combo in weight_map[total_weight]]
            combos = (combos + ['']*cols)[:cols]
            print(formatting.format(total_weight, *combos, math.floor(total_weight / LB_PER_KG)))
            print()

    return weight_map


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('weight_in_lbs', nargs='*', default=None, type=int)
    args = parser.parse_args()
    return args


def main():
    args = parse_args()
    weight_pairs = [2.5, 5, 10, 10, 25, 35, 45]

    weight_map = make_total_weight_map(weight_pairs, args.weight_in_lbs)

    verify(weight_map)
    verify_jumps_by(sorted(list(weight_map.keys())), 5)


if __name__ == '__main__':
    main()

