import colorsys
import hashlib

from PIL import Image, ImageDraw

# 画像のサイズ(pixel)
SIZE: int = 200
# マスの個数
NUMBER_OF_CELLS: int = 5
# マスの一辺の長さ(pixel)
PIXEL: int = 34
# 余白(pixel)
PADDING: int = (SIZE - PIXEL * NUMBER_OF_CELLS) // 2

BACKGROUND_COLOR: int = 0xDDDDDD


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

    def _create_color(hash_value: str) -> tuple[int, int, int]:
        # 色相
        hue: float = int(hash_value[0:3], 16) / 0xFFF * 360
        # 彩度
        saturation: float = 0.65 - int(hash_value[3:5], 16) / 0xFF * 0.2
        # 輝度
        luminance: float = 0.75 - int(hash_value[5:7], 16) / 0xFF * 0.2
        # HSLからRGBに変換
        r, g, b = colorsys.hls_to_rgb(hue / 360, luminance, saturation)
        return (int(r * 255), int(g * 255), int(b * 255))

    def _create_image(
        pattern: list[list[int]], color: tuple[int, int, int]
    ) -> Image.Image:
        def _draw_pixel(
            draw: ImageDraw.ImageDraw,
            y: int,
            x: int,
            color: tuple[int, int, int],
        ) -> None:
            draw.rectangle((x, y, x + PIXEL, y + PIXEL), fill=color)

        image: Image.Image = Image.new("RGB", (SIZE, SIZE), BACKGROUND_COLOR)
        draw: ImageDraw.ImageDraw = ImageDraw.Draw(image)
        for i in range(NUMBER_OF_CELLS):
            for j in range(NUMBER_OF_CELLS):
                if pattern[i][j]:
                    _draw_pixel(
                        draw,
                        PADDING + PIXEL * i,
                        PADDING + PIXEL * j,
                        color,
                    )
        return image

    hash_value: str = hashlib.md5(username.encode()).hexdigest()
    bit_pattern: list[list[int]] = _create_bit_pattern(hash_value[:15])
    color: tuple[int, int, int] = _create_color(hash_value[-7:])
    image: Image.Image = _create_image(bit_pattern, color)
