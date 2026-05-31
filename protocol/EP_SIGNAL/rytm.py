"""EP_SIGNAL Rytm layer.

Rytm is the readable pulse-cadence view of EP_SIGNAL. It preserves the same
reversible binary truth as EP_SIGNAL while adding a compact rhythm packet that is
safe to use inside Cross-X plans. The layer is preview/transport metadata only;
it does not mutate EP_SIGNAL payloads, W3DB records, or W3Lgu source truth.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable

from protocol.EP_SIGNAL import reference_implementation as epi

_HEX_RUNS = {"A": 10, "B": 11, "C": 12, "D": 13, "E": 14, "F": 15}
_RUN_HEX = {value: key for key, value in _HEX_RUNS.items()}


@dataclass(frozen=True)
class RytmPacket:
    """Immutable Rytm packet.

    Fields intentionally mirror the RYTM_SIGNAL draft:
    start bit, pulse rhythm, optional W3Lgu/Cross-X meta tokens, verify value,
    and decode target format.
    """

    start: str
    rhythm: tuple[int, ...]
    verify: int
    fmt: str = "BIN"
    meta: tuple[str, ...] = ()
    source_ep_signal: str | None = None
    references: tuple[str, ...] = field(default_factory=lambda: (
        "protocol/EP_SIGNAL/RYTM_SIGNAL.md",
        "protocol/EP_SIGNAL/TecnicalRytm.md",
    ))

    def __post_init__(self) -> None:
        if self.start not in {"0", "1"}:
            raise ValueError("Rytm start must be '0' or '1'")
        if not self.rhythm or any(run <= 0 for run in self.rhythm):
            raise ValueError("Rytm rhythm requires positive run lengths")
        if self.verify < 0:
            raise ValueError("Rytm verify must be non-negative")
        object.__setattr__(self, "fmt", self.fmt.upper())
        object.__setattr__(self, "meta", tuple(_clean_meta(token) for token in self.meta if _clean_meta(token)))

    @property
    def pulse_count(self) -> int:
        return sum(self.rhythm)

    def to_signal(self) -> str:
        meta = "'" + "'".join(self.meta) + "'" if self.meta else ""
        return f"{self.start}/{encode_rhythm(self.rhythm)}{meta}-{self.verify}//{self.fmt}."

    def to_binary(self) -> str:
        current = self.start
        out: list[str] = []
        for run in self.rhythm:
            out.append(current * run)
            current = "1" if current == "0" else "0"
        binary = "".join(out)
        if binary.count("1") != self.verify:
            raise ValueError("Rytm verification failed")
        return binary

    def to_dict(self) -> dict[str, object]:
        return {
            "rytm_signal": self.to_signal(),
            "start": self.start,
            "rhythm": list(self.rhythm),
            "verify": self.verify,
            "format": self.fmt,
            "meta": list(self.meta),
            "pulse_count": self.pulse_count,
            "source_ep_signal": self.source_ep_signal,
            "references": list(self.references),
        }


def encode_rhythm(rhythm: Iterable[int]) -> str:
    """Encode run lengths as compact Rytm tokens.

    1..9 are direct digits, 10..15 are A..F, and larger values use `*n*`.
    """

    tokens: list[str] = []
    for run in rhythm:
        if run <= 0:
            raise ValueError("Rytm run length must be positive")
        if run <= 9:
            tokens.append(str(run))
        elif run in _RUN_HEX:
            tokens.append(_RUN_HEX[run])
        else:
            tokens.append(f"*{run}*")
    return "".join(tokens)


def parse_rhythm(value: str) -> tuple[int, ...]:
    """Parse compact Rytm run tokens back into run lengths."""

    runs: list[int] = []
    index = 0
    while index < len(value):
        token = value[index]
        if token.isdigit() and token != "0":
            runs.append(int(token))
            index += 1
        elif token in _HEX_RUNS:
            runs.append(_HEX_RUNS[token])
            index += 1
        elif token == "*":
            end = value.find("*", index + 1)
            if end == -1:
                raise ValueError("Unclosed Rytm star run")
            number = value[index + 1:end]
            if not number.isdigit() or int(number) <= 0:
                raise ValueError("Invalid Rytm star run")
            runs.append(int(number))
            index = end + 1
        else:
            raise ValueError(f"Invalid Rytm token: {token!r}")
    if not runs:
        raise ValueError("Rytm rhythm cannot be empty")
    return tuple(runs)


def rytm_from_binary(binary: str, *, meta: Iterable[str] = (), fmt: str = "BIN", source_ep_signal: str | None = None) -> RytmPacket:
    """Build a reversible Rytm packet from binary data."""

    if not binary or any(bit not in "01" for bit in binary):
        raise ValueError("Rytm binary input must be a non-empty 0/1 string")
    return RytmPacket(
        start=binary[0],
        rhythm=tuple(epi.runs_from_binary(binary)),
        verify=epi.count_ones(binary),
        fmt=fmt,
        meta=tuple(meta),
        source_ep_signal=source_ep_signal,
    )


def parse_rytm_signal(signal: str) -> RytmPacket:
    """Parse `[START]/[RHYTHM]'META'-[VERIFY]//[FORMAT].` into a packet."""

    text = signal.strip()
    if text.endswith("."):
        text = text[:-1]
    if "//" not in text:
        raise ValueError("Rytm signal requires //FORMAT")
    left, fmt = text.rsplit("//", 1)
    if "-" not in left:
        raise ValueError("Rytm signal requires -VERIFY")
    body, verify_text = left.rsplit("-", 1)
    if "/" not in body:
        raise ValueError("Rytm signal requires START/RHYTHM")
    start, rhythm_meta = body.split("/", 1)
    parts = rhythm_meta.split("'")
    rhythm_text = parts[0]
    meta = tuple(part for part in parts[1:] if part)
    if not verify_text.isdigit():
        raise ValueError("Rytm verify must be numeric")
    packet = RytmPacket(
        start=start,
        rhythm=parse_rhythm(rhythm_text),
        verify=int(verify_text),
        fmt=fmt,
        meta=meta,
    )
    # Validate reversibility now so invalid packets do not enter Cross-X traces.
    packet.to_binary()
    return packet


def rytm_from_ep_signal(ep_signal: str, *, meta: Iterable[str] = ()) -> RytmPacket:
    """Decode EP_SIGNAL and expose an equivalent Rytm packet."""

    binary = epi.decode(ep_signal)
    return rytm_from_binary(binary, meta=meta, source_ep_signal=ep_signal)


def build_rytm_preview(binary: str, *, meta: Iterable[str] = ()) -> dict[str, object]:
    """Build a preview dictionary for Cross-X and W3-API responses."""

    packet = rytm_from_binary(binary, meta=meta)
    return {
        "mode": "preview_only",
        "mutated": False,
        **packet.to_dict(),
    }


def _clean_meta(value: str) -> str:
    return "_".join(str(value).strip().upper().replace("'", "").split())
