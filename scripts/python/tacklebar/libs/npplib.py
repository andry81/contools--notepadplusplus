from __future__ import print_function

def toggle_readonly_flag_for_all_tabs():
  print('toggle_readonly_flag_for_all_tabs:')

  all_files = notepad.getFiles()
  active_file = notepad.getCurrentFilename()

  num_toggled = 0
  file_index = len(all_files)

  for f in reversed(all_files):
    file_index -= 1
    print('  [{}] {}'.format(file_index, f))
    notepad.activateFile(f[0])
    notepad.menuCommand(MENUCOMMAND.EDIT_SETREADONLY)
    num_toggled += 1

  notepad.activateFile(active_file)

  print()
  print('* Number of toggled paths: '+ str(num_toggled))
  print()

def clear_readonly_flag_from_all_files():
  print('clear_readonly_flag_from_all_files:')

  all_files = notepad.getFiles()
  active_file = notepad.getCurrentFilename()

  num_cleared = 0
  file_index = len(all_files)

  for f in reversed(all_files):
    file_index -= 1
    print('  [{}] {}'.format(file_index, f))
    notepad.activateFile(f[0])
    notepad.menuCommand(MENUCOMMAND.EDIT_CLEARREADONLY)
    num_cleared += 1

  notepad.activateFile(active_file)

  print()
  print('* Number of cleared paths: ' + str(num_cleared))
  print()

def reactivate_all_files(reactivate_reversed = True, reactive_current_at_last = False):
  print('reactivate_all_files:')
  print('  - reactivate_reversed: ' + str(reactivate_reversed))

  all_files = list(notepad.getFiles())
  active_file = notepad.getCurrentFilename()

  num_reopened = 0

  if reactivate_reversed:
    for f in reversed(all_files):
      notepad.activateFile(f[0])
      num_reopened += 1
  else:
    for f in all_files:
      notepad.activateFile(f[0])
      num_reopened += 1

  if reactive_current_at_last:
    notepad.activateFile(active_file)

  print()
  print('* Number of activated paths: ' + str(num_reopened))
  print()

# NOTE:
#   `reactivate_reversed = False` - DOES NOT change activation order
#   `allow_unsaved = True` - where has an unsaved modification
#   `allow_edited = True` - where an undo or redo list is not empty
#
def reopen_all_files(reactivate_reversed = True, allow_unsaved = False, allow_edited = False):
  print('reopen_all_files:')
  print('  - reactivate_reversed: ' + str(reactivate_reversed))
  print('  - allow_unsaved:       ' + str(allow_unsaved))
  print('  - allow_edited:        ' + str(allow_edited))

  all_files = list(notepad.getFiles())
  active_file = notepad.getCurrentFilename()

  if (allow_unsaved and allow_edited):
    notepad.saveAllFiles()
    notepad.closeAll()

  num_reopened = 0
  num_skipped = 0
  file_index = 0

  if (allow_unsaved and allow_edited):
    for f in all_files:
      print('  [{}] {}'.format(file_index, f[0]))
      notepad.open(f[0])
      num_reopened += 1
      file_index += 1
  else:
    # loop with tabs reactivation to call functions
    for f in all_files:
      notepad.activateFile(f[0])
      is_unsaved = editor.getModify()
      can_undo = editor.canUndo()
      can_redo = editor.canRedo()
      if (allow_unsaved or not is_unsaved) and (allow_edited or (not can_undo and not can_redo)):
        print('  [{}] (reopened)        {}'.format(file_index, f[0]))
        notepad.close()
        notepad.open(f[0])
        num_reopened += 1
      else:
        print('  [{}] {}{}{}'.format(file_index,
          ('[unsaved]' if is_unsaved else '         ') + ('[edited]' if can_undo or can_redo else '        '),
          ' ' if is_unsaved or can_undo or can_redo else '', f[0])) 
        num_skipped += 1

      file_index += 1

  if (allow_unsaved and allow_edited):
    if reactivate_reversed:
      for f in reversed(all_files):
        notepad.activateFile(f[0])
  else:
    # have to reactivate again
    all_files = list(notepad.getFiles())

    if not reactivate_reversed:
      for f in all_files:
        notepad.activateFile(f[0])
    else:
      for f in reversed(all_files):
        notepad.activateFile(f[0])

  notepad.activateFile(active_file)

  print()
  print('* Number of reopened paths: ' + str(num_reopened))
  print('* Number of skipped paths:  ' + str(num_skipped))
  print()

