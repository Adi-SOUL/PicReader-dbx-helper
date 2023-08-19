#pragma once
#if _MSC_VER >= 1600
#pragma execution_character_set("utf-8")
#endif

#ifndef __TOOL__
#define __TOOL__

#include "string_op.h"
#include <tuple>
#include <list>
#include <io.h>
#include <direct.h>
#include <locale>
#include <windows.h>
#include <thread>
#include <chrono>
constexpr int LENGTH_OF_MAGIC_NUM = 9;
constexpr int LENGTH_OF_INDEX = 4;
constexpr int LENGTH_OF_TOTAL_NUM = 4;
constexpr int LENGTH_OF_IMAGE_SIZE = 16;
constexpr int LENGTH_OF_IMAGE_NAME = 256;

using std::ios, std::tuple, std::list, std::locale;
auto make_dirs(string dir) -> int;
auto get_path_dir(string filePath) -> string;
auto write_img_file(wstring file_name, wstring& file_name_img, long long int start_at, long long int length) -> void;
auto dbx2img(wstring file_name) -> bool;

#endif // !__TOOL__
// TODO: 在此处引用程序需要的其他标头。
