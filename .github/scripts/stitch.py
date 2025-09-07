from PIL import Image
import os
from datetime import datetime
import string
import math

chunk_dir = "chunks"
output_dir = "combo"
os.makedirs(output_dir, exist_ok=True)

# ----------------------------
# Define reverse prefixes (zzzzz -> aaaaa)
# ----------------------------
prefixes = []
letters = string.ascii_lowercase
for c1 in reversed(letters):
    for c2 in reversed(letters):
        for c3 in reversed(letters):
            for c4 in reversed(letters):
                for c5 in reversed(letters):
                    prefixes.append(c1+c2+c3+c4+c5)

# ----------------------------
# Determine next available prefix
# ----------------------------
existing_files = [f for f in os.listdir(output_dir) if f.endswith(".png")]
used_prefixes = [f.split("_")[0].replace("combo-", "") for f in existing_files]
next_prefix = next((p for p in prefixes if p not in used_prefixes), "zzzzz")

# ----------------------------
# Gather chunks
# ----------------------------
chunks = sorted([f for f in os.listdir(chunk_dir) if f.endswith(".png")],
                key=lambda x: int(x.split("_")[1].split(".")[0]))  # sort numerically
if not chunks:
    raise SystemExit("❌ No chunks found")

# ----------------------------
# Determine grid size automatically
# ----------------------------
num_chunks = len(chunks)
grid_cols = math.ceil(math.sqrt(num_chunks))
grid_rows = math.ceil(num_chunks / grid_cols)

# ----------------------------
# Open first chunk to get size
# ----------------------------
first = Image.open(os.path.join(chunk_dir, chunks[0]))
cw, ch = first.size

final = Image.new("RGBA", (grid_cols * cw, grid_rows * ch), (0, 0, 0, 0))

# ----------------------------
# Paste chunks into final image
# ----------------------------
idx = 0
for r in range(grid_rows):
    for c in range(grid_cols):
        if idx >= num_chunks:
            break
        img_path = os.path.join(chunk_dir, f"chunk_{idx}.png")
        img = Image.open(img_path)
        final.paste(img, (c * cw, r * ch))
        idx += 1

# ----------------------------
# Save stitched combo
# ----------------------------
timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
outfile = os.path.join(output_dir, f"combo-{next_prefix}_{timestamp}.png")
final.save(outfile, "PNG")

print(f"✅ Saved stitched combo as {outfile}")
