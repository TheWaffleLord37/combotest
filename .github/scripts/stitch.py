from PIL import Image
import os
from datetime import datetime

chunk_dir = "chunks"
output_dir = "combo"
os.makedirs(output_dir, exist_ok=True)

chunks = sorted([f for f in os.listdir(chunk_dir) if f.endswith(".png")])

if not chunks:
    raise SystemExit("❌ No chunks found")

# open first to get size
first = Image.open(os.path.join(chunk_dir, chunks[0]))
cw, ch = first.size

# we know it's 2x2 chunks
grid_cols = 2
grid_rows = 2

final = Image.new("RGBA", (grid_cols * cw, grid_rows * ch), (0,0,0,0))

idx = 0
for r in range(grid_rows):
    for c in range(grid_cols):
        img = Image.open(os.path.join(chunk_dir, f"chunk_{idx}.png"))
        final.paste(img, (c * cw, r * ch))
        idx += 1

timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
outfile = os.path.join(output_dir, f"combo_{timestamp}.png")
final.save(outfile, "PNG")

print(f"✅ Saved stitched combo as {outfile}")
