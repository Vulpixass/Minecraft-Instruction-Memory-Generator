import os
import re
import mcschematic

# === CONFIG ===
INPUT_FILE = "PseudoCODE.txt"
OUTPUT_FILE = "memory_towers.schem"

PHASES = [
    {"start": 0, "end": 15, "x": 74, "z": 2, "dir": "south"},
    {"start": 16, "end": 255, "x": 7, "z": 0, "dir": "north"},
    {"start": 256, "end": 527, "x": 37, "z": 0, "dir": "north"},
    {"start": 528, "end": 1023, "x": 7, "z": 2, "dir": "south"},
]

REGISTERS = {str(i): format(i, "04b") for i in range(16)}

OPERATIONS = {
    "NOP": "0000", "HLT": "0001", "ADD": "0010", "SUB": "0011",
    "NOR": "0100", "AND": "0101", "XOR": "0110", "RSH": "0111",
    "LDI": "1000", "ADI": "1001", "JMP": "1010", "BRH": "1011",
    "CAL": "1100", "RET": "1101", "LOD": "1110", "STR": "1111"
}

INSTRUCTION_FORMATS = {
    "NOP": "N", "HLT": "N", "ADD": "RRR", "SUB": "RRR", "NOR": "RRR",
    "AND": "RRR", "XOR": "RRR", "RSH": "RRR", "LDI": "RI", "ADI": "RI",
    "JMP": "J", "BRH": "BRH", "CAL": "J", "RET": "N", "LOD": "RRO", "STR": "RRO"
}

FLAGS = {"Z": "00", "NZ": "01", "C": "10", "NC": "11"}

Y_LEVELS = [0, -2, -4, -6, -8, -10, -12, -14, -19, -21, -23, -25, -27, -29, -31, -33]

# === Pre Process PseudoCODE.txt ===
def preprocess_pseudo_code(input_path="PseudoCODE.txt", output_path="Filled_PseudoCODE.txt"):
    try:
        with open(input_path, "r") as infile:
            lines = infile.readlines()

        filled_lines = []
        for i in range(1024):
            if i < len(lines) and lines[i].strip():
                filled_lines.append(lines[i].strip())
            else:
                filled_lines.append("NOP")

        with open(output_path, "w") as outfile:
            for line in filled_lines:
                outfile.write(line + "\n")

        print(f"Preprocessing complete. Filled {output_path} with 1024 lines.")
    except Exception as e:
        print(f"Error during preprocessing: {e}")

# === Parse PseudoCODE ===
preprocess_pseudo_code()
with open("Filled_PseudoCODE.txt", "r") as f:
    lines = f.readlines()

binary_instructions = []

for line in lines:
    tokens = line.strip().split()
    if not tokens:
        continue
    opcode = tokens[0]
    fmt = INSTRUCTION_FORMATS[opcode]
    if fmt == "RRR":
        r1 = REGISTERS[tokens[1]]
        r2 = REGISTERS[tokens[2]]
        r3 = REGISTERS[tokens[3]]
        binary = OPERATIONS[opcode] + r1 + r2 + r3
    elif fmt == "RI":
        r1 = REGISTERS[tokens[1]]
        imm = format(int(tokens[2]), "08b")
        binary = OPERATIONS[opcode] + r1 + imm
    elif fmt == "J":
        addr = format(int(tokens[1]), "010b")
        binary = OPERATIONS[opcode] + "00" + addr
    elif fmt == "N":
        binary = OPERATIONS[opcode] + "000000000000"
    elif fmt == "BRH":
        flag = FLAGS[tokens[1]]
        addr = format(int(tokens[2]), "010b")
        binary = OPERATIONS[opcode] + flag + addr
    elif fmt == "RRO":
        r_src = REGISTERS[tokens[1]]
        r_dest = REGISTERS[tokens[2]]
        offset_val = int(tokens[3])
        offset = format(offset_val & 0b1111, "04b")
        binary = OPERATIONS[opcode] + r_src + r_dest + offset
    else:
        raise ValueError(f"Unknown instruction format: {opcode}")
    binary_instructions.append(binary)

# === Build schematic ===
schem = mcschematic.MCSchematic()
SLICE_WIDTH = 16
TOWER_SPACING = 10
PHASE_GAP_X = 7
schem.setBlock((0, 0, 0), "minecraft:stone_button[face=floor]")
# === Precompute repeater coordinates
repeater_coords = set()
tower_positions = []

for addr, binary in enumerate(binary_instructions):
    for phase in PHASES:
        if phase["start"] <= addr <= phase["end"]:
            slice_index = (addr - phase["start"]) // SLICE_WIDTH
            tower_index = (addr - phase["start"]) % SLICE_WIDTH

            gap = 0
            if phase["start"] == 256 and slice_index >= 1:
                gap = 5
            elif phase["start"] == 528 and slice_index >= 16:
                gap = 5

            tower_x = phase["x"] + gap + slice_index * 2
            tower_z = phase["z"] + tower_index * TOWER_SPACING
            direction = phase["dir"]
            break

    tower_positions.append((addr, tower_x, tower_z, direction))

    for bit_index, bit in enumerate(binary):
        if bit == "1":
            y = Y_LEVELS[bit_index]
            repeater_coords.add((tower_x, y, tower_z))

# === Pass 1: Place gray wool, skipping repeater coords
for addr, binary in enumerate(binary_instructions):
    tower_x, tower_z, direction = tower_positions[addr][1:]
    
    if binary != "0000000000000000":
        schem.setBlock((tower_x, Y_LEVELS[0] + 1, tower_z), "minecraft:lime_wool")

    for bit_index in range(16):
        y = Y_LEVELS[bit_index]
        coord = (tower_x, y, tower_z)
        if coord not in repeater_coords:
            schem.setBlock(coord, "minecraft:gray_wool")

# === Pass 2: Place repeaters
for coord in repeater_coords:
    x, y, z = coord
    # Find direction from tower_positions
    addr = next(i for i, (a, tx, tz, _) in enumerate(tower_positions) if tx == x and tz == z)
    direction = tower_positions[addr][3]
    schem.setBlock(coord, f"minecraft:repeater[facing={direction},powered=false]")
            
# === Save schematic ===
custom_path = os.getenv("SCHEMATIC_OUTPUT_PATH")
schematics_dir = custom_path or os.path.join(os.getenv("APPDATA"), ".minecraft", "schematics")

schem.save(schematics_dir, OUTPUT_FILE.replace(".schem", ""), mcschematic.Version.JE_1_18_2)

print(f"✅ Saved as {OUTPUT_FILE}")
input("Press Enter to exit...")
