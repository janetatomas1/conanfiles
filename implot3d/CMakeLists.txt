
cmake_minimum_required(VERSION 3.28)
project(implot3d)

set(CMAKE_CXX_STANDARD 20)

file(GLOB SOURCES "${IMPLOT3D_DIR}/*.cpp")
file(GLOB HEADERS "${IMPLOT3D_DIR}/*.h")

add_library(
    implot3d
    STATIC
    ${SOURCES}
)
find_package(imgui REQUIRED)

target_include_directories(
    implot3d
    PUBLIC
    $<BUILD_INTERFACE:${IMPLOT3D_DIR}>
    $<INSTALL_INTERFACE:include>
)
target_link_libraries(
    implot3d
    PUBLIC
    imgui::imgui
)

if(MSVC)
  # not in Debug: /O2 can't be combined with CMake's default /RTC1
  target_compile_options(implot3d PRIVATE $<$<NOT:$<CONFIG:Debug>>:/O2>)
else()
  target_compile_options(implot3d PRIVATE -O3)
endif()

install(FILES ${HEADERS} DESTINATION include)
install(
    TARGETS implot3d
    EXPORT implot3dTargets
    ARCHIVE DESTINATION lib
    LIBRARY DESTINATION lib
    RUNTIME DESTINATION bin
    INCLUDES DESTINATION include
)

install(
    EXPORT implot3dTargets
    FILE implot3dTargets.cmake
    NAMESPACE implot3d::
    DESTINATION lib/cmake/implot3d
)

include(CMakePackageConfigHelpers)

configure_package_config_file(
    implot3dConfig.cmake.in
    ${CMAKE_CURRENT_BINARY_DIR}/implot3dConfig.cmake
    INSTALL_DESTINATION lib/cmake/implot3d
)
install(FILES
    ${CMAKE_CURRENT_BINARY_DIR}/implot3dConfig.cmake
    DESTINATION lib/cmake/implot3d
)
