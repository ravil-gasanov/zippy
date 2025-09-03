import heapq


class Node:
    weight: int = None
    char: str = None
    left = None
    right = None

    def __init__(self, weight: int, char: str = None, left=None, right=None):
        self.weight = weight
        self.char = char
        self.left = left
        self.right = right

    def __lt__(self, other):
        return self.weight < other.weight


def build_huffman_tree(character_frequency_table):
    heap = [
        Node(weight=freq, char=char) for char, freq in character_frequency_table.items()
    ]
    heapq.heapify(heap)

    while len(heap) > 1:
        l = heapq.heappop(heap)
        r = heapq.heappop(heap)

        merged_tree = Node(
            weight=l.weight + r.weight,
            char=None,
            left=l,
            right=r,
        )

        heapq.heappush(heap, merged_tree)

    return heap[0]