# not altered - not modified (but may be saved) and not edited
def reopen_all_not_altered_files(reactivate_reversed = True):
  return reopen_all_files(reactivate_reversed, False, False)

# can be edited
def reopen_all_saved_files(reactivate_reversed = True):
  return reopen_all_files(reactivate_reversed, False, True)

def close_all_files(reactivate_reversed = True, allow_unsaved = False, allow_edited = False):
  print('close_all_files:')
  print('  - reactivate_reversed: ' + str(reactivate_reversed))
  print('  - allow_unsaved:       ' + str(allow_unsaved))
  print('  - allow_edited:        ' + str(allow_edited))

  all_files = list(notepad.getFiles())
  active_file = notepad.getCurrentFilename()

  num_closed = 0
  num_skipped = 0
  file_index = 0

  for f in all_files:
    notepad.activateFile(f[0])
    is_unsaved = editor.getModify()
    can_undo = editor.canUndo()
    can_redo = editor.canRedo()
    if (allow_unsaved or not is_unsaved) and (allow_edited or (not can_undo and not can_redo)):
      print('  [{}] (closed)          {}'.format(file_index, f[0]))
      notepad.close()
      num_closed += 1
    else:
      print('  [{}] {}{}{}'.format(file_index,
        ('[unsaved]' if is_unsaved else '         ') + ('[edited]' if can_undo or can_redo else '        '),
        ' ' if is_unsaved or can_undo or can_redo else '', f[0])) 
      num_skipped += 1

    file_index += 1

  # have to reactivate again
  all_files = list(notepad.getFiles())

  if not reactivate_reversed:
    for f in all_files:
      notepad.activateFile(f[0])
  else:
    for f in reversed(all_files):
      notepad.activateFile(f[0])

  notepad.activateFile(active_file)

  print()
  print('* Number of closed paths:  ' + str(num_closed))
  print('* Number of skipped paths: ' + str(num_skipped))
  print()

# not altered - not modified (but may be saved) and not edited
def close_all_not_altered_files(reactivate_reversed = True):
  return close_all_files(reactivate_reversed, False, False)

# files can be edited
def close_all_saved_files(reactivate_reversed = True):
  return close_all_files(reactivate_reversed, False, True)

def undo_all_files(reversed_order = True):
  print('undo_all_files:')
  print('  - reversed_order: ' + str(reversed_order))

  all_files = list(notepad.getFiles())
  active_file = notepad.getCurrentFilename()

  num_undo = 0

  if reversed_order:
    for f in reversed(all_files):
      notepad.activateFile(f[0])
      if editor.canUndo():
        print('  [{}] {}'.format(num_undo, f[0]))
        editor.undo()
        num_undo += 1
  else:
    for f in all_files:
      notepad.activateFile(f[0])
      if editor.canUndo():
        print('  [{}] {}'.format(num_undo, f[0]))
        editor.undo()
        num_undo += 1

  notepad.activateFile(active_file)

  print()
  print('* Number of undo paths: ' + str(num_undo))
  print()

def redo_all_files(reversed_order = True):
  print('redo_all_files:')
  print('  - reversed_order: ' + str(reversed_order))

  all_files = list(notepad.getFiles())
  active_file = notepad.getCurrentFilename()

  num_redo = 0

  if reversed_order:
    for f in reversed(all_files):
      notepad.activateFile(f[0])
      if editor.canRedo():
        print('  [{}] {}'.format(num_redo, f[0]))
        editor.redo()
        num_redo += 1
  else:
    for f in all_files:
      notepad.activateFile(f[0])
      if editor.canRedo():
        print('  [{}] {}'.format(num_redo, f[0]))
        editor.redo()
        num_redo += 1

  notepad.activateFile(active_file)

  print()
  print('* Number of redo paths: ' + str(num_redo))
  print()

