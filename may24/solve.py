import math
import copy
from functools import partial
from sympy import primerange, fibonacci

connected_component = [
    [0, 0, 0, 1, 1, 1, 2, 2, 3, 3, 3],
    [0, 4, 4, 4, 1, 1, 2, 3, 3, 3, 5],
    [0, 4, 4, 1, 1, 1, 2, 3, 3, 3, 5],
    [0, 4, 4, 1, 1, 6, 6, 3, 5, 5, 5],
    [0, 4, 1, 1, 3, 3, 6, 3, 5, 7, 5],
    [0, 3, 3, 3, 3, 3, 3, 3, 7, 7, 8],
    [9, 3, 3, 3, 3, 10, 10, 3, 7, 7, 7],
    [9, 9, 11, 3, 11, 10, 10, 3, 3, 7, 3],
    [9, 9, 11, 11, 11, 10, 10, 3, 3, 3, 3],
    [9, 11, 11, 9, 9, 9, 10, 3, 3, 3, 12],
    [9, 9, 9, 9, 9, 10, 10, 10, 3, 3, 12],
]


def generate_fibo(max_n):
    fibo.append(1)
    fibo.append(1)
    i = 2
    while len(fibo) < max_n:
        next_fibo = fibo[i - 1] + fibo[i - 2]
        fibo.append(next_fibo)
        i += 1


def str_to_num(s):
    return int(s.replace("#", ""))


def check_square(x):
    sr = math.sqrt(x)
    return (int)(sr) ** 2 == x


def check_palindrome(x, k):
    x -= k
    return str(x) == str(x)[::-1]


def _is_power_of_prime(x, p):
    if x % p != 0:
        return False

    cnt = 0
    y = x
    while y % p == 0:
        y //= p
        cnt += 1

    return y == 1 and cnt in primes


def check_pow_prime(x):
    for p in primes:
        if _is_power_of_prime(x, p):
            return True

    return False


def check_sum_of_digits(x, k):
    return sum([int(i) for i in str(x)]) == k


def check_fibo(x):
    return x in fibonacci_numbers


def check_multiple_of(x, k):
    return x % k == 0


def check_palin_and_multiple_of(x, k):
    return check_palindrome(x, 0) and check_multiple_of(x, k)


def check_product_digits(x, k):
    return math.prod([int(i) for i in str(x)]) % 10 == k


symbols = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]
ans = [["#"] * 11 for i in range(11)]
fibonacci_numbers = [fibonacci(i) for i in range(1, 51)]
primes = list(primerange(2, 1000))


def print_ans():
    sum_ans = 0
    numbers = []
    for i, row in enumerate(ans):
        s = " ".join(row)
        t = " ".join([f"{x:2}" for x in connected_component[i]])
        print(s, " / ", t)

        row_numbers = "".join(row).split("#")
        sum_ans += sum([str_to_num(x) for x in row_numbers if x != ""])
        numbers += [str_to_num(x) for x in row_numbers if x != ""]

    print("Sum of all numbers formed in the completed grid:", sum_ans)
    print("Numbers formed in the completed grid:", numbers)


checkers = [
    check_square,
    partial(check_palindrome, k=1),
    check_pow_prime,
    partial(check_sum_of_digits, k=7),
    check_fibo,
    check_square,
    partial(check_multiple_of, k=37),
    partial(check_palin_and_multiple_of, k=23),
    partial(check_product_digits, k=1),
    partial(check_multiple_of, k=88),
    partial(check_palindrome, k=-1),
]

def check_orthogonal_diff(x, y, s):
    if (
        x > 0
        and y > 0
        and connected_component[x][y] != connected_component[x - 1][y - 1]
        and s == ans[x - 1][y - 1]
    ):
        return False

    if (
        x > 0
        and y + 1 < 11
        and connected_component[x][y] != connected_component[x - 1][y + 1]
        and s == ans[x - 1][y + 1]
    ):
        return False

    return True


# Numbers must be at least two digits long and may not begin with a 0
def check_valid_num(row, s):
    return (len(s) >= 2 and s[0] != "0" and checkers[row](str_to_num(s))) or s == ""


