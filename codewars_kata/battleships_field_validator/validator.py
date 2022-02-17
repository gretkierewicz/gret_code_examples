from typing import Dict, List, Tuple


def check_if_solved(count_dict: Dict[int, int]) -> bool:
    for i in range(1, 5):
        if count_dict[i] != 5 - i:
            return False
    return True


def validate_battlefield(field: List[List[int]]):
    def check_field(*args: int) -> int:
        for arg in args[:2]:
            if arg > 9 or arg < 0:
                return 0
        return field[args[0]][args[1]]

    ships_count = {4: 0, 3: 0, 2: 0, 1: 0}
    checked_ship_fields: List[Tuple[int, int]] = []

    row = 0
    col = -1

    while True:
        # check for wrong number of ships
        for i in range(1, 5):
            if ships_count[i] > 5 - i:
                return False

        # increment checked field
        if col < 9:
            col += 1
        elif row < 9:
            row += 1
            col = 0
        else:
            return check_if_solved(ships_count)

        # if field already checked or empty - nothing to check
        if (row, col) in checked_ship_fields or not field[row][col]:
            continue

        checked_ship_fields.append((row, col))

        direction = [0, 0]
        """direction of ship search: row_inc, col_inc"""

        direction[1] = check_field(row, col + 1)
        direction[0] = check_field(row + 1, col)

        # check for wrong ship shape
        if all(direction):
            return False

        # this field is not checked anywhere else
        if check_field(row + 1, col - 1):
            return False

        # one field ship
        if not any(direction):
            ships_count[1] += 1
            if check_field(row + 1, col + 1):
                return False
            continue

        # 2+ fields ship, searching loop
        for x in range(1, 6):
            next_field_coords = row + x * direction[0], col + x * direction[1]

            # check surroundings rectangular to ship's direction
            if check_field(
                next_field_coords[0] + direction[1], next_field_coords[1] + direction[0]
            ):
                return False

            # found next field in ship's direction - proceed search
            if check_field(*next_field_coords):
                # ship too long
                if x == 4:
                    return False
                checked_ship_fields.append(next_field_coords)
                continue

            # end of the ship
            ships_count[x] += 1
            break

    return check_if_solved(ships_count)
