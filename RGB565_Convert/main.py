from PIL import Image
import os


def convert_to_rgb565_c_array(input_path, output_width=240, output_height=240, array_name="colorBitmap"):

    im = Image.open(input_path).convert("RGB").resize((output_width, output_height))

    lines = []
    lines.append(f"static const uint16_t {array_name}[{output_width}*{output_height}] PROGMEM = {{")
    for y in range(output_height):
        row = []
        for x in range(output_width):
            r, g, b = im.getpixel((x, y))
            rgb565 = ((r & 0xF8) << 8) | ((g & 0xFC) << 3) | (b >> 3)
            row.append(f"0x{rgb565:04X}")
        lines.append("    " + ", ".join(row) + ",")
    lines.append("};")
    return "\n".join(lines)


if __name__ == "__main__":
    # Input image path (adjust extension as needed)
    input_image = r"Location of PNG/JPG Input"
    # Output header file
    output_header = r"Location of the exported bitmap file"

    c_code = convert_to_rgb565_c_array(input_image, array_name="bitmap_1")

    with open(output_header, "w", encoding="utf-8") as f:
        f.write(c_code)

    print(f"RGB565 C array written to: {output_header}")
