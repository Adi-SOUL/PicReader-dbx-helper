# CMakeList.txt: dbx_tools_dev 的 CMake 项目，在此处包括源代码并定义
# 项目特定的逻辑。
#
cmake_minimum_required (VERSION 3.8)

# Enable Hot Reload for MSVC compilers if supported.
if (POLICY CMP0141)
  cmake_policy(SET CMP0141 NEW)
  set(CMAKE_MSVC_DEBUG_INFORMATION_FORMAT "$<IF:$<AND:$<C_COMPILER_ID:MSVC>,$<CXX_COMPILER_ID:MSVC>>,$<$<CONFIG:Debug,RelWithDebInfo>:EditAndContinue>,$<$<CONFIG:Debug,RelWithDebInfo>:ProgramDatabase>>")
endif()

project ("dbx_tools_dev")

# 将源代码添加到此项目的可执行文件。
add_executable (dbx_tools_dev "dbx_tools_dev.cpp" "dbx_tools_dev.h" "string_op.h" "string_op.cpp" "main.cpp")

include_directories(dbx_tools_dev "include")
link_libraries(dbx_tools_dev "libs")

set_property(TARGET dbx_tools_dev PROPERTY CXX_STANDARD 20)
if (CMAKE_VERSION VERSION_GREATER 3.12)
  set_property(TARGET dbx_tools_dev PROPERTY CXX_STANDARD 20)
endif()

# TODO: 如有需要，请添加测试并安装目标。
