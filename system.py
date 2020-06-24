# This module is to automate system based events.

import pathlib as paths
import shutil
import subprocess as sub
import platform as plat
import datetime as dates

# Function to confirm method input(s) are the correct type 
def _is_type_or_print_err(in_type, target_type, in_type_str):
	if in_type is not target_type:
		if target_type is paths.Path:
			# To keep this cross-platform the target_type = paths.Path() so it knows which type to check
			# 	and then confrim it's actually a Posix or Windows path.
			if in_type is not paths.PosixPath and in_type is not paths.WindowsPath:
				target_type_err_str = 'a pathlib PosixPath or WindowsPath,'
			else:
				return True
		elif target_type is int:
			target_type_err_str = 'an int,'
		elif target_type is bool:
			target_type_err_str = 'True or False,'
		elif target_type is str:
			target_type_err_str = 'a str,'
		else:
			print(f'Error, "{target_type}" is not a type that can be checked in _is_type_or_print_err yet.')
			quit()
		print(f'Error, {in_type_str} must be {target_type_err_str} not "{in_type}"')
		quit()

class Operations:
	def __init__(self, print_success=True, print_err=True):
		self.print_success = print_success
		self.print_err = print_err
	
	def copy_to_clipboard(self, new_clip_value):
		"""This method copies new_clip_value to the clipboard."""
		# Check which operating system is running to get the correct copying keyword.
		if plat.system() == 'Darwin':
			copy_keyword = 'pbcopy'
		elif plat.system() == 'Windows':
			copy_keyword = 'clip'
		else:
			print(f'Error, the copy_to_clipboard function does not have the copy ', end='')
			print(f'keyword for the current operating system: "{plat.system()}"')
			quit()

		sub.run(copy_keyword, universal_newlines=True, input=new_clip_value)
		
		if self.print_success is True:
			print(f'"{new_clip_value}" was copied to the clipboard!')
	
	def get_clipboard(self):
		"""This method gets the contents of the clipboard."""
		
		# Check which operating system is running to get the correct clipboard retrival keyword.
		if plat.system() == 'Darwin':
			paste_keyword_list = ['pbpaste']
		elif plat.system() == 'Windows':
			# TODO find a different command that doesn't open another application momentarily.
			paste_keyword_list = ['powershell.exe', '-command', "Get-Clipboard"]
		else:
			print(f'Error, the copy_to_clipboard function does not have the copy ', end='')
			print(f'keyword for the current operating system: "{plat.system()}"')
			quit()

		# Run command to get clipboard contents.
		clipboard_value = sub.run(paste_keyword_list, universal_newlines=True, capture_output=True)
		
		if self.print_success is True:
			print(f'The clipboard has the value: "{clipboard_value.stdout}"')
		return clipboard_value.stdout
	
	def open_path_or_app(self, open_this, custom_app=None):
		"""This method uses the Terminal to open the input open_this.
		open_this can be a string of an application to open or a path to open.
		custom_app can be set an application name to open the file/folder open_this
		with that application instead of the default one.)"""

		# Confirm open_this is a string or paths.Path().
		if type(open_this) is not str and type(open_this) is not paths.PosixPath and type(open_this) is not paths.WindowsPath:
			print(f'Error, open_this must a string of an application name or a pathlib path,'
			      f'not {type(open_this)}, "{open_this}"')
			quit()
		
		# Determine which terminal keyword to use based on the system this is running on.
		if plat.system() == 'Darwin':
			open_keyword = 'open'
		# If the output path is a WindowsPath then the keyword to open the input is "start" in the terminal.
		elif plat.system() == 'Windows':
			open_keyword = 'start'
		
		# A custom application was specified to the Mac/Linux terminal to add that string to the command.
		if custom_app is not None:
			if type(open_this) is not paths.PosixPath and type(open_this) is not paths.WindowsPath:
				print(f'Error, if custom_app is specified then open_this must be type paths.Path(),'
				      f'not {type(open_this)}, "{open_this}"')
				# print(f'Error, in order to open the file/folder open_this custom_app must be a string of
				#   an application name, ', end='')
				# print(f'not open_this = {type(open_this)}, "{open_this}" and
				#   custom_app = {type(custom_app)}, "{custom_app}"')
				quit()
			elif type(custom_app) is not str:
				print(f'Error, custom_app must me a string of an app name, not {type(custom_app)}, "{custom_app}"')
				quit()
			else:
				# Open the file/folder open_this with str(custom_app).
				open_cmd = [open_keyword, '-a', custom_app, open_this]
				if self.print_success is True:
					print(f'Opened file/folder: "{open_this}" with custom application: "{custom_app}"')
		
		# No specific application was specified so just open with the default application.
		else:
			# Open the application: str(open_this).
			if type(open_this) is str:
				open_cmd = [open_keyword, '-a', open_this]
				if self.print_success is True:
					print(f'Opened application: "{open_this}"')
			# open_this is a paths.Path() so open the file/folder.
			else:
				open_cmd = [open_keyword, open_this]
				if self.print_success is True:
					print(f'Opened file/folder: "{open_this}" with the default application.')
		
		# Run terminal command to open the output file.
		sub.run(open_cmd)

	def fq_app(self, kill_app_name):
		"""This method runs a command in the Terminal (without opening it) to force-quit an application."""

		_is_type_or_print_err(type(kill_app_name), str, 'kill_app_name')

		try:
			cmd = ['osascript', '-e', f'quit app "{kill_app_name}"']
			qt_process = sub.run(cmd, universal_newlines=True)
			if self.print_success is True:
				print(f'Successfully force-quit application: "{kill_app_name}"')
		except:
			if self.print_err is True:
				print(f'''Error, it didn't work. cmd="{cmd}" "{qt_process.stderr, qt_process.stdout}"''')
	
	def hide_app(self, hide_app_name):
		"""This method will hide the input application. So it will still be open, just not visible."""
		_is_type_or_print_err(type(hide_app_name), str, 'kill_app_name')

		cmd = ['osascript', '-e', f'tell application "System Events" to set visible of process "{hide_app_name}" to false']
		qt_process = sub.run(cmd, stdout=sub.PIPE, stderr=sub.PIPE, universal_newlines=True)
		if self.print_success is True:
			print(f'"{hide_app_name}" was hidden.')
		if self.print_err is True:
			print(qt_process.stdout, qt_process.stderr)