class EnumNppWindows:
  notepadpp_hwnd = None
  not_multiinst_wnd_list = [] # list of Notepad++ instances w/o `-multiInst` option
  not_multiinst_pid_list = []
  multiinst_wnd_list = []     # list of Notepad++ instances w/ `-multiInst` option
  multiinst_pid_list = []

def enum_notepadpp_windows(enum_npp_windows_out):
  import ctypes
  from ctypes import wintypes
  import psutil, os

  class InParams:
    current_pid = 0

  kernel32 = ctypes.windll.kernel32
  user32 = ctypes.windll.user32

  WNDENUMPROC = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)
  SW_RESTORE = wintypes.DWORD(9)

  kernel32.GetCurrentProcessId.restype = wintypes.DWORD
  kernel32.GetCurrentProcessId.argtypes = []

  user32.EnumWindows.restype = wintypes.BOOL
  user32.EnumWindows.argtypes = [
    WNDENUMPROC,      # [in] WNDENUMPROC lpEnumFunc,
    wintypes.LPARAM   # [in] LPARAM      lParam
  ]

  user32.GetClassNameW.restype = ctypes.c_int
  user32.GetClassNameW.argtypes = [
    wintypes.HWND,    # [in]  HWND   hWnd,
    wintypes.LPWSTR,  # [out] LPWSTR lpClassName,
    ctypes.c_int      # [in]  int    nMaxCount
  ]

  in_params = InParams()

  in_params.current_pid = kernel32.GetCurrentProcessId()
  process_id = wintypes.DWORD()

  wnd_class_name_buf_size = 256
  wnd_class_name_buf = ctypes.create_unicode_buffer(256)

  def enum_notepadpp_windows(hwnd, lparam):
    user32.GetClassNameW(hwnd, wnd_class_name_buf, wnd_class_name_buf_size)
    #wnd_class_name_buf[255] = 0 # string terminator character in case of truncation
    if u'Notepad++' in wnd_class_name_buf.value:
      user32.GetWindowThreadProcessId(hwnd, ctypes.byref(process_id))
      if process_id.value == in_params.current_pid:
        enum_npp_windows_out.notepadpp_hwnd = hwnd
      else:
        cmdline_list = psutil.Process(process_id.value).cmdline()

        is_not_multi_instance = True
        next_arg_ignore = False

        # filter out all `-z` parameters to leave only Notepad++ builtin parameters except several specific
        for arg in cmdline_list:
          if next_arg_ignore:
            next_arg_ignore = False
            continue

          if arg == '-z':
            next_arg_ignore = True
            continue

          if arg == '-multiInst':
            is_not_multi_instance = False
            break

        if is_not_multi_instance:
          enum_npp_windows_out.not_multiinst_wnd_list.append(hwnd)
          enum_npp_windows_out.not_multiinst_pid_list.append(process_id.value)
        else:
          enum_npp_windows_out.multiinst_wnd_list.append(hwnd)
          enum_npp_windows_out.multiinst_pid_list.append(process_id.value)

    return True # continue enumerating

  user32.EnumWindows(WNDENUMPROC(enum_notepadpp_windows), 0)

  print('enum_notepadpp_windows:')
  print('  - pid: ' + str(in_params.current_pid))
  print('  - not multi (shared) instances: ' + str(enum_npp_windows_out.not_multiinst_pid_list))
  print('  - multi (not shared) instances: ' + str(enum_npp_windows_out.multiinst_pid_list))

