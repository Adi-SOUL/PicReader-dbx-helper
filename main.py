import os
from io import BytesIO
from PIL import Image
from sys import argv

if os.name == 'nt':
	path_str = '\\'
else:
	path_str = '/'


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


def dbx2png(dbx_file_name: str) -> None:
	save_dir = path_str.join(dbx_file_name.split(path_str)[:-1])
	with open(dbx_file_name, 'rb') as dbx_file:
		dbx_file.seek(0, 0)
		index_bin = dbx_file.read(32)
		total_size = int(dbx_file.read(128).lstrip(b'0').decode('utf-8'))

		names = []
		sizes = []
		for i in range(total_size):
			_file_name = dbx_file.read(256).lstrip(b'0').decode('utf-8')
			size = int(dbx_file.read(128).lstrip(b'0').decode('utf-8'))
			names.append(_file_name)
			sizes.append(size)

		path_list = [__file_name.split(path_str) for __file_name in names]
		common_prefix = find_longest_common_prefix(path_list)[:-1]
		to_replace = path_str.join(common_prefix)

		for name, size in zip(names, sizes):
			save_filename = name.replace(to_replace, save_dir)
			img_bin = dbx_file.read(size)
			img_bin_io = BytesIO(img_bin)
			img = Image.open(img_bin_io)
			try:
				img.save(save_filename)
			except FileNotFoundError:
				os.makedirs(path_str.join(save_filename.split(path_str)[:-1]))
				img.save(save_filename)
			except FileExistsError:
				pass


def dir2dbx(dir_path: str) -> None:
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

	with open(dbx_path, 'wb') as save:
		x = bytearray('0', encoding='utf-8').zfill(32)
		x += bytearray(str(len(file_list)), encoding='utf-8').zfill(128)
		for file in file_list:
			x += bytearray(file, encoding='utf-8').zfill(256)
			x += bytearray(str(os.path.getsize(file)), encoding='utf-8').zfill(128)
		for file in file_list:
			with open(file, 'rb') as f1:
				n = f1.read()
				x += n
		save.write(x)


if __name__ == '__main__':

	file_name = argv[1]

	if os.path.isfile(file_name):
		if file_name.split('.')[-1] == 'dbx':
			dbx2png(file_name)
		else:
			exit()

	else:
		dir2dbx(file_name)
