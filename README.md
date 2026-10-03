# Anno 1503 Easy Player Boost

A gameplay balance mod for **Anno 1503 History Edition**. It speeds up production, expands the coverage of warehouses, markets, and public services, and shortens resident growth time.

## Changes

- Production cycle intervals for 26 player producer buildings are divided by four (up to 4× faster). This includes workshops, weapons producers, and cannon makers. Each archive keeps its own original values.
- Public-service coverage values are doubled for 17 service buildings, including chapels, churches, taverns, doctors, wells, schools, fire brigades, bath houses, libraries, and the university.
- All three radius-like coverage values are set to 30 for each player warehouse and main market level.
- Resident `VermehrTab` growth values are doubled for Pioneers, Settlers, Citizens, Merchants, and Aristocrats. Positive growth should be faster and negative growth should recover faster.

Carrier movement speed and carrier count are not changed in this test build. Their behavior is stored in binary records and the relevant fields have not been identified confidently.

## Install

1. Close the game.
2. Place this mod folder directly inside the game's install folder, beside `Anno1503.exe`.
3. Run `Install Boost.bat`. The first run saves original copies into this folder, builds the mod archives, then copies them into the game. Python 3 must be installed and available as `python`.
4. Start the game and check production, warehouse/main market coverage, public-service coverage, and resident growth.

The mod replaces `Anlagen.dat`, `Anlagen.classic`, `Anlagen.addon`, and `Data\\BGruppen.dat`. It does not modify the executable. The installer creates local `Original_*` backups on first run; these backups and generated game-data files are excluded from version control.

## Restore

Close the game and run `Restore Original Files.bat`. It restores the originals saved by the installer. Keep the `Original_*` files if you may want to restore later.

## Build and validation

`build_mod.py` reads the local `Original_*` backups when available, otherwise it reads the game files beside the mod folder. It verifies the selected records before writing. The building archives patch 26 producer records, 17 public-service records, and six player warehouse/market records. Production cycle values are divided by four; service coverage fields are doubled and all three warehouse/market coverage fields are set to 30. Resident growth values are doubled for all five groups.

This is a test candidate and has not been checked in-game. Test it before relying on it in a campaign.

## Credits and rights

Mod concept: faster production, expanded warehouse/market and public-service coverage, and faster resident growth for Anno 1503. Anno and its game data are Ubisoft property. No original game data is included in this repository.
