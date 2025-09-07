from PIL import Image
import os
from datetime import datetime
import string

chunk_dir = "chunks"
output_dir = "combo"
os.makedirs(output_dir, exist_ok=True)

# Define prefixes (alphabetical order reversed)
prefixes = []
letters = string.ascii_lowercase
# e.g., zzzzz → zzzzy → ... aaaaa
for c1 in reversed(letters):
    for c2 in reversed(letters):
        for c3 in reversed(letters):
            for c4 in reversed(letters):
                for c5 in reversed(letters):
                    prefixes.append(c1+c2+c3+c4+c5)

# Find the next prefix based on existing files
existing_files = [f for f in os.listdir(output_dir) if f.endswith(".png")]
used_prefixes = [f.split("_")[0].replace("combo-", "") for f in existing_files]
next_prefix = next((p for p in prefixes if p not in used_prefixes), "zzzzz")

# Gather chunks
chunks = sorted([f for f in os.listdir(chunk_dir) if f.endswith(".png")])
if not chunks:
    raise SystemExit("❌ No chunks found")

# Open first chunk to get size
first = Image.open(os.path.join(chunk_dir, chunks[0]))
cw, ch = first.size

# We know it's 2x2 chunks
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
outfile = os.path.join(output_dir, f"combo-{next_prefix}_{timestamp}.png")
final.save(outfile, "PNG")

print(f"✅ Saved stitched combo as {outfile}")
