Well hello!
Thank you for Downloading this pretty complicated Instruction Generator

Credits:
Minecraft User: "Vulpixas" aka me
GitHub User: Vulpixass

WARNING:

Before you go heads into this I'd suggest watching LRR from Mattbatwings to further understand this and the Operations:
Youtube of Mattbatwings: https://www.youtube.com/@mattbatwings

What this Program does:

It takes in your Pseudo Code and turn it into a "memory\_towers.schem" file in whatever Directory you want in this Version of the program: "PseudoCODE to .schem, ADVANCED" by changing the Directory under: "Save schematic" or for the classic schematic Directory with this Version: "PseudoCODE to .schem"

Setup:
1. Install Python 3.10+
2. Install `mcschematic` using CMD or PowerShell:
    pip install mcschematic

Folder Structure:

- PseudoCODE.txt — Your Input file with pseudo instructions

- assembler.py — The compiler that converts pseudo code to `.schem`

- README.txt — Instruction manual and project overview

- LICENSE — The CC BY-NC license

- CPU Folder — Contains binary converter and `.mcfunction` generator

- World — Instruction memory world for testing

Now this is also an Instruction Manual so you know how this works in pseudo code:

In this we use Registers and in this case we have These REGISTERS to use:

R0  = 0;
R1  = 1;
R2  = 2;
R3  = 3;
R4  = 4;
R5  = 5;
R6  = 6;
R7  = 7;
R8  = 8;
R9  = 9;
R10 = 10;
R11 = 11;
R12 = 12;
R13 = 13;
R14 = 14;
R15 = 15;

Whilst R0 is a Zero Register(Always Outputs 0)

And Our OPERATIONS are These:



NOP = No Operation;
HLT = Halt the Program;
ADD = Add two Registers together and Output to one Register;
SUB = subtract two Registers and Output to one Register;
NOR = Or two Registers and Invert the Output and Output to one Register;
AND = And two Registers and Output to one Register;
XOR = Xor two Registers and Output to one Register;
RSH = divide 1 Register by 2 and Output into one Register;
LDI = Load a Number into a Register;
ADI = Add a Number to an existing Register;
JMP = Jump to the specified Line;
BRH = Jump to the specified Line IF a specific Flag is triggered;
CAL = Jump to a specified Line and Return with the RET function;
RET = Returns to the last CAL function Line +1;

We Also as seen up have FLAGS:

Z  = Outputs if the 8 bit Output is Zero;
NZ = Outputs if the 8 bit Output is NOT Zero;
C  = Outputs if the 9th bit is on(Carry Out);
NC = Outputs if the 9th bit is NOT on(Carry Out);

There are 5 Writing Types:

RRR, Example: ADD R1 R2 R3       (R1 + R2, Output into R3);
RI, Example: LDI R1 34           (Output to R1, Number 34);
J, Example: JMP 21               (Jump to Line 21);
N, Example: HLT                  (Halt the Program);
BRH, Example: BRH Z 14           (Jump to Line 14 if the last Number has the Zero Flag);

That is all to the Pseudo Code EXCEPT for one Thing and that is the RESTRICTIONS:

You can only do 1024 Instructions;

You can only have a maximum of 16 subprocesses using CAL;

For RRR you can only use a maximum of 4 Bit Numbers;

For RI you can only use first a maximum of 4 Bit Number and then have an 8 Bit Number;

For J you can have only use a maximum of 10 Bits for your Jump Destination;

For BRH you can only first use a maximum of 2 Bits for the Flags and then 10 Bits for your Jump Destination;

For N you can do whatever in hell you wanna do after the Operation;

For RSH you Need to first put in your wanted shifted Register and then 0(Register 0) and then your Output;

EXAMPLE PROGRAM:
See the Example Program in the named: "EXAMPLE_PseudoCODE.txt"



Also as seen in the CPU Folder there is a file there which will scan your Pseudo Code and turn it into Binary so you can read it and give you semi-correct .mcfunctions to paste it using a datapack into your World

Also for this you will Need McSchematic from I believe Slomayyy on Github: "https://github.com/Sloimayyy/mcschematic".
I have attached it in this Folder already but I don't know if this one works so you gotta try it on your own.

Also the World attached to here is the Instruction Memory I made myself and the Instruction Memory this Generator is based off from.


This project is licensed under the \[CC BY-NC 4.0 License](https://creativecommons.org/licenses/by-nc/4.0/).  

You may use, remix, and share it with credit, but not for commercial purposes.

