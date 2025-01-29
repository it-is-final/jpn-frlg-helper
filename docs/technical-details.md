# Technical details of Japanese ACE Setup
In the Japanese versions of FireRed and LeafGreen (FRLG), mail corruption writes to a different area of Pokémon data in Box 3, Slot 1.
Unlike western versions of FRLG where mail corruption writes to the PID, TID, and nickname of the Pokémon data structure, in the Japanese version, mail corruption writes to the last two halfwords of substructure 1, all of substructure 2, and the first halfword of substructure 3.
Below is a visual representation of where in the Pokémon data mail corruption writes to in these versions:

<img src="jp-mail-corruption-area.png" alt="A visual representation of the mail corruption in Japanese FireRed and LeafGreen" width=300>

This unfortunately means that obtaining a glitch Pokémon is nowhere near as simple as having specific substructure data then swapping the substructures of a donor Pokémon with a specific PID to get what we want.

## Getting the glitch Pokémon
For the ACE setup here, we are modifying the species halfword in the growth substructure, and to maintain a valid checksum, we either modify the lower halfword of the experience field or two EV fields that are of specific pairs which form a halfword in the data structure which are HP and Attack or Sp.Attack and Sp.Defense.
If the lower experience halfword is modified to maintain the checksum, this requires the growth substructure to be substructure 2 in the overall data structure.
Else if the EV stats are the ones being modified to maintain the checksum, this requires the EV/Condition to be substructure 2, **and** growth to be substructure 3.
Below is a guide on which substructure orders can have the checksum maintained by either EVs or experience:
- EV: 8 (AEGM), 22 (MEGA)
- Experience: 6 (AGEM), 7 (AGME), 12 (EGAM), 13 (EGMA), 18 (MGAE), 19 (MGEA)

### Calculating the specific values
#### Species word
The index of the easy chat word that writes the value we want into the species field can be determined from the following formula:
```
(PID_LOW XOR TID) XOR value = INDEX
```
Due to the limitations of the easy chat system’s wordlist, even with a usable PID substructure order, it is still possible for the PID/TID combination to yield no usable options due to the formula producing an unwritable easy chat system word index for every relevant glitch Pokémon index.
The large range of target values available allows this method to be barely viable without RNG manipulation (though you must guess its PID from IVs if you are going this route).

#### Checksum adjustment
A stat of the Pokémon is adjusted so that the checksum accounts for the difference in what is written in the species field, and what is written in the chosen adjustment field.
When the species word, and the checksum word overwrites the existing values, due to this adjustment made earlier, the Pokémon will still be seen as having a valid checksum.

The general adjustment value to allow maintaining a valid checksum after mail corruption is calculated from the following formula:
```
GLITCH_MON_INDEX - BASE_SPECIES_INDEX = DIFFERENCE 
(PID_LOW XOR TID) XOR INDEX_OF_CHECKSUM_WORD = DECRYPTED_VALUE
(DIFFERENCE + DECRYPTED_VALUE) AND 0xFFFF = ADJUSTMENT
```

The exact values for the stats is calculated using the formulas below:
```
ADJUSTMENT = EXPERIENCE AND 0xFFFF (the upper 16 bits of the experience field does not matter)
ADJUSTMENT AND 0xFF = EV 1 (HP or Sp.Attack)
(ADJUSTMENT Rsh 16) AND 0xFF = EV 2 (Attack or Sp.Defense)
```
If an adjustment is made via effort values, it must be noted that the EVs adjusted **must** be either HP and Attack or Sp.Attack and Sp.Defense, they cannot be mix and matched.

### How are we writing encrypted data without knowing the secret ID?
Pokémon data in the generation III games are encrypted through a bitwise XOR of each word in the substructures with the encryption key.
This encryption key is formed through a bitwise XOR of the Pokémon’s PID and the Pokémon’s OTID which is $\text{TID} + \text{SID} \times 65536$.

Since it is unlikely that players would have known about their secret ID beforehand, the upper halfword of the encryption key is unknowable.
However if we know the PID, we can still decrypt the lower halfword of each word in the Pokémon data structure through the trainer ID which forms the lower half of the encryption key.

From the information in this [Bulbapedia article](https://bulbapedia.bulbagarden.net/wiki/Pok%C3%A9mon_data_substructures_(Generation_III)#Format), we know the arrangement of each field in each data substructure relative to each other.
This allows us to determine which field is encrypted by which part of the encryption key.
Species, the lower 2 bytes of the experience field, HP and Attack EVs, and Sp.Attack and Sp.Defense EVs are all encrypted by the known half of the encryption key which enables us to modify the fields without needing to know the secret ID.

### Donor Pokémon characteristics summary
The Pokémon must have:
- PID substructure orders 8 or 22 if adjusting with EVs or 6, 7, 12, 13, 18 or 19 if adjusting experience
- `PID_LOW XOR TID XOR GLITCH_POKEMON_INDEX` must be a writable easy chat system word index
- Stats are adjusted prior to corruption to adjust checksum to account for both the adjusted species value as well as the stats themselves
    - These stats are overwritten by another easy chat system word which allows the corruption process to still keep the checksum valid
    - These stats are the lower 16 bits of experience or HP/Attack EVs or Sp.Attack/Sp.Defense EVs

## 0xFFC9 creation
This is analogous to using 0x611 to create a more stable ACE Pokémon in western releases of Emerald.
While the wide range of targets allows the acquisition of a donor Pokémon to be less specific, the environment set up varies between each species.

The reasons why we use the initial glitch species to create another glitch species is listed below:
- Performing grab ACE causes major graphical glitches (e.g. screen turns black)
- Different CPU execution state (ARM vs Thumb)
- Differing entrypoints within the boxes

This is why the final step of the setup is creating 0xFFC9 which is the main grab ACE Pokémon used in the Japanese glitching community.
The code is below:
```
Box  1: リ び ‥ o く _ ゼ n	[リび‥oく ゼn]
Box  2: _ ‥ t ま _ 1 t ほ	[ ‥tま 1tほ]
Box  3: ぁ m _ _ あ い	[ぁm  あい]
Box  4: ア B ぢ い い N	[アBぢいいN]
Box  5: O	[O]
```
and the exact instructions that make up the code is as follows:
```
4778        BX PC ; Switch to ARM (for Thumb Pokémon), filler otherwise
E3B0        ; filler
E28F0008    ADD R0, PC, #0x8
E8B000FF    LDMIA R0!, {R0, R1, R2, R3, R4, R5, R6, R7}
E8A2001F    STMIA R2!, {R0, R1, R2, R3, R4}
E12FFF1E    BX LR
02010000    ; hasSpecies set, language = Japanese, R0 task end set
51FFFFFF    ; filler
020242BC    ; Address of party slot 3, at nickname chars 8-9, lang and egg flags
FFFFFFC8    ; Checksum and unused data
FFFFFFC9    ; Species and held item
```