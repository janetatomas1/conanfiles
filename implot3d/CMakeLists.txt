
cmake_minimum_required(VERSION 3.28)
project(implot3d)

set(CMAKE_CXX_STANDARD 20)

file(GLOB SOURCES "${CMAKE_SOURCE_DIR}/implot3d/*.cpp")

add_library(
    implot3d
    STATIC
    ${SOURCES}
)

target_link_directories(
    implot3d
    PUBLIC
    ${CMAKE_LIBRARY_PATH}
)
target_link_libraries(
    implot3d
    PUBLIC
    imgui
)
target_include_directories(
    implot3d
    PUBLIC
    ${CMAKE_INCLUDE_PATH}
)

file(GLOB HEADER_FILES "${CMAKE_SOURCE_DIR}/implot3d/*.h")


install(
    TARGETS implot3d
    ARCHIVE DESTINATION lib
)
install(FILES ${CMAKE_SOURCE_DIR}/implot3d/implot3d.h DESTINATION include)
install(FILES ${CMAKE_SOURCE_DIR}/implot3d/implot3d_internal.h DESTINATION include)