def solve(x, y, cur_num):
    """
    The 11-by-11 grid above has been divided into various regions.
    Shade some of the cells black, then place digits (0-9) into the remaining cells.
    Shading must be “sparse”: that is, no two shaded cells may share an edge.

    Every cell within a region must contain the same digit, and orthogonally adjacent cells in different regions must have different digits.
    (Note that shading cells may break up regions or change which pairs of regions are adjacent. See the example, below.)

    Each row has been supplied with a clue.
    Every number formed by concatenating consecutive groups of unshaded cells within a row must satisfy the clue given for the row. (As in the example.)
    Numbers must be at least two digits long and may not begin with a 0.
    The answer to this month’s puzzle is the sum of all the numbers formed in the completed grid. (As in the example.)
    """

    if y == 11:
        if check_valid_num(x, cur_num):
            if x == 10:
                print_ans()
                exit()

            solve(x + 1, 0, "")

        return

    # Case 1: Fill in '#'
    if y == 0 and (x == 0 or (x > 0 and ans[x - 1][y] != "#")):
        solve(x, y + 1, "")

    if ((x > 0 and ans[x - 1][y] != "#") or x == 0) and (
        y > 0 and ans[x][y - 1] != "#"
    ):
        if check_valid_num(x, cur_num):
            solve(x, y + 1, "")

    # Case 2: Fill in the same symbol as the left or top cell if connected, else try all symbols
    candidate_symbol = "#"
    if (
        y > 0
        and connected_component[x][y] == connected_component[x][y - 1]
        and ans[x][y - 1] != "#"
    ):
        candidate_symbol = ans[x][y - 1]
    elif (
        x > 0
        and connected_component[x][y] == connected_component[x - 1][y]
        and ans[x - 1][y] != "#"
    ):
        candidate_symbol = ans[x - 1][y]

    if candidate_symbol != "#":
        ok_left = True
        if (
            y > 0
            and connected_component[x][y] == connected_component[x][y - 1]
            and ans[x][y - 1] != "#"
        ):
            ok_left = candidate_symbol == ans[x][y - 1]

        ok_top = True
        if (
            x > 0
            and connected_component[x][y] == connected_component[x - 1][y]
            and ans[x - 1][y] != "#"
        ):
            ok_top = candidate_symbol == ans[x - 1][y]

        if ok_left and ok_top and check_orthogonal_diff(x, y, candidate_symbol):
            ans[x][y] = candidate_symbol
            solve(x, y + 1, cur_num + candidate_symbol)
            ans[x][y] = "#"

    else:
        for s in symbols:
            # The first digit cannot be 0
            if cur_num == "" and s == "0":
                continue

            if check_orthogonal_diff(x, y, s):
                ans[x][y] = s
                solve(x, y + 1, cur_num + s)
                ans[x][y] = "#"


if __name__ == "__main__":
    solve(0, 0, "")

""" Answer:
1 1 1 2 2 2 3 3 4 4 4  /   0  0  0  1  1  1  2  2  3  3  3
1 3 3 3 2 # 3 4 4 4 #  /   0  4  4  4  1  1  2  3  3  3  5
1 3 3 1 # 7 3 4 4 4 9  /   0  4  4  1  1  1  2  3  3  3  5
1 3 3 # 1 0 0 4 1 1 #  /   0  4  4  1  1  6  6  3  5  5  5
1 3 # 1 4 4 # 4 1 8 1  /   0  4  1  1  3  3  6  3  5  7  5
1 4 4 4 # 4 4 4 8 8 9  /   0  3  3  3  3  3  3  3  7  7  8
7 4 4 4 4 # 7 4 8 8 8  /   9  3  3  3  3 10 10  3  7  7  7
7 7 1 4 1 7 7 # 9 8 9  /   9  9 11  3 11 10 10  3  3  7  3
7 7 1 1 1 7 7 9 9 9 9  /   9  9 11 11 11 10 10  3  3  3  3
# 1 1 4 4 # 7 9 9 9 2  /   9 11 11  9  9  9 10  3  3  3 12
4 4 4 4 4 3 # 3 9 9 2  /   9  9  9  9  9 10 10 10  3  3 12
Sum of all numbers formed in the completed grid: 88243711283
Numbers formed in the completed grid: 
[11122233444, 13332, 3444, 1331, 734449, 133, 100411, 13, 144, 4181, 1444, 444889, 74444, 74888, 7714177, 989, 77111779999, 1144, 79992, 444443, 3992]
"""
