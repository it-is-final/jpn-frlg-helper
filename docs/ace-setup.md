# Performing the ACE Setup
You want to perform this setup but cannot understand a single bit of Japanese, and translate is not helping you? Then try following the instructions below.

## Preamble
Unlike the mail glitch in Western FRLG, Japanese FRLG's mail glitch writes to an area that comprises all of substructure 2, and small bits of substructures 3 and 4.
This means that obtaining glitch Pokémon is going to be a different process as we cannot swap substructures, instead having to edit the substructure and carefully managing the checksum to turn a regular Pokémon into a grab ACE Pokémon.

This setup requires a specific Pokémon and adjusting the stats in a way that when two words of the 'mail' is edited (one for the species and the other for the stats that are adjusted), the checksum is preserved and the Pokémon becomes a glitch Pokémon.

However not all of the grab ACE Pokémon act in desirable ways so usually after converting the Pokémon, a code is executed to generate a Thumb grab ACE Pokémon with index number `0xFFC9` which will be the primary way ACE will be executed.

## I: Getting a suitable Pokémon
We want to get a Pokémon with a specific substructure order (specifically substructure orders 6, 7, 8, 12, 13, 18, and 19).
This Pokémon's PID must satisfy the following equation `((PID ^ TID) & 0xFFFF) ^ (glitch Pokémon's index) == (a word index from the easy chat system)`, where:
 - `^` is the bitwise XOR operation
 - `&` is the bitwise AND operation
 - the glitch Pokémon's index is from the list in [`jpn_frlg_helper/resources/(your game version).csv`](/jpn_frlg_helper/resources/)
 - the word index from [`jpn_frlg_helper/resources/easy_chat.csv`](/jpn_frlg_helper/resources/easy_chat.csv)

We can obtain this Pokémon either through catching a random Pokémon then check its PID or we can use RNG manipulation to guarantee us a suitable Pokémon.

### Obtaining without RNG manipulation
If we are obtaining this through catching a random Pokémon, we will need to have the PID of the Pokémon we caught.
An easy way to get this is calculating the IVs of the Pokémon and then inputting the IVs and the Pokémon's nature into something like [PokéFinder](https://github.com/Admiral-Fish/PokeFinder)'s IVs to PID tool to get back the PID.
The tool outputs a PID along with an associated 'Method' that the Pokémon was generated with. Below is a rough guide (sourced from Blisy's retail RNG Discord) of the most common methods to generate a Pokémon's PID and IVs:

**Method 1**
- Starters
- Fossils and gift Pokémon
- Static encounters
- Roaming Pokémon

**Reverse Method 1**
- Unown
- Box R/S Zigzagoon

**Method 2**
- Event gift Pokémon

**Wild**
- **Method 1**: FireRed or LeafGreen
- **Method 2**: *Not common in any game*
- **Method 4**: Fishing

> [!IMPORTANT]  
> Please check other the associated PIDs of other Methods if it turns out that the reported PID is not the caught Pokémon's PID.
> Generally the reported PID is wrong if writing the glitch mail in step III results in a `Bad EGG`.
> If the encounter type is not listed under a 'reverse' Method, it will never be generated under a 'reverse' Method, and vice versa.

To check that the PID satisfies the conditions outlined earlier, we use the `Calculate PID` tool, input the game version, TID, and PID then it should output data about the PID.
If the adjustment type is reported as `None` or the list of Glitch Pokémon and their associated words is printed as `None`, then the PID is not suitable for the setup, either try a PID associated with another Method (heeding the above note) or catch another Pokémon. Else, jump to the end of step I which should explain what to do with these results.

### Obtaining with RNG manipulation
We can select a target Pokémon with a PID is guarantted to satisfy the above conditions through RNG manipulation.
To do this, we use the `Search RNG` tool.
1. Select a seed you are aiming to get the target Pokémon from
2. Input the data into the `Search RNG` tool (Game version, encounter type, TID, seed, initial advances, advances, and delay (set to 0 if you are not using Lua scripts to RNG manipulate))
    - 'Advances' can be translated as 'Max Advances' in PokéFinder
    - 'Advances' generally does not need to be set to a value greater than 100, there are a lot of target Pokémon whose PID is suitable for this setup.
4. It should output a list of advances with their associated PID, select an advance then perform an RNG manipulation to obtain the Pokémon on that advance.
5. Use the `Calculate PID` tool, then enter the game version, TID, and PID then it should output data about the PID.

The `Calculate PID` tool should output the PID's substructure, the adjustment type of the PID, the encryption key (the result of `(PID ^ TID) & 0xFFFF`), and a list of glitch Pokémon with their corresponding words.
Take note of the adjustment type, the encryption key, one of the glitch Pokémon's index, and that glitch Pokémon's associated word (with their associated group if it helps with finding the word). The associated word is your *species word*.

## II: Getting our adjustment numbers
> [!WARNING]  
> You should probably save before performing any of the following actions, that way you have a recovery point in case of future mistakes.
> Do not perform any later saves until you have `0xFFC9` in step IV.

We have found one of the words we will be inputting into mail slot 255, but we still need the other word.
A nice part of this setup is that the word can be any word in the easy chat system however we can also let the tool run through all of the words then we can decide which one to use based off the degree of adjustment required.

In the tool, select `Calculate Adjustment`, then pass in the:
 - base Pokémon's index number
 - the glitch Pokémon's index number
 - encryption key
 - the other word index (or leave blank for the tool to run through all of the words)
 - the Pokémon's adjustment type
 - current Pokémon experience (if adjustment type is experience, else leave blank)

The tool should then output the word (which will be the adjustment word) along with either: a singular number (for experience adjustment) or two numbers separated by a comma in parentheses (for EV adjustment).

If you have chose to let it run through the whole list, it will show the whole list of words each with their own adjustment numbers.
Choose a word in the list as your adjustment word then note down the adjustment numbers.

We will need to adjust the Pokémon before writing the glitchy mail, what stats to adjust depends on the adjustment type.
Below is a guide on how to adjust your Pokémon based on the adjustment type and the adjustment numbers.
 - **Experience-adjusted Pokémon**: The Pokémon's experience must be equal to the adjustment number.
 - **EV-adjusted Pokémon**: The first stat's (HP or Sp.Attack) EVs must be equal to the first adjustment number.
   The second stat's (Attack if first stat is HP, Sp.Defense if first stat is Sp.Attack) EVs must be equal to the second adjustment number.

## III: Writing glitchy mail
Perform the mail glitch like how it is done in any other version of FRLG.
Then when you get to writing the glitchy mail, make sure that the Pokémon that will be converted is in Box 3, Slot 1.
Where to write each word depends on the adjustment type and how you chose to adjust the Pokémon.
 - **Experience-adjusted Pokémon**: The species word must be in the 3rd slot, and the adjustment word in the 5th slot.
 - **EV-adjusted Pokémon (all)**: The species word must be in the 9th slot
    - **HP / Attack**: The adjustment word must be in the 3rd slot
    - **Sp.Attack / Sp.Defence**: The adjustment word must be in the 5th slot
Once you have written the glitchy mail, check Box 3 again, a decamark should have appeared in the Pokémon's place.

> [!IMPORTANT]  
> If a bad EGG appeared in the Pokémon's place it can be caused by one of the following:
> - The words are in the wrong word slots of the glitchy mail
>     - If you have saved prior to performing the mail writing, go back and double check the word placement before writing.
>       Otherwise it may be the other cases.
> - The Pokémon is not adjusted correctly
>     - If you have saved prior to performing the mail writing, depending on the adjustment type do the following.
>         - **Experience-adjusted Pokémon**: If the experience is over the what the adjusted experience should be, go back to step II and recalculate with the new experience.
>           Otherwise add more experience until it is equal to what the adjusted experience should be.
>         - **EV-adjusted Pokémon**: If you have not been tracking your EVs properly, you must start back to step II or if you saved after performing step II, you must start all over again.
> - The reported PID used as the Pokémon's PID in the tool is not the Pokémon's PID
>     - This case only happens if the donor Pokémon is not obtained via RNG manipulation, in this case, start back at step I and either catch a different Pokémon or use another PID reported in the 'IVs to PID' tool as the Pokémon's PID.

## IV: Getting `0xFFC9`
> [!TIP]
> If you picked `0xFFC9` as your glitch Pokémon in step I, then you can skip the box code that creates `0xFFC9`

While we now have a glitch Pokémon, we generally only use this to create another glitch Pokémon that will actually execute most codes we want.
This is because:
- The Pokémon when swapped may execute at a different point in the boxes than what is expected
- The Pokémon may be executing in ARM or Thumb (the list includes both)
- Some of the glitch Pokémon cause strange graphical glitches when they are swapped

To mitigate this, we will create a glitch Pokémon with index number `0xFFC9` with the code below:
```
Box  1: リ び ‥ o く _ ゼ n	[リび‥oく ゼn]
Box  2: _ ‥ t ま _ 1 t ほ	[ ‥tま 1tほ]
Box  3: ぁ m _ _ あ い	[ぁm  あい]
Box  4: ア B ぢ い い N	[アBぢいいN]
Box  5: O	[O]
```

> [!IMPORTANT]  
> Graphical glitches are to be expected when creating `0xFFC9`.
> You can tell if you are still able to replace the Pokémon to another place and exit the PC afterwards.
> 
> However if the swap action crashes the game instead, then something has gone wrong and it could be caused by:
> - You have written the code wrong
>     - Double check every character, especially for the small kana such as `ぁ` vs `あ`
> - There is Pokémon or invisible Pokémon in the box slots after the entrypoint (this is shown in Step I on the glitch Pokémon list).
>     - Move them out or clear them via group select.
> - You have the wrong Pokémon
>     - See the bad EGG notice in step III for instructions and treat the decamark as if it was the bad EGG.

`0xFFC9` should appear in party slot 3, it's species name should be `むぅァいァい`(FireRed) or `mみみぅむぅ`(LeafGreen), and it should be holding the `????????` item.
To test whether the glitch Pokémon works, run the following code:
```
Box  1: ぞ ぞ ミ び	[ぞぞミび]
```

If the code does not crash, then you can follow the next few instructions to clean up the boxes.
Else check the notice on what to do if the game crashes.

If you want to get rid of the other grab ACE Pokémon created from earlier, then follow the steps below:
1. Place it in your party (should probably use the yellow hand)
2. In the party menu, move it to the front
3. Enter deposit mode in the PC
4. Select the decamark using the white hand
5. Select release and confirm

You have completed the grab ACE setup for Japanese FireRed and LeafGreen.
