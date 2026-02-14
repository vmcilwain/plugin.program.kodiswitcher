"""
Kodi Build Switcher Addon
addon.py - Main addon file
"""

import xbmc
import xbmcaddon
import xbmcgui
import xbmcvfs
import os
import sys
import subprocess

ADDON = xbmcaddon.Addon()
ADDON_NAME = ADDON.getAddonInfo('name')
ADDON_ID = ADDON.getAddonInfo('id')

ENV_FILE_PATH = '/sdcard/xbmc_env.properties'

ROOT_DIR = '/sdcard/'


def log(message, level=xbmc.LOGINFO):
    """Log message to Kodi log"""
    try:
        xbmc.log('[{0}] {1}'.format(ADDON_ID, message), level)
    except:
        pass


def get_kodi_directories():
    """
    Scan the root directory for potential Kodi data directories
    Returns a list of directory names that appear to be Kodi builds
    """
    kodi_dirs = []
    
    try:
        dirs, files = xbmcvfs.listdir(ROOT_DIR)
        
        for directory in dirs:
            dir_lower = directory.lower()
            if 'kodi' in dir_lower or 'xbmc' in dir_lower or 'build' in dir_lower:
                kodi_dirs.append(directory)
                log('Found Kodi directory: {0}'.format(directory))

    except Exception as e:
        log('Error scanning directories: {0}'.format(str(e)), xbmc.LOGERROR)
    
    return sorted(kodi_dirs)


def get_current_location():
    """
    Read the current Kodi data location from xbmc_env.properties
    Returns the path or None if not set
    """
    try:
        if xbmcvfs.exists(ENV_FILE_PATH):
            file_handle = xbmcvfs.File(ENV_FILE_PATH, 'r')
            content = file_handle.read()
            file_handle.close()
            
            for line in content.split('\n'):
                line = line.strip()
                if line.startswith('xbmc.data='):
                    path = line.split('=', 1)[1].strip()
                    log('Current location: {0}'.format(path))
                    return path
        else:
            log('xbmc_env.properties file does not exist')
    except Exception as e:
        log('Error reading current location: {0}'.format(str(e)), xbmc.LOGERROR)
    
    return None


def write_env_file(data_path):
    """
    Write the xbmc_env.properties file with the new data location
    """
    try:
        if not data_path.startswith('/'):
            data_path = os.path.join(ROOT_DIR, data_path)
        
        content = 'xbmc.data={0}\n'.format(data_path)
        
        file_handle = xbmcvfs.File(ENV_FILE_PATH, 'w')
        file_handle.write(content)
        file_handle.close()
        
        log('Successfully wrote xbmc_env.properties with path: {0}'.format(data_path))
        return True
    except Exception as e:
        log('Error writing xbmc_env.properties: {0}'.format(str(e)), xbmc.LOGERROR)
        return False


def get_directory_name_from_keyboard():
    """
    Show keyboard input to get a directory name from the user
    Returns the directory name or None if cancelled
    """
    try:
        keyboard = xbmc.Keyboard('', 'Enter directory name')
        keyboard.doModal()
        
        if keyboard.isConfirmed():
            directory_name = keyboard.getText().strip()
            if directory_name:
                log('User entered directory name: {0}'.format(directory_name))
                return directory_name
        
        log('User cancelled directory name input')
        return None
    except Exception as e:
        log('Error in get_directory_name_from_keyboard: {0}'.format(str(e)), xbmc.LOGERROR)
        return None


