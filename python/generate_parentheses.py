"""Generate all well-formed parentheses combinations."""


def generate_parentheses(n):
    """Return all combinations of ``n`` pairs of well-formed parentheses.

    The function uses backtracking and only adds a closing parenthesis when
    doing so cannot make the partial combination invalid.

    Args:
        n: Number of pairs of parentheses to generate.

    Returns:
        A list of well-formed parentheses strings.

    Raises:
        ValueError: If ``n`` is negative.
    """
    if n < 0:
        raise ValueError("n must be non-negative")

    result = []

    def backtrack(current, open_count, close_count):
        if len(current) == 2 * n:
            result.append("".join(current))
            return

        if open_count < n:
            current.append("(")
            backtrack(current, open_count + 1, close_count)
            current.pop()

        if close_count < open_count:
            current.append(")")
            backtrack(current, open_count, close_count + 1)
            current.pop()

    backtrack([], 0, 0)
    return result


if __name__ == "__main__":
    print(generate_parentheses(3))
