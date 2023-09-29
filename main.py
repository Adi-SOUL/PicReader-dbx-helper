import os
import re
from io import BytesIO
from sys import argv
from time import strftime, localtime

from PIL import Image, ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True

from hashlib import md5


if os.name == 'nt':
	path_str = '\\'
else:
	path_str = '/'

MAGIC_NUM = 'Adijnnuuy'


def find_longest_common_prefix(lists):
	if not lists:
		return []

	it = zip(*lists)
	res = []
	for group in it:
		if all(x == group[0] for x in group):
			res.append(group[0])
		else:
			break
	return res


def get_data_and_update_its_md5(_md5_: md5, _file_object_, size: int):
	while True:
		chunk = _file_object_.read(size)
		if not chunk:
			raise EOFError
		else:
			_md5_.update(chunk)
			yield chunk, str(_md5_.hexdigest())


def dbx2png(dbx_file_name: str) -> None:
	save_dir = path_str.join(dbx_file_name.split(path_str)[:-1] + ['.'.join(dbx_file_name.split(path_str)[-1].split('.')[:-1])])
	with open(dbx_file_name, 'rb') as dbx_file:
		dbx_file.seek(0, 0)
		magic_num = dbx_file.read(9).decode('utf-8')
		if magic_num != MAGIC_NUM:
			exit()

		test_bytes = dbx_file.read(8).lstrip(b'0')
		dbx_file.seek(9, 0)
		if test_bytes:
			test_bytes = dbx_file.read(16).lstrip(b"0").decode('utf-8')
			try:
				_ = int(test_bytes)
			except ValueError:
				INDEX_LENGTH = 4
				TOTAL_SIZE_LENGTH = 4
			else:
				INDEX_LENGTH = 8
				TOTAL_SIZE_LENGTH = 8
			IMG_SIZE_LENGTH = 16
			dbx_file.seek(9, 0)
		else:
			INDEX_LENGTH = 32
			TOTAL_SIZE_LENGTH = 128
			IMG_SIZE_LENGTH = 128

		_ = dbx_file.read(INDEX_LENGTH)
		total_size = int(dbx_file.read(TOTAL_SIZE_LENGTH).lstrip(b'0').decode('utf-8'))

		names = []
		sizes = []
		for i in range(total_size):
			_file_name = dbx_file.read(256).lstrip(b'0').decode('utf-8')
			size = int(dbx_file.read(IMG_SIZE_LENGTH).lstrip(b'0').decode('utf-8'))
			names.append(_file_name)
			sizes.append(size)

		path_list = [__file_name.split(path_str) for __file_name in names]
		common_prefix = find_longest_common_prefix(path_list)[:-1]
		to_replace = path_str.join(common_prefix)

		for _name_, _size_ in zip(names, sizes):
			save_filename = _name_.replace(to_replace, save_dir)
			img_bin = dbx_file.read(_size_)
			img_bin_io = BytesIO(img_bin)
			img = Image.open(img_bin_io)
			try:
				img.save(save_filename)
			except FileNotFoundError:
				os.makedirs(path_str.join(save_filename.split(path_str)[:-1]))
				img.save(save_filename)
			except FileExistsError:
				pass
			except OSError:
				# print(save_filename)
				save_filename = '.'.join(save_filename.split('.')[:-1]+['png'])
				img.save(save_filename)


