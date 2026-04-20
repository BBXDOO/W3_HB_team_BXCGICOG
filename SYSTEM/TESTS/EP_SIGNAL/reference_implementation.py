import re


class EPError(Exception):
    pass


VALID_HEADERS = {"0", "1", "H", "M", "C", "X"}
VALID_FORMATS = {"BIN", "HEX", "META", "CLR", "SYM", "PKG", "RAW"}


def count_ones(binary_string: str) -> int:
    return binary_string.count("1")


# -------------------------------------------------
# PAYLOAD PARSER (รองรับ *12*)
# -------------------------------------------------
def parse_payload(payload: str):
    """
    ตัวอย่าง:
    22113       => [2,2,1,1,3]
    22*12*3     => [2,2,12,3]
    *25*13*40*  => [25,1,3,40]
    """
    runs = []
    i = 0

    while i < len(payload):
        ch = payload[i]

        # multi-digit mode
        if ch == "*":
            j = payload.find("*", i + 1)
            if j == -1:
                raise EPError("Unclosed * marker in payload")

            number_text = payload[i + 1:j]

            if not number_text.isdigit():
                raise EPError("Invalid number inside * *")

            runs.append(int(number_text))
            i = j + 1

        # single digit mode
        elif ch.isdigit():
            runs.append(int(ch))
            i += 1

        else:
            raise EPError("Invalid payload character")

    return runs


# -------------------------------------------------
# ENCODER
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


def encode_run(n: int) -> str:
    if n <= 9:
        return str(n)
    return f"*{n}*"


def encode(binary_string: str, fmt="BIN") -> str:
    if not re.fullmatch(r"[01]+", binary_string):
        raise EPError("Binary input must contain only 0/1")

    if fmt not in VALID_FORMATS:
        raise EPError("Unknown format")

    header = binary_string[0]
    runs = runs_from_binary(binary_string)

    payload = "".join(encode_run(x) for x in runs)
    verify = count_ones(binary_string)

    return f"{header}/{payload}-{verify}'{fmt}"


# -------------------------------------------------
# PARSE FULL EP STRING
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

    for length in runs:
        out.append(current * length)
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
    print("=== BASIC TEST ===")
    ep = "0/221112133-8'BIN"
    print(ep, "=>", decode(ep))

    print("\n=== MULTI DIGIT TEST ===")
    binary = "0" * 12 + "1" * 3
    ep2 = encode(binary)
    print("binary:", binary)
    print("EP:", ep2)
    print("decoded:", decode(ep2))

    print("\n=== MANUAL PAYLOAD TEST ===")
    ep3 = "0/22*12*3-15'BIN"
    print(ep3, "=>", decode(ep3))

    print("\n=== VALIDATION ===")
    print(validate("0/22*12*3-15'BIN"))
    print(validate("0/22*12*3-99'BIN"))


if __name__ == "__main__":
    run_tests()
