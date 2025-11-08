with open("PseudoCODE.txt", "r") as f:
    lines = f.readlines()

REGISTERS = {
    "0": "0000",
    "1": "0001",
    "2": "0010",
    "3": "0011",
    "4": "0100",
    "5": "0101",
    "6": "0110",
    "7": "0111",
    "8": "1000",
    "9": "1001",
    "10": "1010",
    "11": "1011",
    "12": "1100",
    "13": "1101",
    "14": "1110",
    "15": "1111"
}

OPERATIONS = {
    "NOP": "0000",
    "HLT": "0001",
    "ADD": "0010",
    "SUB": "0011",
    "NOR": "0100",
    "AND": "0101",
    "XOR": "0110",
    "RSH": "0111",
    "LDI": "1000",
    "ADI": "1001",
    "JMP": "1010",
    "BRH": "1011",
    "CAL": "1100",
    "RET": "1101",
    "LOD": "1110",
    "STR": "1111"
}
INSTRUCTION_FORMATS = {
    "NOP": "N",
    "HLT": "N",
    "ADD": "RRR",
    "SUB": "RRR",
    "NOR": "RRR",
    "AND": "RRR",
    "XOR": "RRR",
    "RSH": "RRR",
    "LDI": "RI",
    "ADI": "RI",
    "JMP": "J",
    "BRH": "BRH",
    "CAL": "J",
    "RET": "N",
    "LOD": "LOD",
    "STR": "STR",
}
FLAGS = {
    "Z": "00",
    "NZ": "01",
    "C": "10",
    "NC": "11",
}

binary_instructions = []

for i, line in enumerate(lines):
    tokens = line.strip().split()
    if not tokens:
        continue

    opcode = tokens[0]
    fmt = INSTRUCTION_FORMATS[opcode]
    if fmt == "RRR":
        operand1, operand2, operand3 = tokens[1], tokens[2], tokens[3]
        r1 = REGISTERS[operand1]
        r2 = REGISTERS[operand2]
        r3 = REGISTERS[operand3]
        binary = OPERATIONS[opcode] + r1 + r2 + r3

    elif fmt == "RI":
        operand1, operand2 = tokens[1], tokens[2]
        r1 = REGISTERS[operand1]
        imm = format(int(operand2), '08b')
        binary = OPERATIONS[opcode] + r1 + imm
    
    elif fmt == "J":
        operand1 = tokens[1]
        addr = format(int(operand1), '010b')
        binary = OPERATIONS[opcode] + addr

    elif fmt == "N":
        binary = OPERATIONS[opcode] + "000000000000"

    elif fmt == "BRH":
        flag_mode = FLAGS[tokens[1]]
        addr = format(int(tokens[2]), '010b')
        binary = OPERATIONS[opcode] + flag_mode + addr
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

address_map = {i: binary_instructions[i] for i in range(len(binary_instructions))}


Y_LEVELS = [0, -2, -4, -6, -8, -10, -12, -14, -19, -21, -23, -25, -27, -29, -31, -33]

with open("memory_towers.mcfunction", "w") as f:
    tower_count = 0
    x, z = 74, 2  # Phase 1 start
    x_phase2 = 7
    z_phase2 = 0
    x_phase3 = x_phase2 + 2 * 15 + 6
    z_phase3 = 0
    x_phase4 = 7
    z_phase4 = 2
    phase2_x_adds = 0
    phase3_x_adds = 0
    phase4_x_adds = 0

    for addr in sorted(address_map):
        binary = address_map[addr]

        if addr < 9:
            # Phase 1: first 9 towers at X=74, Z=2→152
            tower_x = x
            tower_z = z
            z += 10
            direction = "north"

        elif addr < 25:
            # Phase 2: next 16 towers at X=7, Z=0→150, then X+=2
            tower_x = x_phase2
            tower_z = z_phase2
            z_phase2 += 10
            direction = "north"
            if z_phase2 > 150:
                z_phase2 = 0
                phase2_x_adds += 1
                x_phase2 += 2
                if phase2_x_adds == 15:
                    x_phase2 += 6

        elif addr < 40:
            # Phase 3: next 15 towers after the +6 jump
            tower_x = x_phase2
            tower_z = z_phase3
            z_phase3 += 10
            direction = "north"
            if z_phase3 > 150:
                z_phase3 = 0
                phase3_x_adds += 1
                x_phase2 += 2

        else:
            # Phase 4: remaining 984 towers
            tower_x = x_phase4
            tower_z = z_phase4
            z_phase4 += 10
            direction = "south"
            if z_phase4 > 150:
                z_phase4 = 2
                phase4_x_adds += 1
                if phase4_x_adds == 15:
                    x_phase4 += 6
                else:
                    x_phase4 += 2

        # Place bits vertically
        for bit_index, bit in enumerate(binary):
            y = Y_LEVELS[bit_index]
            block = f"repeater[facing={direction}]" if bit == "1" else "purple_wool"
            f.write(f"setblock ~{tower_x} ~{y} ~{tower_z} minecraft:{block}\n")

        tower_count += 1
        
for addr in sorted(address_map):
    print(f"{addr:>4}: {address_map[addr]}")
    
input("Press Enter to exit...")