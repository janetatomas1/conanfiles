
cmake_minimum_required(VERSION 3.28)
project(implot)

set(CMAKE_CXX_STANDARD 20)

if(MSVC)
    file(GLOB SOURCES "${CMAKE_SOURCE_DIR}\\implot\\*.cpp")
else()
    file(GLOB SOURCES "${CMAKE_SOURCE_DIR}/implot/*.cpp")
endif()

add_library(
    implot
    STATIC
    ${SOURCES}
)

target_link_directories(
    implot
    PUBLIC
    ${CMAKE_LIBRARY_PATH}
)
target_link_libraries(
    implot
    PUBLIC
    imgui
)
target_include_directories(
    implot
    PUBLIC
    ${CMAKE_INCLUDE_PATH}
)

file(GLOB HEADER_FILES "${CMAKE_SOURCE_DIR}/implot/*.h")

install(
    TARGETS implot
    ARCHIVE DESTINATION lib
)
install(FILES ${HEADER_FILES} DESTINATION include)