def dir2dbx(dir_path: str) -> None:
	file_md5 = md5()
	dir_path = path_str.join(dir_path.split('/'))
	file_list = []
	for __dir_path, __dir_name, __file_names in os.walk(dir_path):
		__dir_path = path_str.join(__dir_path.split('/'))
		for __file_name in __file_names:
			img_file = path_str.join([__dir_path, __file_name])
			extent = __file_name.split('.')[-1].lower()
			if extent in ['png', 'jpg', 'jpeg'] and os.path.getsize(img_file) > 2e5:
				file_list.append(img_file)
	fast_save = '.'.join([dir_path.split(path_str)[-1], 'dbx'])
	save_dir = path_str.join(dir_path.split(path_str)[:-1])
	dbx_path = path_str.join([save_dir, fast_save])

	path_list = [__file_name.split(path_str) for __file_name in file_list]
	common_prefix = find_longest_common_prefix(path_list)
	root_for_file_whose_name_is_too_long = path_str.join(common_prefix+['file_whose_name_is_too_long'])

	file_name_that_is_too_long: dict = {}
	index_of_file_name_that_is_too_long: int = 1

	with open(dbx_path, 'wb') as save:

		# ---- HEAD ---- #

		x = bytearray(MAGIC_NUM, encoding='utf-8')
		x += bytearray('0', encoding='utf-8').zfill(8) # 32 -> 4
		x += bytearray(str(len(file_list)), encoding='utf-8').zfill(8)  # 128 -> 4 // The same as index.

		# ----- FILE DIRECTORY ---- #

		for file in file_list:
			b_file_name = bytearray(file, encoding='utf-8')
			if len(b_file_name) > 256:
				file_extent: str = file.split('.')[-1]
				changed_file_name = path_str.join(
					[
						root_for_file_whose_name_is_too_long,
						f'file_name_that_is_too_long_{index_of_file_name_that_is_too_long}.{file_extent}'
					]
				)
				b_file_name = bytearray(changed_file_name, encoding='utf-8')
				file_name_that_is_too_long[file] = changed_file_name
				index_of_file_name_that_is_too_long += 1

			x += b_file_name.zfill(256)
			x += bytearray(str(os.path.getsize(file)), encoding='utf-8').zfill(16)  # 128 -> 16
		file_md5.update(x)
		save.write(x)

		# ---- FILE CONTENT ---- #

		time_array = []
		for current_file_name in file_list:
			with open(current_file_name, 'rb') as f1:
				n = f1.read()
				time_array.append(strftime('%Y%m%d%H%M%S', localtime(os.stat(current_file_name).st_mtime)))
				file_md5.update(n)
				save.write(n)

		# ---- MD5 ---- #

		md5_value = str(file_md5.hexdigest())
		save.write(bytearray(md5_value, encoding='utf-8'))

		# ---- TIME INFO ---- #

		for time_str in time_array:
			save.write(bytearray(time_str, encoding='utf-8'))

		if file_name_that_is_too_long:
			text_file_path = '.'.join(dbx_path.split('.')[:-1]+['convert_log', 'txt'])
			with open(text_file_path, 'w', encoding='utf-8') as text_file:
				text_file.write(
					'Some image files have been moved because their names are longer than 256 under encoding: "utf-8".\n')
				text_file.write(
					'Here are the mappings:\n')
				for key, value in file_name_that_is_too_long.items():
					text_file.write(f'Origin file:\n {key}\n has been moved to:\n {value}\n')


