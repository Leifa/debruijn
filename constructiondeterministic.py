def is_construction_deterministic(pattern):
    sets = {frozenset({node}) for node in pattern.nodes}
    change = True
    while change:
        change = False

        # Calculate new sets
        sets_to_add = set()
        for set1 in sets:
            for set2 in sets:
                set1_green_succ = pattern.get_green_successors_of_set(set1)
                set2_red_succ = pattern.get_red_successors_of_set(set2)
                intersection = set1_green_succ.intersection(set2_red_succ)
                is_new = True
                for set3 in sets:
                    if intersection.issubset(set3):
                        is_new = False
                        break
                if is_new:
                    sets_to_add.add(frozenset(intersection))

        # Add new sets
        for new_set in sets_to_add:
            change = True
            sets.add(new_set)

        # Remove subsets
        sets_to_remove = set()
        for set1 in sets:
            for set2 in sets:
                if set1 != set2 and set1.issubset(set2):
                    sets_to_remove.add(set1)
        for set_to_remove in sets_to_remove:
            sets.remove(set_to_remove)

    print(sets)
    set_of_all_nodes = set(pattern.nodes)
    return set_of_all_nodes not in sets