def process_extra_command_line():
  import ctypes
  from ctypes import wintypes
  import sys, os, io, shlex

  print('process_extra_command_line:')

  cmdline_list = shlex.split(notepad.getCommandLine())

  from_utf8 = False
  from_utf16 = False
  from_utf16le = False
  from_utf16be = False

  open_from_file_list_path = ''
  next_arg_is_file_list_path = False

  open_path_len_limit = 0 # open as is
  next_arg_is_open_path_limit = False

  child_cmdline_len_limit = 32767 # use default limit - 32767
  next_arg_is_child_cmdline_len_limit = False

  chdir_path = ''
  next_arg_is_chdir_path = False

  do_append = False
  do_append_by_child_instance = False
  do_reopen_all_files = False
  allow_reopen_unsaved_files = False
  allow_reopen_edited_files = False # can undo or redo
  do_restore_if_open_inplace = False

  is_multi_instance = False

  no_activate_after_append = False
  no_exit_after_append = False

  is_launcher = False

  # to debug purposes
  is_debug = False

  for arg in cmdline_list:
    if arg == '-z':
      continue

    if next_arg_is_file_list_path:
      open_from_file_list_path = str(arg)
      next_arg_is_file_list_path = False
    elif next_arg_is_chdir_path:
      chdir_path = str(arg)
      next_arg_is_chdir_path = False
    elif next_arg_is_open_path_limit:
      open_path_len_limit = max(int(arg), 255) # 255 is builtin minimum
      next_arg_is_open_path_limit = False
      print('--open_short_path_if_gt_limit ' + str(open_path_len_limit))
    elif next_arg_is_child_cmdline_len_limit:
      # 1 is builtin minimum, means: use one file to open per each child Notepad++ command line
      # 32767 is builtin maximum for Win32 CreateProcess
      child_cmdline_len_limit = min(max(int(arg), 1), 32767)
      next_arg_is_child_cmdline_len_limit = False
      print('--child_cmdline_len_limit ' + str(child_cmdline_len_limit))
    else:
      if arg == '-from_utf8':
        from_utf8 = True
      elif arg == '-from_utf16':
        from_utf16 = True
      elif arg == '-from_utf16le':
        from_utf16le = True
      elif arg == '-from_utf16be':
        from_utf16be = True
      elif arg == '--open_from_file_list':
        next_arg_is_file_list_path = True
      elif arg == '--open_short_path_if_gt_limit':
        next_arg_is_open_path_limit = True
      elif arg == '--child_cmdline_len_limit':
        next_arg_is_child_cmdline_len_limit = True
      elif arg == '--chdir':
        next_arg_is_chdir_path = True
      elif arg == '-reopen_all_files':
        do_reopen_all_files = True
      elif arg == '-allow_reopen_unsaved_files':
        allow_reopen_unsaved_files = True
      elif arg == '-allow_reopen_edited_files':
        allow_reopen_edited_files = True
      elif arg == '-restore_if_open_inplace':
        do_restore_if_open_inplace = True
      elif arg == '-append':
        do_append = True
      elif arg == '-append_by_child_instance':
        do_append_by_child_instance = True
      elif arg == '-multiInst':
        is_multi_instance = True
      elif arg == '-no_activate_after_append':
        no_activate_after_append = True
      elif arg == '-no_exit_after_append':
        no_exit_after_append = True
      elif arg == '-launcher':
        is_launcher = True
      elif arg == '-debug':
        is_debug = True

  #if is_debug:
  #  pass

  #if is_launcher:
  #  pass

  # append and restore has meaning ONLY in multi-instance mode
  if not is_multi_instance:
    do_append = False
    do_restore_if_open_inplace = False
  # restore has meaning ONLY in the minimized show state used in the append mode
  elif not do_append:
    do_restore_if_open_inplace = False

  num_processed_paths = 0
  num_success_paths = 0

  # True - open files in current Notepad++ instance
  # False - open file in another Notepad++ instance
  do_open_inplace = True

  if chdir_path:
    os.chdir(chdir_path)
    print('--chdir: ' + chdir_path)

  if open_from_file_list_path:
    if do_append or open_path_len_limit > 0:
      import ctypes
      from ctypes import wintypes

    # construct child command line
    if do_append:
      enum_npp_windows = EnumNppWindows()

      # enumerate Notepad++ instances as standalone windows
      enum_notepadpp_windows(enum_npp_windows)

      if do_restore_if_open_inplace:
        if enum_npp_windows.notepadpp_hwnd and not len(enum_npp_windows.not_multiinst_pid_list): # open inplace
          print('  - instance restored')
          user32.ShowWindow(enum_npp_windows.notepadpp_hwnd, SW_RESTORE)
        else:
          print('  - instance NOT restored')

      if len(enum_npp_windows.not_multiinst_pid_list):
        do_open_inplace = False

        append_cmdline_file_list = list()

        if do_append_by_child_instance:
          # prepare child Notepad++ command line to pass all being opened files into it to append to existing Notepad++ instance (except this instance)
          child_cmdline_prefix_list = list()

          next_arg_ignore = False

          # filter out all `-z` parameters to leave only Notepad++ builtin parameters except several specific
          for arg in cmdline_list:
            if next_arg_ignore:
              next_arg_ignore = False
              continue

            if arg == '-z':
              next_arg_ignore = True
              continue

            if next_arg_is_file_list_path:
              open_from_file_list_path = str(arg)
              next_arg_is_file_list_path = False
            elif next_arg_is_chdir_path:
              chdir_path = str(arg)
              next_arg_is_chdir_path = False
            elif next_arg_is_open_path_limit:
              open_path_len_limit = max(int(arg), 255) # 255 is builtin minimum
              next_arg_is_open_path_limit = False
              print('--open_short_path_if_gt_limit ' + str(open_path_len_limit))
            else:
              if arg == '-nosession':
                continue
              if arg == '-multiInst':
                continue

              child_cmdline_prefix_list.append(arg)

    print('--open_from_file_list:')

    with open(open_from_file_list_path, 'rb') as file_list: # CAUTION: binary mode is required to correctly decode string into `utf-8` below
      file_content = file_list.read()

    # CAUTION:
    #   Do decode with explicitly stated encoding to avoid the error:
    #   `UnicodeDecodeError: 'charmap' codec can't decode byte ... in position ...: character maps to <undefined>`
    #   (see details: https://stackoverflow.com/questions/27453879/unicode-decode-error-how-to-skip-invalid-characters/27454001#27454001 )
    #
    recode_to_utf8 = False
    if from_utf8:
      file_content_decoded = file_content.decode('utf-8', errors = 'ignore')
      recode_to_utf8 = True
    elif from_utf16:
      file_content_decoded = file_content.decode('utf-16', errors = 'ignore')
      recode_to_utf8 = True
    elif from_utf16le:
      file_content_decoded = file_content.decode('utf-16-le', errors = 'ignore')
      recode_to_utf8 = True
    elif from_utf16be:
      file_content_decoded = file_content.decode('utf-16-be', errors = 'ignore')
      recode_to_utf8 = True
    else:
      file_content_decoded = file_content

    # To iterate over lines instead chars.
    # (see details: https://stackoverflow.com/questions/3054604/iterate-over-the-lines-of-a-string/3054898#3054898 )
    file_strings = io.StringIO(file_content_decoded)

    # CAUTION:
    #   The `win32api.GetShortPathName` awaits ascii format and unicode variant is not implemented in Python 2.7.
    #   So we must use `ctype` module to directly call `GetShortPathNameW` instead.
    #
    #   For details:
    #     https://mail.python.org/pipermail/python-win32/2006-May/004697.html
    #
    #        John Machin irta:
    #     >     According to my reading of the source, the function you have called
    #     >     expects an 8-bit string.
    #     >     ====
    #     >     static PyObject *
    #     >     PyGetShortPathName(PyObject * self, PyObject * args)
    #     >     {
    #     >         char *path;
    #     >         if (!PyArg_ParseTuple(args, "s:GetShortPathName", &path))
    #     >     ====
    #     >     If it is given Unicode, PyArg_ParseTuple will attempt to encode it
    #     >     using the default encoding (ascii). Splat.
    #     >
    #     >     Looks like you need a GetShortPathNameW() but it's not implemented.
    #     >     ...
    #     >
    #     >     Another thought: try using ctypes.
    #     >

    file_path_unc_prefix = u'\\\\?\\' # a constant

    if open_path_len_limit > 0:
      kernel32 = ctypes.windll.kernel32

      kernel32.GetShortPathNameW.restype = wintypes.DWORD
      kernel32.GetShortPathNameW.argtypes = [
          wintypes.LPCWSTR,# [in]  LPCWSTR lpszLongPath,
          wintypes.LPWSTR, # [out] LPWSTR  lpszShortPath,
          wintypes.DWORD   # [in]  DWORD   cchBuffer
      ]

    for line in file_strings:
      file_path = line.strip()
      if file_path:
        file_path_decoded = file_path
        # python 2 only
        if sys.version_info[0] < 3:
          if recode_to_utf8:
            file_path = file_path_decoded.encode('utf-8', errors = 'ignore')
        print('  [{}] ({}) {}'.format(num_processed_paths, len(file_path), file_path))

        # 0 or >= 255 - builtin minimum
        do_open_as_is = True if not open_path_len_limit or open_path_len_limit >= len(file_path) else False

        if do_open_as_is:
          if do_open_inplace:
            notepad.open(file_path)

            if notepad.getCurrentFilename() == file_path:
              num_success_paths += 1
            else:
              print("    - error: path is not opened.")
          else:
            append_cmdline_file_list.append(file_path)
            num_success_paths += 1
        else:
          file_path_unc = file_path_unc_prefix + file_path_decoded

          file_path_short_buf_size = len(file_path_unc) + 1 # in characters
          file_path_short_buf = ctypes.create_unicode_buffer(file_path_short_buf_size) # plus terminator character

          if kernel32.GetShortPathNameW(file_path_unc, file_path_short_buf, file_path_short_buf_size):
            file_path = str(file_path_short_buf.value)

            print('    - ({}) {}'.format(len(file_path), file_path))

            if do_open_inplace:
              notepad.open(str(file_path_short_buf.value))

              if notepad.getCurrentFilename() == file_path:
                num_success_paths += 1
              else:
                print("    - error: path is not opened.")
            else:
              append_cmdline_file_list.append(str(file_path_short_buf.value))
              num_success_paths += 1
          else:
            print("    - error: path is not opened: `ctypes.windll.kernel32.GetShortPathNameW` call is failed.")

            # fall back to long path
            if do_open_inplace:
              notepad.open(file_path)

              if notepad.getCurrentFilename() == file_path:
                num_success_paths += 1
              else:
                print("    - error: path is not opened.")
            else:
              # ISSUE:
              #   We have to skip append into a child command line, because in that case Notepad++ does not open the entire command line
              #   including not long file path arguments if at least one argument is a long file path!
              #
              #   OS:           Windows 8 x64
              #   Notepad++:    8.5.7 32-bit
              #   PythonScript: 1.5.4.0 32-bit
              #   Python:       2.7.18 32-bit
              #
              #append_cmdline_file_list.append(file_path)
              print("    - error: path is not opened.")

          #file_path_short_buf = None

        num_processed_paths += 1

  print()
  print('* Number of success paths: {} of {}'.format(str(num_success_paths), str(num_processed_paths)))
  print()

  if not do_open_inplace:
    if not do_append_by_child_instance:
      print('sending WM_COPYDATA messages to pid={}:'.format(enum_npp_windows.not_multiinst_pid_list[0]))
    else:
      print('executing child subprocess:')

    if len(append_cmdline_file_list):
      if not do_append_by_child_instance:
        if not hasattr(wintypes, 'LRESULT'):
          wintypes.LRESULT = ctypes.c_ssize_t

        user32 = ctypes.windll.user32

        user32.SendMessageW.restype = wintypes.LRESULT
        user32.SendMessageW.argtypes = [
          wintypes.HWND,    # [in] HWND   hWnd,
          wintypes.UINT,    # [in] UINT   Msg,
          wintypes.WPARAM,  # [in] WPARAM wParam,
          wintypes.LPARAM   # [in] LPARAM lParam
        ]

        WM_COPYDATA = 0x004A
        COPYDATA_FILENAMESW = 2

        if not hasattr(wintypes, 'ULONG_PTR'):
          if ctypes.sizeof(ctypes.c_void_p) == 8:
            wintypes.ULONG_PTR = ctypes.c_ulonglong
          else:
            wintypes.ULONG_PTR = ctypes.c_ulong

        class COPYDATASTRUCT(ctypes.Structure):
          _fields_ = [
            ('dwData', wintypes.ULONG_PTR),
            ('cbData', wintypes.DWORD),
            ('lpData', wintypes.LPVOID)
          ]

        copydata = COPYDATASTRUCT()
        copydata.dwData = COPYDATA_FILENAMESW
      else:
        import subprocess#, time

      # each command line must be not longer than a command line length limit
      cmdline_len_max = child_cmdline_len_limit

      # count accumulated command line length respective to white space characters
      white_space_chars = ' \t'

      if not do_append_by_child_instance:
        # virtual limitation for WM_COPYDATA
        child_subprocess_prefix_cmdline_list = []
      else:
        child_subprocess_prefix_cmdline_list = [sys.argv[0]] + child_cmdline_prefix_list[1:] + ['-nosession', '-noPlugin', '-z', '-launcher']

      def cmdline_len(arg_list):
        cmdline_len = 0
        arg_index = 0

        for arg in arg_list:
          if len(arg):
            if not do_append_by_child_instance:
              # always quoted
              cmdline_len += len(arg) + 2
            else:
              # conditionally quoted
              arg_has_white_space_char = any(elem in arg for elem in white_space_chars)
              cmdline_len += len(arg) + (2 if arg_has_white_space_char else 0)
          else: # empty argument
            cmdline_len += 2

          if arg_index:
            cmdline_len += 1 # space between arguments

          arg_index += 1

        return cmdline_len

      child_subprocess_prefix_cmdline_len = cmdline_len(child_subprocess_prefix_cmdline_list)

      while len(append_cmdline_file_list):
        file_path = append_cmdline_file_list.pop(0)
        file_path_list = [file_path]

        child_cmdline_file_path_list = file_path_list

        child_subprocess_prev_cmdline_len = child_subprocess_prefix_cmdline_len + (1 if child_subprocess_prefix_cmdline_len else 0) + cmdline_len(file_path_list)

        if len(append_cmdline_file_list):
          file_path = append_cmdline_file_list[0]
          file_path_list = [file_path]

          child_subprocess_next_cmdline_len = child_subprocess_prev_cmdline_len + (1 if child_subprocess_prev_cmdline_len else 0) + cmdline_len(file_path_list)

          while cmdline_len_max >= child_subprocess_next_cmdline_len:
            append_cmdline_file_list.pop(0)

            child_cmdline_file_path_list.append(file_path)

            child_subprocess_prev_cmdline_len = child_subprocess_next_cmdline_len

            if len(append_cmdline_file_list):
              file_path = append_cmdline_file_list[0]
              file_path_list = [file_path]

              child_subprocess_next_cmdline_len = child_subprocess_prev_cmdline_len + (1 if child_subprocess_prev_cmdline_len else 0) + cmdline_len(file_path_list)
            else:
              break

        if not do_append_by_child_instance and len(enum_npp_windows.not_multiinst_wnd_list):
          print('  - WM_COPYDATA: ' + str(child_subprocess_prefix_cmdline_list))
          print('    command line length: ' + str(child_subprocess_prev_cmdline_len))

          child_subprocess_prev_cmdline = ''
          file_index = 0

          for file_path in child_cmdline_file_path_list:
            print('    [{}] ({}) {}'.format(file_index, len(file_path), file_path))
            child_subprocess_prev_cmdline += (' ' if len(child_subprocess_prev_cmdline) else '') + '"' + file_path + '"'
            file_index += 1

          child_cmdline_buf = ctypes.create_unicode_buffer(child_subprocess_prev_cmdline) # must be quoted as in the command line

          copydata.cbData = ctypes.sizeof(child_cmdline_buf)
          copydata.lpData = ctypes.cast(child_cmdline_buf, wintypes.LPVOID)

          user32.SendMessageW(enum_npp_windows.not_multiinst_wnd_list[0], WM_COPYDATA,
            enum_npp_windows.notepadpp_hwnd if not enum_npp_windows.notepadpp_hwnd is None else 0, ctypes.addressof(copydata))
        else:
          print('  - ' + str(child_subprocess_prefix_cmdline_list))
          print('    command line length: ' + str(child_subprocess_prev_cmdline_len))

          file_index = 0

          for file_path in child_cmdline_file_path_list:
            print('    [{}] ({}) {}'.format(file_index, len(file_path), file_path))
            file_index += 1

          # ISSUE:
          #   Tests showed random application hang after the `subprocess.call`.
          #
          #   OS:           Windows 8 x64
          #   Notepad++:    8.5.7 32-bit
          #   PythonScript: 1.5.4.0 32-bit
          #   Python:       2.7.18 32-bit
          #
          #   Suggestion:
          #     Child Notepad++ process uses SendMessage to a random Notepad++ instance excluding itself,
          #     when the parent instance is blocked in the main thread by this function call to the parent process.
          #
          #   Workaround:
          #     The asynchronous subprocess call from here as `subprocess.popen` instead of `subprocess.call` is used
          #     to unblock the parent process to handle a child process call and the rest of messages.
          #
          # CAUTION:
          #   DO NOT USE this implementation because of this issue and other issues like wrong
          #   order of messages to process because of an asynchronous child call.
          #   Use direct notification to another instance which does not have has the `-multiInst` in the command line.
          #   This implementation is left as an aternative and the last method.
          #
          subprocess.Popen(child_subprocess_prefix_cmdline_list + child_cmdline_file_path_list, stdin = None, stdout = None, stderr = None, shell = False)

          #time.sleep(0.100) # pause to partially sync order of opening

      if not do_append_by_child_instance and len(enum_npp_windows.not_multiinst_wnd_list):
        if not no_activate_after_append:
          user32.SetForegroundWindow.restype = wintypes.BOOL
          user32.SetForegroundWindow.argtypes = [
            wintypes.HWND     # [in] HWND   hWnd
          ]

          user32.SetForegroundWindow(enum_npp_windows.not_multiinst_wnd_list[0])

    else:
      print('  - None')

    if not no_exit_after_append:
      sys.exit(0)

  if do_reopen_all_files:
    reopen_all_files(True, allow_reopen_unsaved_files, allow_reopen_edited_files)