def get_structure(dbx_file_name: str) -> None:
	def flatten(_list: list) -> list:
		res = sum(([x] if not isinstance(x, list) else flatten(x) for x in _list), [])
		return res

	def get_sub_file(fake_file: str, fake_file_list: list[str]) -> list:
		result = []
		for f in fake_file_list:
			if f.startswith(fake_file) and f != fake_file:
				temp = f.replace(fake_file, '')
				if temp.split(path_str)[0] not in result:
					result.append(temp.split(path_str)[0])
		return result

	def fake_is_dir(fake_file: str, fake_file_list: list[str]) -> bool:
		result = []
		for f in fake_file_list:
			if f.startswith(fake_file) and f != fake_file:
				result.append(f)
		return bool(len(result))

	# def has_dir(fake_file: str, fake_file_list: list[str]) -> bool:
	# 	for item in get_sub_file(fake_file, fake_file_list):
	#
	# 		if fake_is_dir(''.join([item, fake_file]), fake_file_list):
	# 			return True
	# 	return False

	def _sort_(file_list: list[str]) -> list:

		def encode(_str: str) -> int:
			num = re.findall('\d+', _str)
			if num:
				return max(0, min(int(''.join(num)), 2147483647))
			else:
				return 0

		max_depth = max([len(x.split(path_str)) for x in file_list])
		new_file_list = []
		for file in file_list:
			split_file = file.split(path_str)
			_len_file_name = len(split_file)
			if _len_file_name == max_depth:
				new_file_list.append(file)
			else:
				ext = ['OutOfRange'] * (max_depth - _len_file_name)
				new_file_list.append(path_str.join(split_file[:-1] + ext + [split_file[-1]]))

		convert = [new_file_list]
		depth = 1
		while depth < max_depth:
			sub = []
			for to_be_sort in convert:
				to_be_sort.sort(key=lambda x: encode(x.split(path_str)[depth]))
				search_length = len(to_be_sort)
				while search_length >= 1:
					sub_list = []
					_path = to_be_sort[0].split(path_str)[:depth]
					for index in range(search_length - 1, -1, -1):
						if to_be_sort[index].split(path_str)[:depth] == _path:
							sub_list.append(to_be_sort.pop(index))
					sub.append(sub_list)

					search_length = len(to_be_sort)
			convert = sub
			depth = depth + 1

		raw_sorted_list = flatten(convert)
		file_list = [ii.replace(path_str + 'OutOfRange', '') for ii in raw_sorted_list]
		file_list.reverse()

		return file_list

	def tree(path, depth):
		if depth == 0:
			save_list.append('[ROOT]\n')

		for item in get_sub_file(path, names):
			if fake_is_dir(''.join([path, item]), names):
				save_list.append('|    ' * depth + f'+----[{item}]\n')
			else:
				save_list.append('|    ' * depth + f'+----{item}\n')

			new_item = ''.join([path, item])
			if fake_is_dir(new_item, names):
				tree(new_item + path_str, depth + 1)

	save_path = '.'.join(['.'.join(dbx_file_name.split('.')[:-1]), 'txt'])
	with open(dbx_file_name, 'rb') as dbx_file:
		dbx_file.seek(0, 0)
		magic_num = dbx_file.read(9).decode('utf-8')
		if magic_num != MAGIC_NUM:
			exit()

		test_bytes = dbx_file.read(8).lstrip(b'0')
		dbx_file.seek(9, 0)
		if test_bytes:
			test_bytes = dbx_file.read(16).lstrip(b"0").decode('utf-8')
			try:
				_ = int(test_bytes)
			except ValueError:
				INDEX_LENGTH = 4
				TOTAL_SIZE_LENGTH = 4
			else:
				INDEX_LENGTH = 8
				TOTAL_SIZE_LENGTH = 8
			IMG_SIZE_LENGTH = 16
			dbx_file.seek(9, 0)
		else:
			INDEX_LENGTH = 32
			TOTAL_SIZE_LENGTH = 128

		_ = dbx_file.read(INDEX_LENGTH)
		total_size = int(dbx_file.read(TOTAL_SIZE_LENGTH).lstrip(b'0').decode('utf-8'))

		names = []
		for i in range(total_size):
			_file_name = dbx_file.read(256).lstrip(b'0').decode('utf-8')
			_ = int(dbx_file.read(IMG_SIZE_LENGTH).lstrip(b'0').decode('utf-8'))
			names.append(_file_name)

		names = _sort_(names)

		path_list = [__file_name.split(path_str) for __file_name in names]
		common_prefix = find_longest_common_prefix(path_list) + ['']
		root = path_str.join(common_prefix)

		save_list = []
		tree(root, 0)
		save_list.append('[END]\n')

		with open(save_path, 'w', encoding='utf-8') as save_file:
			save_file.writelines(save_list)


if __name__ == '__main__':

	command = argv[1]
	file_name = argv[2]

	if command == 'c':
		if os.path.isfile(file_name):
			dbx2png(file_name)
		else:
			dir2dbx(file_name)
	elif command == 't':
		if os.path.isfile(file_name):
			get_structure(file_name)
