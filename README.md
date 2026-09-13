# Garmin Map Combiner

Desktop app that merges OSM / [GMapTool](https://www.gmaptool.eu/) `.img` files into a single **`gmapsupp.img`** for older Garmin nüvi units (including the **nüvi 2589**).

It checks the **4 GB FAT32** file-size limit used by microSD cards those devices can read.

## What you need

| Requirement | Why |
|---|---|
| macOS 13+ (Apple Silicon or Intel) | This app is a Mac GUI |
| [Java](https://formulae.brew.sh/formula/openjdk) (`brew install openjdk`) | Runs mkgmap |
| [mkgmap](https://www.mkgmap.org.uk/download/mkgmap.html) (`mkgmap.jar`) | Builds the combined map |
| Python 3.13 + Tk (`brew install python@3.13 python-tk@3.13`) | The window |

You do **not** need Garmin Express.

## Install (double-click)

1. Download this repository as a ZIP (**Code → Download ZIP**) and unzip it.
2. Right-click **`install-macos.command` → Open**.
3. The app is copied to **`~/Applications/Garmin Map Combiner.app`**.
4. Open it from there, or drag it to the Dock.

If macOS says the file is from an unidentified developer, use **Open** from the right-click menu once.

## First run

1. Install Java if needed:

   ```bash
   brew install openjdk
   ```

2. Download **mkgmap** from [mkgmap.org.uk](https://www.mkgmap.org.uk/download/mkgmap.html), unzip it.

3. In the app:
   - **Add .img files** (for example Pacific, Mountain, South Central from GMapTool)
   - **Browse** to `mkgmap.jar` if it was not auto-detected
   - **Combine maps**

4. Copy the resulting `gmapsupp.img` (must be **under 4 GB**) onto a **FAT32** microSD card as:

   ```
   Garmin/gmapsupp.img
   ```

5. On the nüvi: **Settings → Map & Vehicle → myMaps**. Enable the OSM map. Turn the factory map off if streets look doubled.

## Overlap warnings

mkgmap may print `File already exists` when two regions share border tiles. That is normal. `Number of MapFailedExceptions: 0` means the merge succeeded.

## License

MIT. Map data belongs to [OpenStreetMap](https://www.openstreetmap.org/copyright) contributors. mkgmap is a separate GPL program — download it from its own site; it is not bundled here.