def open_from_file_list(file_list):
  print('open_from_file_list:')

  num_opened = 0

  for file in file_list:
    print("  - " + file)
    notepad.open(file)
    num_opened += 1

  print()
  print('* Number of opened paths: ' + str(num_opened))
  print()

# closes (not minimizes) all windows
def close_all_npp_windows(not_multiinst = True, current_proc = True):
  import ctypes
  from ctypes import wintypes

  enum_npp_windows = EnumNppWindows()

  # enumerate Notepad++ instances as standalone windows
  enum_notepadpp_windows(enum_npp_windows)

  user32 = ctypes.windll.user32

  if not hasattr(wintypes, 'LRESULT'):
    wintypes.LRESULT = ctypes.c_ssize_t

  user32.PostMessageW.restype = wintypes.LRESULT
  user32.PostMessageW.argtypes = [
    wintypes.HWND,    # [in] HWND   hWnd,
    wintypes.UINT,    # [in] UINT   Msg,
    wintypes.WPARAM,  # [in] WPARAM wParam,
    wintypes.LPARAM   # [in] LPARAM lParam
  ]

  WM_CLOSE = 0x0010

  # CAUTION:
  #   We close all windows, including all in a process.

  # multi instance windows at first
  for hwnd in enum_npp_windows.multiinst_wnd_list:
    user32.PostMessageW(hwnd, WM_CLOSE, 0, 0)

  # not multi instance (shared) windows at second
  if not_multiinst:
    for hwnd in enum_npp_windows.not_multiinst_wnd_list:
      user32.PostMessageW(hwnd, WM_CLOSE, 0, 0)

  # the current process at the last
  if current_proc:
    notepad.menuCommand(MENUCOMMAND.FILE_EXIT)
