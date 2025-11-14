# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a MicroPython project for the Raspberry Pi Pico that drives a Waveshare 2.13" e-Paper Display Module B (black/red, 212×104 pixels, non-V4 version). The project is developed using VSCode with the MicroPico extension.

## Development Workflow

### Connecting to the Pico

The Pico must be connected and detected by VSCode before running any commands:

```bash
# In VSCode Command Palette (Ctrl+Shift+P):
# MicroPico: Connect
```

Verify connection by checking for "Pico Connected" in the status bar.

### Running Code on the Pico

**Upload a file to the Pico:**
```bash
# In VSCode Command Palette:
# Right-click file → "Upload to Pico"
# OR: MicroPico: Upload current file to Pico
```

**Run a file on the Pico:**
```bash
# In VSCode Command Palette:
# MicroPico: Run current file on Pico
```

**Auto-run on boot:**
- Any file named `main.py` on the Pico will automatically run when the device powers up
- Use this for persistent demos or applications

### Development Pattern

1. Write/edit Python files locally in VSCode (source files are in `src/`)
2. Upload the file(s) to the Pico using the MicroPico extension
3. Run the file to test
4. For driver files like `src/epd2in13b.py`, upload once and import in other scripts
5. The Pico's filesystem is separate from your local files - always upload before testing

## Code Architecture

### Display Driver (`src/epd2in13b.py`)

The driver provides two classes for different orientations:

**`EPD_2in13_B` (Portrait mode):**
- Dimensions: 104 (width) × 212 (height) pixels
- Default orientation - display is tall

**`EPD_2in13_B_Landscape` (Landscape mode):**
- Dimensions: 212 (width) × 104 (height) pixels
- Swaps width/height, sets data entry mode to 0x07 for proper landscape rendering

**Dual framebuffer architecture:**
- `imageblack`: FrameBuffer for black content
- `imagered`: FrameBuffer for red content
- Both framebuffers are rendered simultaneously with `display()`
- Drawing operations use `framebuf` methods: `text()`, `rect()`, `fill_rect()`, `line()`, `hline()`, `vline()`, `pixel()`

**Color convention (INVERTED for e-ink):**
- `0x00` = black/red (color ON)
- `0xff` = white (color OFF)
- Example: `imageblack.fill(0xff)` creates a white background

**Key methods:**
- `init()`: Initialize the display hardware (called automatically in `__init__`)
- `display()`: Send both black and red buffers to the display and refresh
- `display_mono_fast()`: Fast black/white only display (EPD_2in13_B only)
- `Clear(colorblack, colorred)`: Hardware clear operation
- `sleep()`: Put display into deep sleep mode to save power

### Hardware Pin Configuration

Pins are hardcoded in [src/epd2in13b.py](src/epd2in13b.py):
- SPI MOSI (DIN): GP11
- SPI CLK: GP10
- CS: GP9
- DC: GP8
- RST: GP12
- BUSY: GP13

The Waveshare e-Paper HAT connects directly to Pico headers with no additional wiring.

## Important Notes

### E-ink Display Characteristics

- **Slow refresh:** Display updates take 2-3 seconds - this is normal for e-ink technology
- **Persistent image:** E-ink displays retain the image even when unpowered - no need to keep the Pico connected after displaying static content
- **Flashing during update:** The display will flash black/white during refresh cycles - this is expected behavior
- **Ghost images:** Faint remnants of previous images may persist; call `Clear(0xff, 0xff)` multiple times to fully clear

### Common Pitfalls

1. **Forgetting to upload files:** The Pico's filesystem is independent - you must upload files before they can be imported or run
2. **Not calling `display()`:** Drawing operations only update the framebuffer in RAM; call `display()` to physically update the screen
3. **Color confusion:** Remember that 0x00 = colored, 0xff = white (inverted from typical conventions)
4. **Portrait vs. landscape confusion:** The two classes have different width/height values and different internal configurations - choose the right one for your orientation

### Project Structure

```
pico-display/
├── firmware/
│   └── micropython-pico.uf2    # MicroPython firmware for flashing
├── src/
│   ├── epd2in13b.py            # E-Paper display driver
│   └── hello_world.py          # Example demo script
├── CLAUDE.md                    # This file
└── README.md                    # User documentation
```

**File organization notes:**
- All Python source files are in `src/`
- `src/epd2in13b.py`: Display driver - upload to Pico once, then import it in your scripts
- `src/hello_world.py`: Example demo - shows basic text and border rendering
- `firmware/micropython-pico.uf2`: Pre-downloaded MicroPython firmware for convenience
- Files to create for your applications can be named anything, but `main.py` (when uploaded to Pico) will auto-run on boot
