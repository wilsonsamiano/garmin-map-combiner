# Garmin Map Combiner

Desktop Mac app that merges OSM / [GMapTool](https://www.gmaptool.eu/) `.img` files into a single **`gmapsupp.img`** for older Garmin nüvi units (including the **nüvi 2589**).

It checks the **4 GB FAT32** file-size limit used by microSD cards those devices can read.

You do **not** need Garmin Express.

## Download the app

**[Garmin-Map-Combiner-macOS.zip](https://github.com/wilsonsamiano/garmin-map-combiner/releases/download/v1.0.0/Garmin-Map-Combiner-macOS.zip)** (v1.0.0)

1. Unzip the download.
2. Right-click **Garmin Map Combiner.app → Open**. macOS will warn that the developer is unidentified — choose **Open**.
3. Drag the app to the Dock.

The app is unsigned. Do not double-click it the first time; right-click Open is required once.

## Alternate install (uses Homebrew Python)

1. Download the source ZIP: [garmin-map-combiner-main.zip](https://github.com/wilsonsamiano/garmin-map-combiner/archive/refs/heads/main.zip) and unzip it.
2. Right-click **`install-macos.command` → Open**.
3. That writes **`~/Applications/Garmin Map Combiner.app`**. Drag it to the Dock.

## What you still need on the Mac

| Requirement | Why |
|---|---|
| macOS 13+ (Apple Silicon or Intel) | This app is a Mac GUI |
| [Java](https://formulae.brew.sh/formula/openjdk) (`brew install openjdk`) | Runs mkgmap |
| [mkgmap](https://www.mkgmap.org.uk/download/mkgmap.html) (`mkgmap.jar`) | Builds the combined map |

Python is **not** required for the Releases `.app`.

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
