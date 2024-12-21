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
 - the glitch Pokémon's index is from the list in `jpn_frlg_helper/resources/(your game version).csv`
 - the word index from `jpn_frlg_helper/resources/easy_chat.csv`

We can get this Pokémon via RNG manipulation, of which you can use the `Search RNG` option of this Python script or attempt to use a myriad of custom settings in PokéFinder's researcher to find your target.
The other option is to hope that the game's RNG has given you a suitable Pokémon, which after determining the PID, can pass in to the `Calculate PID` component of the tool and check the Pokémon's suitability.

> [!NOTE]  
> It is recommended that you set 'Advances' (not Initial Advances) to 100, as you are very likely to find a target.
> The searcher may become very slow if you set 'Advances' to a higher amount.

Once you have obtained your target, pass in the target's PID, your TID, and your game version then let it calculate the results.
It should have given you the PID substructure (not that important here), the adjustment type, the encryption key (the result of `(PID ^ TID) & 0xFFFF`), and a list of glitch Pokémon with their corresponding words.

Take note of one of these words (and perhaps the word group they belong to for easier searching, and maybe the glitch species associated with it), this will be your species word.

## II: Getting our adjustment numbers
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

For experience adjusted Pokémon, the adjustment number is what the experience needs to be before performing the mail glitch.
For EV adjusted Pokémon, the adjustment numbers represent a pair of EVs, which can be either HP / Attack or Sp.Attack / Sp.Defence depending on which one you choose.

## III: Writing glitchy mail
Perform the mail glitch like how it is done in any other version of FRLG.
Then when you get to writing the glitchy mail, make sure that the Pokémon that will be converted is in Box 3, Slot 1.
Where to write each word depends on the adjustment type and how you chose to adjust the Pokémon.
 - **Experience-adjusted Pokémon**: The species word must be in the 3rd slot, and the adjustment word in the 5th slot.
 - **EV-adjusted Pokémon (all)**: The species word must be in the 9th slot
    - **HP / Attack**: The adjustment word must be in the 3rd slot
    - **Sp.Attack / Sp.Defence**: The adjustment word must be in the 5th slot
Once you have written the glitchy mail, check Box 3 again, a decamark should have appeared in the Pokémon's place.

## Getting `0xFFC9`
Unless your decamark is `0xFFC9`, (check what species word you picked in step I and what species it corresponds to), run this code so that Japanese codes work as expected by using the correct decamark (make sure that party slot 3 is empty before running this):
```
Box  1: リ び ‥ o く _ ゼ n	[リび‥oく ゼn]
Box  2: _ ‥ t ま _ 1 t ほ	[ ‥tま 1tほ]
Box  3: ぁ m _ _ あ い	[ぁm  あい]
Box  4: ア B ぢ い い N	[アBぢいいN]
Box  5: O	[O]
```
`0xFFC9` should appear in party slot 3, and that should conclude this guide to setting up Japanese FRLG ACE.
If you want to get rid of the other grab ACE Pokémon created from earlier, then follow the following steps:
1. Place it in your party (should probably use the yellow hand)
2. In the party menu, move it to the front
3. Enter deposit mode in the PC
4. Select the decamark using the white hand
5. Select release and confirm