class Paths:
	"""This class handles common system path operations."""
	
	def __init__(self, print_success=True, print_err=True):
		self.print_success = print_success
		self.print_err = print_err
	
	def create_dir(self, parent_dir_path, new_dir_name):
		"""This method creates a new directory."""
		
		_is_type_or_print_err(type(parent_dir_path), paths.Path, 'parent_dir_path')
		_is_type_or_print_err(type(new_dir_name), str, 'new_dir_name')

		# pathlib path to new folder from the parent path and the new directory name.
		create_dir_path = parent_dir_path.joinpath(new_dir_name)
		
		# Check for errors then create new directory.
		if create_dir_path.exists():
			if self.print_err is True:
				print(f'Error, target output directory, "{create_dir_path}" already exists.')
			return False
		elif parent_dir_path.is_dir() is False:
			if self.print_err is True:
				print(f'Error, "{parent_dir_path}" is not a valid parent directory.')
			return False
		else:
			create_dir_path.mkdir()
			if self.print_success is True:
				print(f'New directory, "{create_dir_path}" was created!')
			return create_dir_path
		
	def del_ds_store(self, del_ds_dir_or_dir_list, print_deleted=False):
		"""Delete any .DS_Store files within the input directory(s)"""
		
		# Make input a list if it isn't already.
		if type(del_ds_dir_or_dir_list) is not list:
			if type(del_ds_dir_or_dir_list) is not paths.PosixPath and type(del_ds_dir_or_dir_list) is not paths.WindowsPath:
				print(f'Error, del_ds_dir_or_dir_list must be a pathlib directory or a list,', end='')
				print(f' not {type(del_ds_dir_or_dir_list)} "{del_ds_dir_or_dir_list}"')
				quit()
			elif del_ds_dir_or_dir_list.is_dir() is False:
				print(f'''Error, the input folder "{del_ds_dir_or_dir_list}" doesn't exist.''')
				quit()
			else:
				del_ds_dir_or_dir_list = [del_ds_dir_or_dir_list]
		
		# Delete any .DS_Store files.
		for directory in del_ds_dir_or_dir_list:
			if type(directory) is not paths.PosixPath:
				if self.print_err is True:
					print(f'Error, "{del_ds_dir_or_dir_list[0]}" is not a PosixPath.' )
			elif directory.is_dir() is False:
				if self.print_err is True:
					print(f'Error, {directory} is not a directory.')
			else:
				for ds_file in directory.iterdir():
					if ds_file.is_file() and ds_file.name == '.DS_Store':
						ds_file.unlink()
						if print_deleted is True:
							print(f'{ds_file} was deleted.')
	
	def create_cur_year_month_dir(self, parent_dir_path):
		"""Create a directory of the current month and year (if it doesn't already exist.)"""

		# Get the current month and year in str numbers.
		cur_year = dates.date.today().strftime("%Y")
		cur_month = dates.date.today().strftime("%m %B")
		
		_is_type_or_print_err(type(parent_dir_path), paths.Path, 'parent_dir_path')

		if parent_dir_path.exists() is False:
			if self.print_err is True:
				print(f'''Error, the parent directory "{parent_dir_path}" doesn't exist''')
			quit()
		
		# Paths to a dir for the current month and year.
		cur_year_dir = parent_dir_path.joinpath(cur_year)
		cur_month_dir = cur_year_dir.joinpath(cur_month)
		
		# Create the new directories (if the directory already exists it will print an error by default,
		#   so toggle that off because it doesn't matter if that directory already exists).
		if cur_year_dir.exists() is False:
			Paths(self.print_err, self.print_success).create_dir(parent_dir_path, cur_year)
		if cur_month_dir.exists() is False:
			Paths(self.print_err, self.print_success).create_dir(cur_year_dir, cur_month)
		
		return cur_month_dir
	
	def delete(self, del_file_folder_path, del_dir_contents=True, del_in_dir_files=True,
	           del_in_dir_dirs=True, print_individual_deleted=False):
		"""If del_file_folder_path is a file then delete that, if del_dir_contents is True then delete the contents of
		the input directory. Otherwise if del_dir_contents is False then delete the input directory and all of its contents."""
		
		_is_type_or_print_err(type(del_file_folder_path), paths.Path, 'del_file_folder_path')
		_is_type_or_print_err(type(del_dir_contents), bool, 'del_dir_contents')
		_is_type_or_print_err(type(del_in_dir_files), bool, 'del_in_dir_files')
		_is_type_or_print_err(type(del_in_dir_dirs), bool, 'del_in_dir_dirs')
		_is_type_or_print_err(type(print_individual_deleted), bool, 'print_individual_deleted')

		if del_dir_contents is False and del_in_dir_files is True or del_dir_contents is False and del_in_dir_dirs is True:
			print('Error, del_dir_contents is mutually exclusive, so it must be True for del_in_dir_files'
			      f' or del_in_dir_dirs to be True, but del_dir_contents={del_dir_contents}')
			return False
		elif del_dir_contents is True and del_in_dir_files is False and del_in_dir_dirs is False:
			print('Error, either del_in_dir_files or del_in_dir_dirs must be True for del_dir_contents to be True.')
			quit()

		if del_file_folder_path.exists() is False:
			print(f'''Error, target to delete "{del_file_folder_path}" doesn't exist''')
			return False

		if del_file_folder_path.is_dir() is False and del_file_folder_path.is_file() is False:
			print(f'Error, "{del_file_folder_path}" is not a valid file or folder.')
		else:
			if del_file_folder_path.is_dir() is True:
				# For loop to delete all contents or either all files or all folders in the input directory.
				if del_dir_contents is True:
					for content in del_file_folder_path.iterdir():
						if content.is_dir() and del_in_dir_dirs is True:
							shutil.rmtree(content)
							if print_individual_deleted is True:
								print(f'Deleted folder "{content.name}" and all of its contents.')
						elif content.is_file() and del_in_dir_files is True:
							content.unlink()
							if print_individual_deleted is True:
								print(f'Deleted file "{content.name}"')
				else:
					# Delete the input directory and all of its contents.
					shutil.rmtree(del_file_folder_path)
					if self.print_success is True and del_dir_contents is False:
						print(f'Folder "{del_file_folder_path}" and all of its contents were deleted.')
				if self.print_success is True:
					if del_dir_contents is True:
						if del_in_dir_files is True and del_in_dir_dirs is True:
							print(f'All the contents of "{del_file_folder_path}" were deleted.')
						elif del_in_dir_dirs is True:
							print(f'All the folders in "{del_file_folder_path}" were deleted.')
						elif del_in_dir_files is True:
							print(f'All the files in "{del_file_folder_path}" were deleted.')
			elif del_file_folder_path.is_file() is True:
				del_file_folder_path.unlink()
				if self.print_success is True:
					print(f'File "{del_file_folder_path}" was deleted.')
	
	def move_to_new_dir(self, move_file_folder_path, new_dir_path):
		"""This method will move the input file/folder to the output directory."""

		_is_type_or_print_err(type(move_file_folder_path), paths.Path, 'copy_file_folder_path')
		_is_type_or_print_err(type(new_dir_path), paths.Path, 'new_dir_path')

		# List of the operation type for error messages.
		op_type = ['move', 'moved']

		self._check_depend(move_file_folder_path, op_type, new_move_out_dir=new_dir_path)

	def copy_to_new_dir(self, copy_file_folder_path, new_dir_path, new_basename=''):
		"""This method will copy the input file/folder into the output directory.\n
		new_basename can be set to a string to change the output file/folder basename."""

		_is_type_or_print_err(type(copy_file_folder_path), paths.Path, 'copy_file_folder_path')
		_is_type_or_print_err(type(new_dir_path), paths.Path, 'new_dir_path')

		if new_basename is not None and type(new_basename) is not str:
			print(f'Error, new_basename must be None or a string, not {type(new_basename)}, "{new_basename}"')
			return False

		# List of the operation type for error messages.
		op_type = ['copy', 'copied']

		self._check_depend(copy_file_folder_path, op_type, replace_name_with_this=new_basename,
		                   new_move_out_dir=new_dir_path, copy=True)

	def rename(self, rename_file_folder_path, new_name):
		"""This method will rename the input file/folder into the same directory.\n
		new_name can't be an empty string."""

		_is_type_or_print_err(type(rename_file_folder_path), paths.Path, 'rename_file_folder_path')
		_is_type_or_print_err(type(new_name), str, 'new_name')

		if new_name == '':
			print("Error, new_name can't be an empty string.")
			quit()

		# List of the operation type for error messages.
		op_type = ['rename', 'renamed']

		self._check_depend(rename_file_folder_path, op_type, replace_name_with_this=new_name)

	def duplicate(self, copy_file_folder_path, append_str=''):
		"""This method will duplicate the input file/folder into the same directory.\n
		append_str can be set to set a custom value for what is appended to the copied file/folder basename."""
		
		_is_type_or_print_err(type(copy_file_folder_path), paths.Path, 'copy_file_folder_path')
		_is_type_or_print_err(type(append_str), str, 'append_str')

		if append_str == '':
			append_this = ' copy'
		else:
			append_this = append_str

		# List of the operation type for error messages.
		op_type = ['duplicate', 'duplicated']

		self._check_depend(copy_file_folder_path, op_type,
		                   replace_name_with_this=copy_file_folder_path.stem + append_this, copy=True)
	
	def change_ext(self, change_ext_file_path, new_ext, keep_orig_file=True, new_out_path=None):
		"""This method will change the extension for the input file/folder\n
		new_ext must be in the ".ext" format.\n
		if keep_orig_file is True then the input file will be duplicated with a different extensions instead of
		overwriting the input.\n
		If new_out_path is a path.Path then the output with the new extension will be in a different directory."""

		_is_type_or_print_err(type(change_ext_file_path), paths.Path, 'change_ext_file_path')
		_is_type_or_print_err(type(new_ext), str, 'new_ext')
		_is_type_or_print_err(type(keep_orig_file), bool, 'keep_orig_file')

		if new_out_path is not None and type(new_out_path) is not paths.PosixPath and paths.WindowsPath:
			print(f'Error, new_out_path must be None or a pathlib.Path, not {type(new_out_path)}, "{new_out_path}"')
			return False

		# Set out_ext to new_ext because the input is a file.
		if change_ext_file_path.is_file():
			if change_ext_file_path.suffix == new_ext:
				print(f'Error, the target output extension "{new_ext}" is the same as the input extension so nothing happened.')
				print('\nPlease use the duplicate method if you want to copy a file.')
				return False
			
			if new_ext[0] != '.':
				print(f'Error, the new_ext "{new_ext}" must begin with a period.')
				quit()

			if keep_orig_file is True:
				copy_bool = True
			else:
				copy_bool = False
			
			op_type = ['new extension']
			if keep_orig_file is True:
				op_type.append('copied')
			else:
				op_type.append('changed')

			self._check_depend(change_ext_file_path, op_type, new_ext=new_ext,
			                   new_move_out_dir=new_out_path, copy=copy_bool)

		elif change_ext_file_path.is_dir():
			if self.print_err is True:
				print(f'Error, aborted changing the extension because new_ext was specified but'
				      f' the input "{change_ext_file_path}" is a folder.')
			return False
		else:
			if self.print_err is True:
				print(f'''Error, the input file "{change_ext_file_path}" doesn't exist.''')
			return False
		
	def _check_depend(self, in_file_or_dir_path, operation_type_list, replace_name_with_this='',
	                  new_ext='', append_this='', new_move_out_dir=None, copy=False):
		"""This method renames the input, but if the path is changed then it will move the input.\n
		If find_this is specified then it will only rename a file from within the input folder if they have the same
		name and extension (name.ext).\n
		new_move_out_dir can be set for the move, copy, and change_ext methods.\n
		the copy_to_new_dir and duplicate methods have copy set to True so it copies the file instead of moving it.
		"""
		
		_is_type_or_print_err(type(in_file_or_dir_path), paths.Path, 'in_file_or_dir_path')
		_is_type_or_print_err(type(operation_type_list), list, 'operation_type_list')
		_is_type_or_print_err(type(replace_name_with_this), str, 'replace_name_with_this')
		_is_type_or_print_err(type(copy), bool, 'copy')
		_is_type_or_print_err(type(append_this), str, 'append_this')
		_is_type_or_print_err(type(new_ext), str, 'new_ext')

		# If the input doesn't exist then print an error message and return False (the file doesn't exist)
		if in_file_or_dir_path.exists() is False:
			if in_file_or_dir_path.suffix != '':
				if self.print_err is True:
					print(f'''Error, the input file to {operation_type_list[0]} "{in_file_or_dir_path}" doesn't exist.''')
				return False
			else:
				if self.print_err is True:
					print(f'''Error, the input folder to {operation_type_list[0]} "{in_file_or_dir_path}" doesn't exist.''')
				return False

		# Set out_ext to new_ext if it's specified.
		if new_ext != '':
			out_ext = new_ext
		else:
			out_ext = in_file_or_dir_path.suffix

		# The new name for the output is formatted using system names so print an error.
		if replace_name_with_this.startswith('.'):
			print(f'Error, replace_name_with_this "{replace_name_with_this}" can not start with a "."'
			      f' (those are reserved for hidden files).')
			return False
		elif replace_name_with_this != '':
			out_name = replace_name_with_this + append_this + out_ext
		else:
			out_name = in_file_or_dir_path.stem + append_this + out_ext

		# If a "new_move_out_dir" is specified in the initial input
		# 	then create a path object pointing to the new output directory "new_move_out_dir".
		if new_move_out_dir is not None:
			_is_type_or_print_err(type(new_move_out_dir), paths.Path, 'new_move_out_dir')
			if new_move_out_dir.is_dir() is False:
				print(f'''Error, the output folder "{new_move_out_dir}" doesn't exist.''')
				return False
			else:
				# If the input is a file it will append the appropriate extension,
				# 	otherwise if the input is a folder it will append an empty string which won't do anything.
				out_path = paths.Path.joinpath(new_move_out_dir, out_name)
		else:
			out_path = in_file_or_dir_path.with_name(out_name)

		# Check if output already exists.
		if out_path.exists():
				print(f'Error, the target {operation_type_list[0]} output "{out_path}" already exists.')
				return False
		else:
			# No issues were encountered so perform the operation.
			if copy is True:
				if in_file_or_dir_path.is_dir():
					shutil.copytree(in_file_or_dir_path, out_path)
				else:
					shutil.copy2(in_file_or_dir_path, out_path)
			else:
				in_file_or_dir_path.rename(out_path)
			if self.print_success is True:
				# If operation_type_list is copy then set copy_plural to the plural copy (copied)
				print(f'"{in_file_or_dir_path}" was successfully {operation_type_list[1]} to "{out_path}"')