def create_new_build_directory(directory_name):
    """
    Create a new directory with .kodi subfolder inside
    Returns the directory name if successful, None otherwise
    """
    try:
        # Sanitize directory name (remove problematic characters)
        directory_name = directory_name.replace('/', '_').replace('\\', '_').strip()
        
        if not directory_name:
            xbmcgui.Dialog().ok(
                ADDON_NAME,
                'Invalid directory name',
                'Please enter a valid directory name.'
            )
            return None
        
        new_dir_path = os.path.join(ROOT_DIR, directory_name)
        kodi_subdir_path = os.path.join(new_dir_path, '.kodi')
        
        # Check if directory already exists
        if xbmcvfs.exists(new_dir_path):
            xbmcgui.Dialog().ok(
                ADDON_NAME,
                'Directory already exists',
                'A directory named "{0}" already exists.'.format(directory_name)
            )
            return None
        
        # Create the main directory
        try:
            xbmcvfs.mkdirs(new_dir_path)
            log('Created directory: {0}'.format(new_dir_path))
        except Exception as e:
            log('Error creating directory: {0}'.format(str(e)), xbmc.LOGERROR)
            xbmcgui.Dialog().ok(
                ADDON_NAME,
                'Failed to create directory',
                'Error: {0}'.format(str(e))
            )
            return None
        
        # Create the .kodi subdirectory
        try:
            xbmcvfs.mkdirs(kodi_subdir_path)
            log('Created .kodi subdirectory: {0}'.format(kodi_subdir_path))
        except Exception as e:
            log('Error creating .kodi subdirectory: {0}'.format(str(e)), xbmc.LOGERROR)
            xbmcgui.Dialog().ok(
                ADDON_NAME,
                'Failed to create .kodi subdirectory',
                'Directory created but .kodi subdirectory failed: {0}'.format(str(e))
            )
            return None
        
        log('Successfully created build directory: {0}'.format(directory_name))
        return directory_name
    except Exception as e:
        log('Error in create_new_build_directory: {0}'.format(str(e)), xbmc.LOGERROR)
        xbmcgui.Dialog().ok(
            ADDON_NAME,
            'Error creating build directory',
            str(e)
        )
        return None


def show_build_selector():
    """
    Display a dialog with available Kodi builds and allow user to select one
    """
    try:
        kodi_dirs = get_kodi_directories()
        
        current_location = get_current_location()
        current_dir = None
        if current_location:
            current_dir = os.path.basename(current_location.rstrip('/'))
        
        display_list = []
        for directory in kodi_dirs:
            if directory == current_dir:
                display_list.append('[CURRENT] {0}'.format(directory))
            else:
                display_list.append(directory)
        
        # Add "Create New Build" option at the bottom
        display_list.append('+ Create New Build')
        
        if not display_list or (len(display_list) == 1 and display_list[0] == '+ Create New Build'):
            # Only create option available
            dialog = xbmcgui.Dialog()
            selected_index = dialog.select(
                '{0} - Select Build'.format(ADDON_NAME),
                display_list
            )
            
            if selected_index >= 0:
                if selected_index == len(display_list) - 1:
                    return 'CREATE_NEW'
            return None
        else:
            dialog = xbmcgui.Dialog()
            selected_index = dialog.select(
                '{0} - Select Build'.format(ADDON_NAME),
                display_list
            )
            
            if selected_index >= 0:
                # Check if user selected "Create New Build"
                if selected_index == len(display_list) - 1:
                    return 'CREATE_NEW'
                else:
                    selected_dir = kodi_dirs[selected_index]
                    log('User selected: {0}'.format(selected_dir))
                    return selected_dir
        
        return None
    except Exception as e:
        log('Error in show_build_selector: {0}'.format(str(e)), xbmc.LOGERROR)
        xbmcgui.Dialog().ok(
            ADDON_NAME,
            'Error showing build selector',
            str(e)
        )
        return None


def confirm_switch(build_name):
    """
    Ask user to confirm the switch
    """
    try:
        dialog = xbmcgui.Dialog()
        message = (
            'Switch to build: {0}?\n\n'
            'Kodi will quit immediately after switching.\n\n'
            'Continue?'
        ).format(build_name)
        
        return dialog.yesno(ADDON_NAME, message)
    except Exception as e:
        log('Error in confirm_switch: {0}'.format(str(e)), xbmc.LOGERROR)
        return False


