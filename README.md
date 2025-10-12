# Kodi Build Switcher Addon

A Kodi addon for Android that allows you to easily switch between different Kodi data directories (builds) by modifying [xbmc_env.properties](https://kodi.wiki/view/HOW-TO:Change_data_location_for_Android) file.

## Disclaimer

**Use at your own risk.**

This addon modifies your `xbmc_env.properties` file to switch Kodi builds. Always back up your `xbmc_env.properties` and any important data before using this addon. The author is not responsible for any data loss or issues resulting from its use.

## The Use Case

If you are anything like me, you have had issues customizing Kodi because permissions in the /sdcard/Data directory are restricted in the latest version of Android. Attempting to use a fork of Kodi does not work because using the `data` property in /sdcard/xbmc_env.properties will always load the same build not matter how many instances Kodi you install on your device.

Because I like trying/testing things before actually using them in my daily build (as everyone should), I more and more felt the need to have a plugin like this than to have separate devices with different builds to accomplish the same goal.

## Features

- Automatically scans `/sdcard/` for Kodi build directories
- Detects Kodi directories by looking for characteristic folders (addons, userdata)
- Also finds directories with "kodi", "xbmc", or "build" in their names
- Displays a list of available builds with the current build marked
- Updates xbmc_env.properties `xbmc.data` property to switch builds
- Automatically quits Kodi after switching

## Requirements

- Kodi on Android
- Existing `xbmc_env.properties` file in `/sdcard/` with `xmbc.data` set
- Multiple Kodi build directories in `/sdcard/` **with this plugin installed on each build**
- Proper file permissions for Kodi to read/write to external storage

## Installation

- Download the adding to your Android device
- Go to Add-ons → Install from zip file
- Navigate to the zip file and install

## Usage

1. **Launch the addon:**

   - Go to Add-ons → Program add-ons
   - Click on "Kodi Switcher"

2. **Select a build:**

   - A dialog will appear showing available Kodi builds
   - The current build will be marked with `[CURRENT]`
   - Select the build you want to switch to

3. **Confirm the switch:**

   - Read the confirmation message carefully
   - Click "Yes" to proceed

4. **Kodi quits automatically:**

   - A notification will briefly appear
   - Kodi will quit after 3 seconds

5. **Restart Kodi:**
   - Launch Kodi from your launcher (I have seen this take up 5-10 seconds ONLY on initial start)
   - The new build will load

## Directory Structure Example

Your `/sdcard/` directory should contain multiple Kodi build folders:

```
/sdcard/
├── xbmc_env.properties
├── kodi_build_main/
│   ├── addons/
│   ├── userdata/
│   └── ...
├── kodi_build_gaming/
│   ├── addons/
│   ├── userdata/
│   └── ...
└── kodi_build_movies/
    ├── addons/
    ├── userdata/
    └── ...
```

## Starting a new Kodi build

1. Create a folder in `/sdcard` with the name you would like
2. Create an empty child folder named `addons` or `userdata`
3. Open Kodi Switcher from with the current Kodi build being used
4. The new folder should be detected, switch to that
5. Launch Kodi after it quits and you should have a fresh Kodi install to customize

## Permissions

On Android TV or newer Android versions, ensure Kodi has proper file permissions:

1. Go to Android Settings → Apps → Kodi
2. Select Permissions → Files and Media
3. Choose "Allow all the time"

## Troubleshooting

### No builds found

- Ensure your Kodi build directories are in `/sdcard/`
- Each build should have an `addons` or `userdata` folder
- Or name directories with "kodi", "xbmc", or "build" in the name

### Cannot write xbmc_env.properties

- Check that the file exists and is writable
- Verify Kodi has storage permissions
- Ensure `/sdcard/` is accessible

### Build doesn't switch after restart

- Try **force stopped** Kodi from Android settings
- Simply closing Kodi is not enough, sometimes you must force stop it
- Go to Android Settings → Apps → Kodi → Force Stop
- Then restart Kodi
- The `xbmc_env.properties` file is only read when Kodi starts fresh

### How to force stop Kodi on Android

1. Press Home button to exit Kodi
2. Open Android Settings
3. Navigate to Apps or Application Manager
4. Find and tap on Kodi
5. Tap "Force Stop" button
6. Confirm if prompted
7. Return to home screen and launch Kodi again

## Technical Details

- **xbmc_env.properties format:** `xbmc.data=/sdcard/your_build_directory`
- **Detection method:** Scans for directories with `addons` or `userdata` folders
- **Platform:** Android only (due to `/sdcard/` path usage)

## Customization

You can modify the addon to:

- Change the root directory (edit `ROOT_DIR` in addon.py)
- Adjust directory detection logic (edit `get_kodi_directories()` function)
- Add additional validation checks
- Include custom build naming conventions

## License

GPL-3.0-only

## Credits

Created for Kodi enthusiasts who manage multiple build configurations on Android devices.
