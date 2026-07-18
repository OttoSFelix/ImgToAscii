# ImgToAscii

A command-line Python utility to convert images into ASCII art with support for custom character sets, contrast adjustments, and 24-bit ANSI colored terminal output.

## Installation & Setup

1. Make sure you have Python 3 installed.
2. Install dependencies:
   ```bash
   pip install pillow
   ```

## Usage

Run the converter by pointing it to any image:
```bash
python3 img_to_ascii.py <path_to_image> [options]
```

### Options

- `-w, --width <int>`: Set output width in characters. If omitted, the tool automatically detects your terminal's width.
- `-i, --invert`: Invert character mapping (recommended if you are using a light-colored terminal background).
- `-c, --color`: Enable 24-bit True Color ANSI output to display ASCII art with original colors.
- `-s, --charset <preset/string>`: Select character set. Presets include:
  - `standard` (default): ` .:-=+*#%@`
  - `detailed`: 70 characters for fine gradients
  - `blocks`: ` ░▒▓█` for block art
  - Alternatively, pass any custom string of characters (e.g., `"-#"`).
- `--contrast <float>`: Adjust contrast (e.g., `1.5` to make colors/details pop, `0.5` to flatten).
- `--aspect <float>`: Character aspect ratio correction factor (defaults to `0.55` to offset terminal height/width differences).

### Examples

- Standard grayscale rendering to terminal width:
  ```bash
  python3 img_to_ascii.py path/to/image.jpg
  ```
- Colored retro block-art (width 80):
  ```bash
  python3 img_to_ascii.py path/to/image.jpg -w 80 -s blocks -c
  ```
- Custom character set with enhanced contrast:
  ```bash
  python3 img_to_ascii.py path/to/image.jpg -s " .*" --contrast 1.7
  ```


  !['pengling'](/pengling2.png)

  !['original'](/original_pengling.png)