
cmake_minimum_required(VERSION 3.28)
project(implot)

set(CMAKE_CXX_STANDARD 20)

file(GLOB SOURCES "${IMPLOT_DIR}/*.cpp")
file(GLOB HEADERS "${IMPLOT_DIR}/*.h")

add_library(
    implot
    STATIC
    ${SOURCES}
)
find_package(imgui REQUIRED)

target_include_directories(
    implot
    PUBLIC
    $<BUILD_INTERFACE:${IMPLOT_DIR}>
    $<INSTALL_INTERFACE:include>
)
target_link_libraries(
    implot
    PUBLIC
    imgui::imgui
)

install(FILES ${HEADERS} DESTINATION include)
install(
    TARGETS implot
    EXPORT implotTargets
    ARCHIVE DESTINATION lib
    LIBRARY DESTINATION lib
    RUNTIME DESTINATION bin
    INCLUDES DESTINATION include
)

install(
    EXPORT implotTargets
    FILE implotTargets.cmake
    NAMESPACE implot::
    DESTINATION lib/cmake/implot
)

include(CMakePackageConfigHelpers)

configure_package_config_file(
    implotConfig.cmake.in
    ${CMAKE_CURRENT_BINARY_DIR}/implotConfig.cmake
    INSTALL_DESTINATION lib/cmake/implot
)
install(FILES
    ${CMAKE_CURRENT_BINARY_DIR}/implotConfig.cmake
    DESTINATION lib/cmake/implot
)
