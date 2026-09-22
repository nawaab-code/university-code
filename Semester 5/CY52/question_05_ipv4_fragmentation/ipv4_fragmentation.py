"""Simulate IPv4 packet fragmentation and reassembly."""


def fragment_packet(packet_size, mtu):
    header = 20
    data_size = packet_size - header
    max_data = ((mtu - header) // 8) * 8

    if data_size < 0 or max_data <= 0:
        raise ValueError("Packet size or MTU is too small")

    fragments = []
    offset = 0
    remaining = data_size

    while remaining > 0:
        fragment_data = min(max_data, remaining)
        more_fragments = 1 if remaining > fragment_data else 0
        fragments.append((offset, fragment_data, more_fragments))
        offset += fragment_data // 8
        remaining -= fragment_data

    return fragments


def reassemble(fragments):
    return sum(fragment[1] for fragment in fragments) + 20


if __name__ == "__main__":
    packet_size = int(input("Enter original packet size (bytes): "))
    mtu = int(input("Enter MTU (bytes): "))
    fragments = fragment_packet(packet_size, mtu)

    print("\nFragment\tData Size\tOffset\tMF")
    for number, (offset, data_size, mf) in enumerate(fragments, 1):
        print(f"{number}\t\t{data_size}\t\t{offset}\t{mf}")

    reassembled_size = reassemble(fragments)
    print("\nReassembled packet size:", reassembled_size, "bytes")
    print("Reassembly successful!" if reassembled_size == packet_size else "Reassembly failed!")
