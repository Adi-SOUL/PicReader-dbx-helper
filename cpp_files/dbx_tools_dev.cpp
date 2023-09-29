#include "dbx_tools_dev.h"

const string MAGIC_NUM = "Adijnnuuy";
const wstring W_MAGIC_NUM = L"Adijnnuuy";
const string path_str = "\\";
const wstring w_path_str = L"\\";
const char path_char = '\\';
const wchar_t w_path_char = L'\\';

auto get_path_dir(string filePath) -> string {
	string dirPath = filePath;
	size_t p = filePath.find_last_of('\\');
	if (p != -1) {
		dirPath.erase(p);
	}
	return dirPath;
}

auto make_dirs(string dir) -> int {
	if (::_access(dir.c_str(), 00) == 0) {
		return 0;
	}

	list <string> dirList;
	dirList.push_front(dir);

	string curDir = get_path_dir(dir);
	while (curDir != dir) {
		if (::_access(curDir.c_str(), 00) == 0) {
			break;
		}

		dirList.push_front(curDir);

		dir = curDir.c_str();
		curDir = get_path_dir(dir);
	}
	int make_dir_res = 0;
	for (auto it : dirList) {
		wstring w_it = s2ws(it);
		//std::cout << it << std::endl;
		make_dir_res = _wmkdir(w_it.c_str());
	}
	return make_dir_res;
}

auto write_img_file(wstring file_name, wstring& file_name_img, long long int start_at, long long int length) -> void {
	
	char* img = new char[length];
	//std::cout << ws2s(file_name_img) << std::endl;
	
	ifstream sub_dbx_file(file_name, ios::binary);
	sub_dbx_file.seekg(start_at, ios::beg);
	//std::cout << start_at << ';' << sub_dbx_file.tellg() << std::endl;
	sub_dbx_file.read(img, length);
	//string _img;

	std::ofstream img_file;
	img_file.open(file_name_img, ios::binary);
	if (!img_file.is_open()) {
		vector<string> splited_img_path = splited_string(ws2s(file_name_img), path_char);
		vector<string> splited_img_save_dir;
		for (int i = 0; i < splited_img_path.size() - 1; i++) {
			splited_img_save_dir.push_back(splited_img_path[i]);
		}
		string img_save_dir = join(splited_img_save_dir, path_str);
		make_dirs(img_save_dir);
		img_file.open(file_name_img, ios::binary);
	}
	// std::cout << _img << std::endl;
	for (long long int i = 0; i < length; i++) {
		img_file << img[i];
		//if (length > 10000000) std::cout << i << std::endl;
	}
	//std::this_thread::sleep_for(std::chrono::milliseconds(100));
	img_file.close();
	delete[] img;
}

auto dbx2img(wstring file_name) -> bool {
	int LENGTH_OF_INDEX = 8;
	int LENGTH_OF_TOTAL_NUM = 8;
	vector<wstring> splited_file_path = splited_string(file_name, path_char);
	vector<wstring> splited_save_dir;
	for (int i = 0; i < splited_file_path.size() - 1; i++) {
		splited_save_dir.push_back(splited_file_path[i]);
	}
	vector<wstring> raw_splited_dbx_file_name = splited_string(splited_file_path[splited_file_path.size() - 1], L'.');
	vector<wstring> splited_dbx_file_name;
	for (int i = 0; i < raw_splited_dbx_file_name.size() - 1; i++) {
		splited_dbx_file_name.push_back(raw_splited_dbx_file_name[i]);
	}
	wstring dbx_file_name = join(splited_dbx_file_name, L".");
	splited_save_dir.push_back(dbx_file_name);
	wstring w_save_dir = join(splited_save_dir, w_path_str);
	
	string save_dir = ws2s(w_save_dir);
	// std::cout << save_dir << std::endl;

	ifstream dbx_file;
	dbx_file.open(file_name, ios::binary);
	dbx_file.seekg(0, ios::beg);

	string magic_num = get_string_from_file(dbx_file, LENGTH_OF_MAGIC_NUM);
	if (magic_num != MAGIC_NUM) {
		return false;
	}
	try{
		string test_string = get_string_from_file(dbx_file, 16);
	}catch(const std::exception &e){
		LENGTH_OF_INDEX = 4;
		LENGTH_OF_TOTAL_NUM = 4;
	}
	dbx_file.seekg(LENGTH_OF_MAGIC_NUM, ios::beg);
	string str_index = get_string_from_file(dbx_file, LENGTH_OF_INDEX);
	string str_total_num = get_string_from_file(dbx_file, LENGTH_OF_TOTAL_NUM);
	int total_num = std::stoi(str_total_num);

	long long int init_position = LENGTH_OF_MAGIC_NUM + LENGTH_OF_INDEX + LENGTH_OF_TOTAL_NUM + (LENGTH_OF_IMAGE_NAME + LENGTH_OF_IMAGE_SIZE) * total_num;
	long long int start_at = init_position;
	vector<wstring> names;
	vector<vector<string>> splited_names;
	vector<long long int> img_sizes_raw;
	vector<tuple<long long int, long long int>> img_range;

	long long int max_size = 0;
	for (int i = 0; i < total_num; i++) {
		
		string img_file_name_raw = get_string_from_file(dbx_file, LENGTH_OF_IMAGE_NAME);
		vector<string> splited_name_raw = splited_string(img_file_name_raw, path_char);
		//wstring w_img_file_name_raw = s2ws(img_file_name_raw);
		string str_img_size_raw = get_string_from_file(dbx_file, LENGTH_OF_IMAGE_SIZE);
		long long int img_size_raw = std::stoi(str_img_size_raw);
		if (img_size_raw > max_size) {
			max_size = img_size_raw;
		}

		splited_names.push_back(splited_name_raw);
		img_sizes_raw.push_back(img_size_raw);

		long long int end_at = start_at + img_size_raw;
		img_range.push_back(tuple(start_at, end_at));
		start_at = end_at;
	}
	vector<string> common_prefix = find_longest_common_prefix(splited_names);
	int common_length = common_prefix.size();

	for (int i = 0; i < total_num; i++) {
		int length = splited_names[i].size();
		vector<string> this_splited_raw_name = splited_string(save_dir, path_char);
		for (int j = 0; j < length; j++) {
			if (j >= common_length) {
				this_splited_raw_name.push_back(splited_names[i][j]);
			}
		}
		string this_name = join(this_splited_raw_name, path_str);
		wstring w_this_name = s2ws(this_name);
		//std::wcout << w_this_name << std::endl;
		names.push_back(w_this_name);
	}
	
	vector<std::thread> vector_threads;
	for (int i = 0; i < total_num; i++) {
		//write_img_file(file_name, ref(names[i]), std::get<0>(img_range[i]), img_sizes_raw[i]);
		std::thread th(write_img_file, file_name, ref(names[i]), std::get<0>(img_range[i]), img_sizes_raw[i]);
		//th.detach();
		vector_threads.emplace_back(std::move(th));
		
		//std::this_thread::sleep_for(std::chrono::milliseconds(500));
	}
	auto it = vector_threads.begin();
	for (; it != vector_threads.end(); ++it) {
		(*it).join();
	}
}
