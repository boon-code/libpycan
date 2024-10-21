cmake_minimum_required(VERSION 3.10 FATAL_ERROR)

project(testapp LANGUAGES C)

add_compile_options(-Wall -Wextra)

add_library(pycan SHARED IMPORTED)
set_target_properties(pycan PROPERTIES
    IMPORTED_LOCATION "${CMAKE_CURRENT_BINARY_DIR}/libpycan.so"
    INTERFACE_INCLUDE_DIRECTORIES "${CMAKE_CURRENT_SOURCE_DIR}"
)

add_executable(testapp
    "${CMAKE_CURRENT_SOURCE_DIR}/main.c"
)
target_link_libraries(testapp pycan)

add_custom_target(copy_pycan
    COMMAND "${CMAKE_COMMAND}" -E echo "Build and copy libpycan.so"
    COMMAND "${CMAKE_CURRENT_SOURCE_DIR}/build.sh"
    COMMAND "${CMAKE_COMMAND}" -E copy "${CMAKE_CURRENT_SOURCE_DIR}/libpycan.so" "${CMAKE_CURRENT_BINARY_DIR}/libpycan.so"
    COMMAND "${CMAKE_COMMAND}" -E copy "${CMAKE_CURRENT_SOURCE_DIR}/virtual-can.ini" "${CMAKE_CURRENT_BINARY_DIR}/can.ini"
    WORKING_DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}"
)

add_dependencies(pycan copy_pycan)
