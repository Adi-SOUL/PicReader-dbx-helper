#include "dbx_tools_dev.h"

int wmain(int argc, wchar_t* argv[]) {
	system("chcp 65001");
	//auto start = std::chrono::steady_clock::now();
	bool x = dbx2img(argv[1]);
	//auto end = std::chrono::steady_clock::now();
	//std::cout << "Elapsed time in seconds: "
	//	<< std::chrono::duration_cast<std::chrono::seconds>(end - start).count()
	//	<< " sec";
	//std::cout << x << std::endl;
}