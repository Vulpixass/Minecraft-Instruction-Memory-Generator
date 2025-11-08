import os
import re
import mcschematic

# === CONFIG ===
INPUT_FILE = "PseudoCODE.txt"
OUTPUT_FILE = "memory_towers.schem"

REGISTERS = {
    str(i): format(i, "04b") for i in range(16)
}

OPERATIONS = {
    "NOP": "0000", "HLT": "0001", "ADD": "0010", "SUB": "0011",
    "NOR": "0100", "AND": "0101", "XOR": "0110", "RSH": "0111",
    "LDI": "1000", "ADI": "1001", "JMP": "1010", "BRH": "1011",
     "CAL": "1100", "RET": "1101", "LOD": "1110", "STR": "1111"
}

INSTRUCTION_FORMATS = {
    "NOP": "N", "HLT": "N", "ADD": "RRR", "SUB": "RRR", "NOR": "RRR",
    "AND": "RRR", "XOR": "RRR", "RSH": "RRR", "LDI": "RI", "ADI": "RI",
    "JMP": "J", "BRH": "BRH", "CAL": "J", "RET": "N", "LOD" : "LOD",
    "STR": "STR"
}

FLAGS = {
    "Z": "00", "NZ": "01", "C": "10", "NC": "11"
}

Y_LEVELS = [0, -2, -4, -6, -8, -10, -12, -14, -19, -21, -23, -25, -27, -29, -31, -33]

# === Parse PseudoCODE ===
with open(INPUT_FILE, "r") as f:
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
        binary = OPERATIONS[opcode] + addr
    elif fmt == "N":
        binary = OPERATIONS[opcode] + "000000000000"
    elif fmt == "BRH":
        flag = FLAGS[tokens[1]]
        addr = format(int(tokens[2]), "010b")
        binary = OPERATIONS[opcode] + flag + addr
    elif fmt == "LOD":
        r_src = REGISTERS[tokens[1]] 
        r_dest = REGISTERS[tokens[2]]  
        offset = format(int(tokens[3]), "04b") 
        binary = OPERATIONS[opcode] + r_src + r_dest + offset
    elif fmt == "STR":
        r_ptr = REGISTERS[tokens[1]]
        value = format(int(tokens[2]), "08b")
        binary = OPERATIONS[opcode] + r_ptr + value
    else:
        raise ValueError(f"Unknown instruction format: {opcode}")
    binary_instructions.append(binary)

# === Build schematic ===
schem = mcschematic.MCSchematic()
x, z = 74, 2
x_phase2 = 7
z_phase2 = 0
x_phase3 = x_phase2 + 2 * 15 + 7
z_phase3 = 0
x_phase4 = 7
z_phase4 = 2
phase2_x_adds = phase3_x_adds = phase4_x_adds = 0
schem.setBlock((0, -33, -1), "minecraft:stone_button[face=floor]")


for addr, binary in enumerate(binary_instructions):
    if addr < 16:
        tower_x, tower_z = x, z
        z += 10
        direction = "south"
    elif addr < 256:
        tower_x, tower_z = x_phase2, z_phase2
        z_phase2 += 10
        direction = "north"
        if z_phase2 > 150:
            z_phase2 = 0
            phase2_x_adds += 1
            x_phase2 += 2
            if phase2_x_adds == 15:
                x_phase2 += 6
    elif addr < 520:
        tower_x, tower_z = x_phase3, z_phase3
        z_phase3 += 10
        direction = "north"
        if z_phase3 > 150:
            z_phase3 = 0
            phase3_x_adds += 1
            x_phase3 += 2
    elif addr < 1024:
        tower_x, tower_z = x_phase4, z_phase4
        z_phase4 += 10
        direction = "south"
        if z_phase4 > 150:
            z_phase4 = 2
            phase4_x_adds += 1
            x_phase4 += 6 if phase4_x_adds == 15 else 2

    for bit_index, bit in enumerate(binary):
        y = Y_LEVELS[bit_index]
        block = f"minecraft:repeater[facing={direction},powered=false]" if bit == "1" else "minecraft:air"
        schem.setBlock((tower_x, y, tower_z), block)

# === Save schematic ===
schematics_dir = os.path.join(os.getenv("APPDATA"), ".minecraft", "schematics")
schem.save(schematics_dir, OUTPUT_FILE.replace(".schem", ""), mcschematic.Version.JE_1_18_2)
print(f"✅ Saved as {OUTPUT_FILE}")
input("Press Enter to exit...")
