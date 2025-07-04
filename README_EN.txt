* README_EN.txt
* 2025.06.29
* contools--notepadplusplus

1. DESCRIPTION
2. LICENSE
3. REPOSITORIES
5. DISTRIBUTION
6. INSTALLATION
7. SCRIPTS
8. USAGE
9. SHORTCUTS
10. AUTHOR

-------------------------------------------------------------------------------
1. DESCRIPTION
-------------------------------------------------------------------------------
Set of scripts for the Notepad++ Python Script plugin.

-------------------------------------------------------------------------------
2. LICENSE
-------------------------------------------------------------------------------
The MIT license (see included text file "license.txt" or
https://en.wikipedia.org/wiki/MIT_License)

-------------------------------------------------------------------------------
3. REPOSITORIES
-------------------------------------------------------------------------------
Primary:
  * https://github.com/andry81/contools--notepadplusplus/branches
    https://github.com/andry81/contools--notepadplusplus.git
First mirror:
  * https://sf.net/p/contools/contools--notepadplusplus/ci/master/tree
    https://git.code.sf.net/p/contools/contools--notepadplusplus
Second mirror:
  * https://gitlab.com/andry81/contools-notepadplusplus/-/branches
    https://gitlab.com/andry81/contools-notepadplusplus.git

-------------------------------------------------------------------------------
5. DISTRIBUTION
-------------------------------------------------------------------------------
Catalog of applications, tools, modules and files included in the distribution:

  * Python scripts for Notepad++ PythonScript plugin using from `tacklebar`
    project.

  * List files for Notepad++ MultiReplace plugin using from Notepad++.

-------------------------------------------------------------------------------
6. INSTALLATION
-------------------------------------------------------------------------------

1. Install `PythonScript` plugin within the Notepad++ `Plugins` menu item or
   download the installer from:
     https://github.com/bruderstein/PythonScript/releases

2. Copy scripts into `scripts` sub directory inside the Notepad++ directory:
   `../plugins/Config/PythonScript`.

3. Change the initialization item from the PythonScript configuration menu
   item: `Plugins->Python Scripts->Configuration...`:
   From `LAZY` to `ATSTARTUP`

Now each time when the Notepad++ starts it will call to `startup.py` script.

-------------------------------------------------------------------------------
7. SCRIPTS
-------------------------------------------------------------------------------
* `/scripts/python/tacklebar/libs/npplib.py`

  Main library script.

* `/scripts/python/tacklebar/open_new_*_from_current_tab_text_as_file_path_list.py`

  Scripts to search the current tab text for file paths and open them.

* `/scripts/python/tacklebar/reopen_all_*files*.py`

  Scripts to workaround the Notepad++ bug:
    `[Feature Request] Language auto detection from simplified session file`:
    https://github.com/notepad-plus-plus/notepad-plus-plus/issues/5844

* `/scripts/python/tacklebar/close_all_saved_files_*.py`
  `/scripts/python/tacklebar/close_all_not_altered_files_*.py`

  Scripts to safely close all saved or not altered files.

* `/scripts/python/tacklebar/reactivate_all_files_*.py`

  Scripts to reactivate all opened files in forward or reversed order.

* `/scripts/python/tacklebar/toggle_readonly_flag_for_all_tabs.py`

  Script to toggle the inner Read-Only flag for all tabs (in the Notepad++).

* `/scripts/python/tacklebar/clear_readonly_flag_from_all_files.py`

  Script to clear the Read-Only flag from all opened tab files in the file
  system.

* `/scripts/python/tacklebar/undo_all_files.py`
  `/scripts/python/tacklebar/redo_all_files.py`

  Script to undo/redo the history for all opened tab files.
  Useful to undo/redo the replacement action after the `Find and Replace`
  dialog in all opened file tabs.

  Available shortcut to use:
    * Undo: CTRL+ALT-Z (`CTRL-SHIFT-Z` is reserved for the redo)
    * Redo: CTRL+ALT-Y

  CAUTION:
    Script does undo/redo for ALL tabs, even for those, where the action is not
    needed to be done. So it can undo/redo not the last/first the
    `Find and Replace` dialog replacement.
    To avoid the issue you have to open a standalone Notepad++ instance to
    undo/redo only a required set of tabs.

* `/scripts/python/tacklebar/close_all_npp_windows.py`

  Script to close all Notepad++ windows including current process instance.

* `/scripts/python/startup.py` -

  Sript to call upon the Notepad++ instance launch.

-------------------------------------------------------------------------------
8. USAGE
-------------------------------------------------------------------------------
Basically, `startup.py` will automatically call upon start of each Notepad++
instance.
All other scripts can be directly used from the Notepad++ Plugins menu.

Examples of the Notepad++ extra command line:

>
notepad++.exe -nosession -multiInst -z -from_utf16 -z --open_from_file_list -z "<utf-16-with-bom-paths-list-file>"

>
notepad++.exe -nosession -multiInst -z -from_utf16le -z --open_from_file_list -z "<utf-16le-without-bom-paths-list-file>"

Additional command line arguments:

`-z --remove_file_list_after_open`

  Remove the file list after all paths from it is opened.

`-z --open_short_path_if_gt_limit -z 258`

  Translates each path into a short DOS path if greater than the limit.
  Can workaround long path files open, which Notepad++ does not support.

  See the related long path issue:
    `Can not open long path files` :
    https://github.com/notepad-plus-plus/notepad-plus-plus/issues/9181

  NOTE:
    The Short File Names (SFN) generation must be explicitly enabled in the
    Windows file system before a file or a directory creation.
    See the `fsutil 8dot3name ...` command for the details.

`-z -append`

  Append mode.
  Runs Notepad++ instance to either open the files from a list in place or
  delegate files to open them in an already running Notepad++ process.
  If a Notepad++ instance already has been running and has no `-multiInst`
  parameter on the command line (shared instance), then the files delegates to
  open into that instance. After that the being launched instance does auto
  close.
  If there is no Notepad++ instance without `-multiInst` parameter on the
  command line (not shared instance), then the files does open in place.

`-z -restore_if_open_inplace`

  Has meaning in the append mode.
  If there were no shared instances without `-multiInst` on the command line,
  then the Notepad++ does restore the window show state (unminimizes) before
  open in place.
  Useful in case when the user want to hide the window blinking.

`-z --child_cmdline_len_limit -z 4096`

  Has meaning in the append mode and if `-z -append_by_child_instance` is used.
  Reduces the maximum command line length limit per child instance which is
  32767 as by default.
  In case of a delegated open the launched Notepad++ instance builds each
  command line until this limit and only after runs it.
  To append each file by a separate child Notepad++ process you can set it to
  1.

`-z -append_by_child_instance`

  Has meaning in the append mode.
  By default file open delegation made through the `WM_COPYDATA` +
  `COPYDATA_FILENAMESW` message as a most reliable. To replace it by a child
  process method use this option.

`-z -no_activate_after_append`

  Does not activate the Notepad++ instance main window in case of delegated
  open in the append mode.
  Useful to avoid window focus change after append.

`-z -no_exit_after_append`

  Does not auto close the launched Notepad++ instance in case of delegated open
  in the append mode.
  Useful to debug the launched instance on the Python errors from the builtin
  console.

For the rest options see the `npplib.py` script file.

-------------------------------------------------------------------------------
9. SHORTCUTS
-------------------------------------------------------------------------------
The Notepad++ has no functionality to add a shortcut at the moment and only
can modify the existing one.
You can use a plugin to add the functionality. The `PythonScript` plugin still
can do this.

See details:
  https://community.notepad-plus-plus.org/post/28150
  https://community.notepad-plus-plus.org/topic/14703/run-python-script-pythonscript-plugin-with-a-shortcut/3

NOTE:
  You must restart the Notepad++ to apply the modified shortcuts in the
  Shortcut Mapper.

-------------------------------------------------------------------------------
10. AUTHOR
-------------------------------------------------------------------------------
Andrey Dibrov (andry at inbox dot ru)
