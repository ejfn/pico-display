# Raspberry Pi Pico e-Paper Display

This project demonstrates how to use the **Waveshare 2.13" e-Paper Display Module B** with the Raspberry Pi Pico, programmed in MicroPython using VSCode.

## Hardware

- **Raspberry Pi Pico** (with soldered headers)
- **Waveshare Pico-ePaper-2.13-B** (2.13" e-Paper display, black/red, 212×104 pixels)
  - Non-V4 version (older model)
  - [Product page](https://www.waveshare.com/wiki/Pico-ePaper-2.13)

### Pin Connections

The display connects directly to the Pico via the header pins:

| e-Paper Pin | Pico Pin | Function            |
|-------------|----------|---------------------|
| VCC         | VSYS     | Power (5V tolerant) |
| GND         | GND      | Ground              |
| DIN         | GP11     | SPI MOSI            |
| CLK         | GP10     | SPI Clock           |
| CS          | GP9      | Chip Select         |
| DC          | GP8      | Data/Command        |
| RST         | GP12     | Reset               |
| BUSY        | GP13     | Busy Signal         |

> **Note**: If you have the Waveshare e-Paper HAT, it connects directly to the Pico headers - no wiring needed!

## Software Setup

### 1. Install MicroPython on the Pico

1. **Download MicroPython firmware**:
   - Go to [MicroPython Downloads for Pico](https://micropython.org/download/rp2-pico/)
   - Download the latest `.uf2` file (e.g., `rp2-pico-latest.uf2`)
   - OR use the pre-downloaded firmware in `firmware/micropython-pico.uf2`

2. **Flash the Pico**:
   - Hold the **BOOTSEL** button on the Pico while plugging it into your computer via USB
   - The Pico will appear as a USB mass storage device (like a flash drive)
   - Drag and drop the `.uf2` file onto the drive
   - The Pico will automatically reboot with MicroPython installed

### 2. Set Up VSCode

1. **Install VSCode** (if not already installed):
   - Download from [code.visualstudio.com](https://code.visualstudio.com/)

2. **Install the MicroPico Extension**:
   - Open VSCode
   - Go to Extensions (Ctrl+Shift+X / Cmd+Shift+X)
   - Search for "MicroPico"
   - Install the extension by **paulober**

3. **Configure the Extension**:
   - Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on Mac) to open the command palette
   - Type "MicroPico: Configure Project" and select it
   - This creates a `.vscode` folder with settings

### 3. Connect to the Pico

1. **Connect via MicroPico**:
   - Press `Ctrl+Shift+P` and run **MicroPico: Connect**
   - The extension will detect your Pico and connect to it
   - You should see "Pico Connected" in the status bar

2. **Verify connection**:
   - Open the terminal in VSCode (View → Terminal)
   - You can interact with the Pico's Python REPL if needed

## Running the Demo

### Upload Files to the Pico

1. **Upload the driver**:
   - Right-click on `src/epd2in13b.py` in VSCode
   - Select **"Upload to Pico"** (or use `Ctrl+Shift+P` → "MicroPico: Upload current file to Pico")

2. **Upload the demo**:
   - Right-click on `src/hello_world.py` (or rename it to `main.py` for auto-run)
   - Select **"Upload to Pico"**

### Run the Demo

**Option 1: Run from VSCode**
- Open `src/hello_world.py`
- Press `Ctrl+Shift+P` → **"MicroPico: Run current file on Pico"**
- Watch the output in the terminal

**Option 2: Auto-run on power-up**
- Rename `hello_world.py` to `main.py` before uploading (or upload as `main.py`)
- Files named `main.py` automatically run when the Pico boots
- Just unplug and replug the Pico USB cable
- The demo will run automatically

### What the Demo Does

The `hello_world.py` demo displays:
- "HELLO WORLD" text in black
- A border around the display
- Shows the persistent nature of e-ink (image remains without power)

## Project Files

```
pico-display/
├── firmware/
│   └── micropython-pico.uf2    # Pre-downloaded MicroPython firmware
├── src/
│   ├── epd2in13b.py            # E-Paper display driver (Waveshare)
│   └── hello_world.py          # Demo script (customize this!)
├── CLAUDE.md                    # Development guide for Claude Code
└── README.md                    # This file
```

## Customizing the Display

Create your own Python scripts in the `src/` folder. Here are some examples:

### Display Text

```python
from epd2in13b import EPD_2in13_B

epd = EPD_2in13_B()
epd.imageblack.fill(0x00)  # Clear to white (INVERTED!)
epd.imagered.fill(0x00)

epd.imageblack.text("Hello", 10, 10, 0xff)  # Black text
epd.imagered.text("World!", 10, 25, 0xff)   # Red text

epd.display()
```

### Draw Shapes

```python
# Lines
epd.imageblack.line(x1, y1, x2, y2, 0x00)  # Line from (x1,y1) to (x2,y2)
epd.imageblack.hline(x, y, width, 0x00)    # Horizontal line
epd.imageblack.vline(x, y, height, 0x00)   # Vertical line

# Rectangles
epd.imageblack.rect(x, y, width, height, 0x00)       # Outline
epd.imagered.fill_rect(x, y, width, height, 0x00)    # Filled

# Pixels
epd.imageblack.pixel(x, y, 0x00)  # Single pixel
```

### Display Dimensions

- Width: 104 pixels
- Height: 212 pixels
- Colors: Black (via `imageblack`) and Red (via `imagered`)
- Note: 0x00 = black/red, 0xff = white

### Important Notes

- The display has **two framebuffers**: `imageblack` and `imagered`
- Drawing to `imageblack` shows in black on the display
- Drawing to `imagered` shows in red on the display
- Call `epd.display()` to update the physical display
- The display refreshes slowly (2-3 seconds) - this is normal for e-ink!
- Always call `epd.sleep()` when done to save power

## Troubleshooting

### Display doesn't update
- Make sure you call `epd.display()` after drawing
- E-ink displays are slow - wait 2-3 seconds for refresh
- Try calling `epd.Clear(0xff, 0xff)` first

### "Pico not found" in VSCode
- Make sure MicroPython is installed (see Setup step 1)
- Try unplugging and replugging the USB cable
- Check that no other program (like Thonny) is connected to the Pico

### Import errors
- Make sure `epd2in13b.py` is uploaded to the Pico (it must be there for other scripts to import it)
- Check the terminal output for error messages

### Display shows ghost images
- E-ink displays can retain faint images
- Call `epd.Clear(0xff, 0xff)` multiple times
- This is normal for e-ink technology

## Next Steps

Now that you have the display working, you can:

- Display sensor data (temperature, humidity, etc.)
- Create a clock or calendar
- Show notifications or messages
- Display images (you'll need to convert them to bitmap format)
- Build a status dashboard

## Resources

- [Waveshare Wiki](https://www.waveshare.com/wiki/Pico-ePaper-2.13) - Official documentation
- [MicroPython Docs](https://docs.micropython.org/en/latest/rp2/quickref.html) - Pico reference
- [FrameBuffer Docs](https://docs.micropython.org/en/latest/library/framebuf.html) - Drawing functions
- [Waveshare GitHub](https://github.com/waveshare/Pico_ePaper_Code) - Original demo code

## License

The display driver (`src/epd2in13b.py`) is from Waveshare and is licensed under the MIT License.

---

**Happy Making!** If you build something cool, share it!