def show_quit_method_selector():
    """
    Display a dialog to choose quit method
    Returns: 'force' for force quit, 'regular' for regular quit, None if cancelled
    """
    try:
        dialog = xbmcgui.Dialog()
        
        options = [
            'Force Quit & Auto-Restart (Recommended)',
            'Regular Quit (Manual Restart Required)'
        ]
        
        selected_index = dialog.select(
            '{0} - Select Quit Method'.format(ADDON_NAME),
            options
        )
        
        if selected_index == 0:
            dialog.ok(
                ADDON_NAME,
                'Force Quit Selected\n\nKodi will attempt to force-stop and automatically restart.\n\nIf automatic restart fails, please manually restart Kodi from your launcher.'
            )
            log('User selected: Force Quit')
            return 'force'
        elif selected_index == 1:
            dialog.ok(
                ADDON_NAME,
                'Regular Quit Selected\n\nKodi will exit normally.\n\nYou MUST manually close Kodi completely and restart it for the build switch to take effect.'
            )
            log('User selected: Regular Quit')
            return 'regular'
        else:
            log('User cancelled quit method selection')
            return None
    except Exception as e:
        log('Error in show_quit_method_selector: {0}'.format(str(e)), xbmc.LOGERROR)
        try:
            xbmcgui.Dialog().ok(
                ADDON_NAME,
                'Error showing quit method selector',
                str(e)
            )
        except:
            pass
        return None


def force_quit_kodi():
    """
    Force quit Kodi application
    On Android, we need to kill the process for xbmc_env.properties to take effect
    """
    log('Force quitting Kodi application')
    
    try:
        subprocess.call(['am', 'force-stop', 'org.xbmc.kodi'])
        log('Sent force-stop command via am')
    except Exception as e:
        log(f'Failed to force-stop via am: {str(e)}', xbmc.LOGERROR)
    
    try:
        result = subprocess.check_output(['pidof', 'org.xbmc.kodi'])
        pid = result.decode('utf-8').strip()
        if pid:
            subprocess.call(['kill', '-9', pid])
            log(f'Killed process {pid}')
    except Exception as e:
        log(f'Failed to kill process: {str(e)}', xbmc.LOGERROR)
    
    try:
        xbmc.executebuiltin('ShutDown()')
        log('Sent ShutDown command')
    except Exception as e:
        log(f'Failed to execute ShutDown: {str(e)}', xbmc.LOGERROR)
    
    try:
        xbmc.executebuiltin('Quit()')
        log('Sent Quit command')
    except Exception as e:
        log(f'Failed to execute Quit: {str(e)}', xbmc.LOGERROR)


def main():
    """
    Main addon logic
    """
    log('Build Switcher addon started')
    
    try:
        selected_build = show_build_selector()
        
        if selected_build is None:
            log('No build selected, exiting')
            return
        
        # Handle new build creation
        if selected_build == 'CREATE_NEW':
            log('User selected to create new build')
            
            directory_name = get_directory_name_from_keyboard()
            if directory_name is None:
                log('User cancelled directory name input')
                return
            
            created_build = create_new_build_directory(directory_name)
            if created_build is None:
                log('Failed to create build directory')
                return
            
            selected_build = created_build
            log('Created new build: {0}'.format(created_build))
        
        if not confirm_switch(selected_build):
            log('User cancelled switch')
            return
        
        build_path = os.path.join(ROOT_DIR, selected_build)
        
        if write_env_file(build_path):
            xbmcgui.Dialog().notification(
                ADDON_NAME,
                'Switched to: {0}\nKodi will now quit'.format(selected_build),
                xbmcgui.NOTIFICATION_INFO,
                3000
            )
            
            log('Build switch completed successfully. Quitting Kodi...')
            
            xbmc.sleep(3000)
            
            xbmc.executebuiltin("Quit")
        else:
            xbmcgui.Dialog().ok(
                ADDON_NAME,
                'Error\n\nFailed to write xbmc_env.properties file.\nPlease check permissions and try again.'
            )
    except Exception as e:
        log('Error in main: {0}'.format(str(e)), xbmc.LOGERROR)
        try:
            xbmcgui.Dialog().ok(
                ADDON_NAME,
                'Unexpected Error',
                str(e)
            )
        except:
            pass


if __name__ == '__main__':
    main()