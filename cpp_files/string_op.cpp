#include "string_op.h"

auto get_string_from_file(wifstream& __file__, int size_of_string) -> wstring {
	wchar_t* raw_string = new wchar_t[size_of_string];
	__file__.read(raw_string, size_of_string);

	int pos = 0;
	for (pos; pos < size_of_string; pos++) {
		if (raw_string[pos] == '0') {
			pos++;
		}
		else {
			break;
		}
	}
	wstring result = ((wstring)raw_string).substr(pos, size_of_string - pos);
	//wstring w_result = s2ws(result);
	//delete[] raw_string;
	return result;
}

auto splited_string(const wstring& str, wchar_t delim) -> vector<wstring> {
	std::wstringstream ss(str);
	wstring item;
	vector<wstring> elems;

	while (std::getline(ss, item, delim)) {
		if (!item.empty()) {
			elems.push_back(item);
		}
	}
	return elems;
}

auto find_longest_common_prefix(vector<vector<wstring>>& lists) -> vector<wstring> {
	if (lists.empty()) {
		return {};
	}

	vector<wstring> res;
	for (size_t i = 0; i < lists[0].size(); ++i) {
		wstring current = lists[0][i];
		bool is_common = true;

		for (size_t j = 1; j < lists.size(); ++j) {
			if (i >= lists[j].size() || lists[j][i] != current) {
				is_common = false;
				break;
			}
		}
		if (is_common) {
			res.push_back(current);
		}
		else {
			break;
		}
	}
	return res;
}

auto join(vector<wstring>& items, const wstring separator) -> wstring {
	std::wostringstream oss;
	auto it = items.begin();
	if (it != items.end()) {
		oss << *it;
		++it;
	}
	for (; it != items.end(); ++it) {
		oss << separator << *it;
	}
	return oss.str();
}

auto get_string_from_file(ifstream& __file__, int size_of_string) -> string {
	char* raw_string = new char[size_of_string];
	__file__.read(raw_string, size_of_string);

	int pos = 0;
	for (pos; pos < size_of_string; pos++) {
		if (raw_string[pos] != '0') {
			break;
		}
	}

	string result = ((string)raw_string).substr(pos, static_cast<std::basic_string<char, std::char_traits<char>, std::allocator<char>>::size_type>(size_of_string) - pos);
	//wstring w_result = s2ws(result);
	//delete[] raw_string;
	return result;
}

auto splited_string(const string& str, char delim) -> vector<string> {
	std::stringstream ss(str);
	string item;
	vector<string> elems;

	while (std::getline(ss, item, delim)) {
		if (!item.empty()) {
			elems.push_back(item);
		}
	}
	return elems;
}

auto find_longest_common_prefix(vector<vector<string>>& lists) -> vector<string> {
	if (lists.empty()) {
		return {};
	}

	vector<string> res;
	for (size_t i = 0; i < lists[0].size(); ++i) {
		string current = lists[0][i];
		bool is_common = true;

		for (size_t j = 1; j < lists.size(); ++j) {
			if (i >= lists[j].size() || lists[j][i] != current) {
				is_common = false;
				break;
			}
		}
		if (is_common) {
			res.push_back(current);
		}
		else {
			break;
		}
	}
	return res;
}

auto join(vector<string>& items, const string separator) -> string {
	std::ostringstream oss;
	auto it = items.begin();
	if (it != items.end()) {
		oss << *it;
		++it;
	}
	for (; it != items.end(); ++it) {
		oss << separator << *it;
	}
	return oss.str();
}
wstring s2ws(string& str) {
	using convert_typeX = std::codecvt_utf8<wchar_t>;
	std::wstring_convert<convert_typeX, wchar_t> converterX;
	return converterX.from_bytes(str);
}

string ws2s(wstring& wstr) {
	using convert_typeX = std::codecvt_utf8<wchar_t>;
	std::wstring_convert<convert_typeX, wchar_t> converterX;
	return converterX.to_bytes(wstr);
}