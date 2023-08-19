#pragma once
#ifndef __STRING_OP__
#define __STRING_OP__


#include <iostream>
#include <fstream>
#include <vector>
#include <codecvt>
#include <sstream>
#include <algorithm>
#include <ranges>
#include <string>

using std::string, std::wstring, std::wifstream, std::stringstream, std::vector, std::ostringstream, std::ifstream;
// for wstring
auto get_string_from_file(wifstream& __file__, int size_of_string) -> wstring;
auto splited_string(const wstring& str, wchar_t delim) -> vector<wstring>;
auto find_longest_common_prefix(vector<vector<wstring>>& lists) -> vector<wstring>;
auto join(vector<wstring>& items, const wstring separator) -> wstring;

// for string
auto get_string_from_file(ifstream& __file__, int size_of_string) -> string;
auto splited_string(const string& str, char delim) -> vector<string>;
auto find_longest_common_prefix(vector<vector<string>>& lists) -> vector<string>;
auto join(vector<string>& items, const string separator) -> string;

wstring s2ws(string& str);
string ws2s(wstring& wstr);


#endif // !__STRING_OP__