def validate_guess(guess: str, target: str) -> list[dict]:
    guess = guess.upper()
    target = target.upper()
    n = len(target)
    result = [{"letter": guess[i], "status": "absent"} for i in range(n)]
    target_counts = {}

    # First pass: correct (green)
    for i in range(n):
        if guess[i] == target[i]:
            result[i]["status"] = "correct"
        else:
            target_counts[target[i]] = target_counts.get(target[i], 0) + 1

    # Second pass: present (yellow)
    for i in range(n):
        if result[i]["status"] == "correct":
            continue
        letter = guess[i]
        if target_counts.get(letter, 0) > 0:
            result[i]["status"] = "present"
            target_counts[letter] -= 1

    return result
