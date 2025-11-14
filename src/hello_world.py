"""
Hello World static display - PORTRAIT
Run this, wait for it to complete, then unplug the Pico.
The display will keep showing the image without power.
(Physically rotate the display if you want landscape)
"""

from epd2in13b import EPD_2in13_B

print("="*40)
print("HELLO WORLD DISPLAY")
print("="*40)

# Initialize in portrait mode (104 x 212)
print("Initializing display...")
epd = EPD_2in13_B()

# Create content
print("Preparing content...")
epd.imageblack.fill(0xff)  # White background
epd.imagered.fill(0xff)

# Add "HELLO WORLD" text (centered)
epd.imageblack.text("HELLO", 20, 95, 0x00)
epd.imageblack.text("WORLD", 20, 110, 0x00)

# Add a border
epd.imageblack.rect(5, 5, 94, 202, 0x00)

# Display (will flash during update)
print("Updating display (flashing is normal)...")
epd.display()

print("="*40)
print("DONE!")
print("You can now unplug the Pico.")
print("The display will stay as-is forever.")
print("No need for sleep() - just unplug!")
print("="*40)
