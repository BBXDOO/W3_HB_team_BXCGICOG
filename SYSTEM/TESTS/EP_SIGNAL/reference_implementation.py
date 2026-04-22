import re


class EPError(Exception):
    pass


VALID_HEADERS = {"0", "1", "H", "M", "C", "X"}
VALID_FORMATS = {"BIN", "HEX", "META", "CLR", "SYM", "PKG", "RAW"}


def count_ones(binary_string: str) -> int:
    return binary_string.count("1")


# -------------------------------------------------
# PAYLOAD PARSER
# รองรับ:
# 22113
# *12*
# *23'15'11'40*
# 22*12*3
# -------------------------------------------------
def parse_payload(payload: str):
    """
    return list[int]

    examples:
    22113            => [2,2,1,1,3]
    22*12*3          => [2,2,12,3]
    *23'15'11'40*    => [23,15,11,40]
    """

    runs = []
    i = 0

    while i < len(payload):
        ch = payload[i]

        # block mode
        if ch == "*":
            j = payload.find("*", i + 1)
            if j == -1:
                raise EPError("Unclosed * marker")

            content = payload[i + 1:j]

            if not content:
                raise EPError("Empty * * block")

            # multi values mode
            if "'" in content:
                parts = content.split("'")

                for p in parts:
                    if not p.isdigit():
                        raise EPError("Invalid block number")
                    runs.append(int(p))

            # single value mode
            else:
                if not content.isdigit():
                    raise EPError("Invalid number in * *")
                runs.append(int(content))

            i = j + 1

        # single digit mode
        elif ch.isdigit():
            runs.append(int(ch))
            i += 1

        else:
            raise EPError("Invalid payload character")

    return runs


# -------------------------------------------------
# RUN LENGTH
# -------------------------------------------------
def runs_from_binary(binary_string: str):
    if not binary_string:
        raise EPError("Empty binary input")

    runs = []
    current = binary_string[0]
    count = 1

    for bit in binary_string[1:]:
        if bit == current:
            count += 1
        else:
            runs.append(count)
            current = bit
            count = 1

    runs.append(count)
    return runs


# -------------------------------------------------
# ENCODE TOKEN
# -------------------------------------------------
def encode_run(n: int) -> str:
    if n <= 9:
        return str(n)
    return f"*{n}*"


def encode_runs_compact(runs):
    """
    1..9   => direct digit
    10+    => *n*
    optional block mode if all 10+
    """
    return "".join(encode_run(x) for x in runs)


# -------------------------------------------------
# ENCODER
# -------------------------------------------------
def encode(binary_string: str, fmt="BIN") -> str:
    if not re.fullmatch(r"[01]+", binary_string):
        raise EPError("Binary input must contain only 0/1")

    if fmt not in VALID_FORMATS:
        raise EPError("Unknown format")

    header = binary_string[0]
    runs = runs_from_binary(binary_string)
    payload = encode_runs_compact(runs)
    verify = count_ones(binary_string)

    return f"{header}/{payload}-{verify}'{fmt}"


# -------------------------------------------------
# PARSE FULL EP
# -------------------------------------------------
def parse_ep(ep_string: str):
    pattern = r"^([A-Z0-1])\/(.+)-([0-9]+)'([A-Z]+)$"
    m = re.fullmatch(pattern, ep_string)

    if not m:
        raise EPError("Invalid EP format")

    header, payload, verify, fmt = m.groups()

    if header not in VALID_HEADERS:
        raise EPError("Invalid header")

    if fmt not in VALID_FORMATS:
        raise EPError("Unknown format")

    return header, payload, int(verify), fmt


# -------------------------------------------------
# DECODE
# -------------------------------------------------
def expand_runs(header: str, payload: str):
    if header not in {"0", "1"}:
        raise EPError("BIN decode supports only 0 or 1 header")

    runs = parse_payload(payload)

    current = header
    out = []

    for n in runs:
        out.append(current * n)
        current = "1" if current == "0" else "0"

    return "".join(out)


def decode(ep_string: str):
    header, payload, verify, fmt = parse_ep(ep_string)

    if fmt != "BIN":
        raise EPError("Reference decoder supports BIN only")

    binary = expand_runs(header, payload)

    if count_ones(binary) != verify:
        raise EPError("Verification failed")

    return binary


def validate(ep_string: str):
    try:
        decode(ep_string)
        return True
    except EPError:
        return False


# -------------------------------------------------
# TESTS
# -------------------------------------------------
def run_tests():
    print("=== BASIC ===")
    ep = "0/221112133-8'BIN"
    print(ep, "=>", decode(ep))

    print("\n=== MULTI DIGIT ===")
    ep2 = "0/22*12*3-15'BIN"
    print(ep2, "=>", decode(ep2))

    print("\n=== BLOCK MODE ===")
    ep3 = "0/*23'15'11'40*-26'BIN"
    print(parse_payload("*23'15'11'40*"))

    print("\n=== AUTO ENCODE ===")
    binary = "0" * 12 + "1" * 15 + "0" * 11 + "1" * 40
    ep4 = encode(binary)
    print(ep4)
    print(validate(ep4))

    print("\n=== INVALID ===")
    print(validate("0/22*12*3-99'BIN"))


if __name__ == "__main__":
    run_tests()
