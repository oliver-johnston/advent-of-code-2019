def is_match(password, min_adjacent, max_adjacent):
    prev = '0'
    count_adjacent = dict()

    for cur in password:
        if cur < prev:
            return False
        elif cur == prev:
            count_adjacent[cur] += 1
        else:
            count_adjacent[cur] = 1
        prev = cur

    return any(map(lambda x: min_adjacent <= x <= max_adjacent, count_adjacent.values()))


print(sum(1 for p in range(125730, 579381) if is_match(str(p), 2, 999)))
print(sum(1 for p in range(125730, 579381) if is_match(str(p), 2, 2)))
