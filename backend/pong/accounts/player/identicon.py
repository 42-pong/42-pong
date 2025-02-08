import hashlib

# マスの個数
NUMBER_OF_CELLS: int = 5


def generate_identicon(username: str) -> None:
    def _create_bit_pattern(hash_value: str) -> list[list[int]]:
        length: int = len(hash_value)

        # 16進数のhash値を10進数に変換して2で割った余りのlistを作成(0 or 1)
        hash_bit_list: list[int] = [
            int(hash_value[i], 16) % 2 for i in range(length)
        ]
        # 5x3の二次元配列に変換
        width: int = NUMBER_OF_CELLS // 2 + 1
        bit_pattern: list[list[int]] = [
            hash_bit_list[i : i + width] for i in range(0, length, width)
        ]
        # 線対象に折り返して5x5の二次元配列に変換
        return [row + row[::-1][1:] for row in bit_pattern]

    hash_value: str = hashlib.md5(username.encode()).hexdigest()
    bit_pattern: list[list[int]] = _create_bit_pattern(hash_value[:15])
