"""Lab 5: simulate IPv4 fragmentation and reassembly with a 20-byte header."""

import argparse
from dataclasses import dataclass


IPV4_HEADER = 20  # no options
MAX_IPV4_PACKET = 65535


@dataclass(frozen=True)
class Fragment:
    offset_units: int  # IPv4 header stores offset in 8-byte units
    more_fragments: bool
    payload: bytes

    @property
    def total_length(self) -> int:
        return IPV4_HEADER + len(self.payload)


def fragment_packet(packet_size: int, mtu: int) -> tuple[bytes, list[Fragment]]:
    if not IPV4_HEADER <= packet_size <= MAX_IPV4_PACKET:
        raise ValueError("packet size (including header) must be 20..65535 bytes")
    if mtu < IPV4_HEADER:
        raise ValueError("MTU must fit the 20-byte IPv4 header")

    payload = bytes(i % 256 for i in range(packet_size - IPV4_HEADER))
    if packet_size <= mtu:
        return payload, [Fragment(0, False, payload)]

    max_payload = ((mtu - IPV4_HEADER) // 8) * 8
    if max_payload == 0:
        raise ValueError("MTU must be at least 28 bytes to fragment this packet")
    fragments = []
    for start in range(0, len(payload), max_payload):
        part = payload[start : start + max_payload]
        fragments.append(Fragment(start // 8, start + len(part) < len(payload), part))
    return payload, fragments


def reassemble(fragments: list[Fragment]) -> bytes:
    if not fragments:
        raise ValueError("no fragments received")
    ordered = sorted(fragments, key=lambda item: item.offset_units)
    result = bytearray()
    for index, fragment in enumerate(ordered):
        start = fragment.offset_units * 8
        if start != len(result):
            raise ValueError("fragment gap or overlap")
        if fragment.more_fragments != (index < len(ordered) - 1):
            raise ValueError("invalid More Fragments flag or missing final fragment")
        if fragment.more_fragments and len(fragment.payload) % 8:
            raise ValueError("non-final fragment payload must be a multiple of 8 bytes")
        result.extend(fragment.payload)
    return bytes(result)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("packet_size", type=int, help="original IPv4 packet size, including 20-byte header")
    parser.add_argument("mtu", type=int, help="outgoing link MTU, including fragment headers")
    args = parser.parse_args()
    try:
        original, fragments = fragment_packet(args.packet_size, args.mtu)
        reassembled = reassemble(list(reversed(fragments)))  # arrival order may differ
    except ValueError as error:
        parser.error(str(error))

    print("No.  Total bytes  Payload bytes  Offset (8-byte units)  MF")
    for number, item in enumerate(fragments, 1):
        print(f"{number:>3}  {item.total_length:>11}  {len(item.payload):>13}  {item.offset_units:>21}  {int(item.more_fragments):>2}")
    print(f"Reassembled payload: {len(reassembled)} bytes")
    print("Matches original:", reassembled == original)


if __name__ == "__main__":
    main()
