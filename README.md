# Kodi Build Switcher Addon

A Kodi addon for Android devices that allows easy switching between different Kodi instances by modifying [xbmc_env.properties](https://kodi.wiki/view/HOW-TO:Change_data_location_for_Android) file.

## Disclaimer

**Use at your own risk.**

This addon modifies your `xbmc_env.properties` file to switch Kodi builds. Always back up your `xbmc_env.properties` and any important data before using this addon. The author is not responsible for any data loss or issues resulting from its use.

## What it is

- An addon for quickly switching between kodi instances located in the root directory of your device
- The goal is similar to what Kodi forks are used for. The only reason to use this addon is if you have customized the installation of Kodi or are not a fan of using Kodi forks.

## What its not

- It is not a build installer. Every instance created is a brand new fresh Kodi install.
- You still need to install the build you would like manually.

## The Use Case

If you are like me, you have had issues customizing Kodi because permissions in the /sdcard/Data directory are restricted in the latest version of Android. Attempting to use a fork of Kodi does not work because using the `data` property in /sdcard/xbmc_env.properties will always load the same build not matter how many instances Kodi you install on your device.

Because I like trying/testing things before actually using them in my daily build (as everyone probably should), I (more and more) felt the need to have a plugin like this than to have separate devices with different builds to accomplish the same goal.

## Features

- Automatically scans `/sdcard/` for Kodi instance directories
- Detects Kodi directories by looking for .kodi directory
- Displays a list of available builds with the current build marked
- Option to create new Kodi instance directories directly from the addon
- Updates xbmc_env.properties `xbmc.data` property to switch builds
- Automatically quits Kodi after switching

## Requirements

- Kodi on Android
- Existing `xbmc_env.properties` file in `/sdcard/` with `xmbc.data` set
- Kodi instance directories located in `/sdcard/` **with this plugin installed on each build for easy switching**
- Proper file permissions for Kodi to read/write to external storage

## Installation

- Download the addon to your Android device
- Go to Add-ons → Install from zip file
- Navigate to the zip file and install
- Do not delete the zip file as you will need it for every Kodi instance you create

## Usage

1. **Launch the addon:**
   - Go to Add-ons → Program add-ons
   - Click on "Kodi Switcher"

2. **Select a build or create a new one:**
   - A dialog will appear showing available Kodi builds
   - The current build will be marked with `[CURRENT]`
   - Select an existing build to switch to
   - **or**
   - Select `+ Create New Build` to create a new build directory

3. **If creating a new build:**
   - An on-screen keyboard will appear
   - Enter a name for your new build directory
   - The addon will create the directory structure (`/sdcard/your_name/.kodi/`)
   - Proceed to step 4

4. **Confirm the switch:**
   - Read the confirmation message carefully
   - Click "Yes" to proceed

5. **Kodi quits automatically:**
   - A notification will briefly appear
   - Kodi will quit after 3 seconds
   - If it does not quit, force close Kodi manually.

6. **Restart Kodi:**
   - Launch Kodi from your launcher (I have seen this take up 5-10 seconds ONLY on initial start)
   - The new instance will load

## Directory Structure Example

Your `/sdcard/` directory should contain multiple Kodi build folders:

```
/sdcard/
├── xbmc_env.properties
├── kodi_main_build/
│   ├── .kodi/
│   └──── ...
├── kodi_diggz_xenon/
│   ├── .kodi/
│   └──── ...
└── kodi_cman/
    ├── .kodi/
    └──── ...
```

## Starting a new Kodi build

**Easy Method (Recommended):**

1. Open Kodi Switcher addon from within Kodi
2. Select `+ Create New Build` from the build list
3. Enter a name for your new build when prompted
4. The addon will create the directory structure automatically
5. Confirm the switch to activate the new build
6. Kodi will quit and when you restart it, you'll have a fresh Kodi install to customize

**Manual Method:**

1. Create a folder in `/sdcard` with the name you would like
2. Create an empty child folder named `.kodi` inside it
3. Open Kodi Switcher from within the current Kodi build being used
4. The new folder should be detected, switch to that build
5. Launch Kodi after it quits and you should have a fresh Kodi install to customize

## Permissions

On Android TV or newer Android versions, ensure Kodi has proper file permissions:

1. Go to Android Settings → Apps → Kodi
2. Select Permissions → Files and Media
3. Choose "Allow all the time"

## Troubleshooting

### No builds found

- Ensure your Kodi build directories are in `/sdcard/`
- Each build should have an `.kodi`

### Cannot write xbmc_env.properties

- Check that the file exists and is writable
- Verify Kodi has storage permissions
- Ensure `/sdcard/` is accessible

### Build doesn't switch after restart

- Try to **force quit** Kodi from Android settings
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
- **Detection method:** Scans for directories with `.kodi` folders
- **Platform:** Android only (due to `/sdcard/` path usage)

## Customization

You can modify the addon to:

## License

GPL-3.0-only

## Credits

Created for Kodi enthusiasts who manage multiple build configurations on Android devices.
