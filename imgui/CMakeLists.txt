
cmake_minimum_required(VERSION 3.28)
project(imgui)

set(CMAKE_CXX_STANDARD 20)
set(IMGUI_BACKENDS_DIR ${IMGUI_DIR}/backends)

set(
    IMGUI_SOURCES
    "${IMGUI_DIR}/imgui.cpp"
    "${IMGUI_DIR}/imgui_draw.cpp"
    "${IMGUI_DIR}/imgui_tables.cpp"
    "${IMGUI_DIR}/imgui_widgets.cpp"
    "${IMGUI_DIR}/misc/cpp/imgui_stdlib.cpp"
    "${IMGUI_BACKENDS_DIR}/imgui_impl_opengl3.cpp"
    "${IMGUI_BACKENDS_DIR}/imgui_impl_sdl3.cpp"
)
file(GLOB HEADER_FILES "${IMGUI_DIR}/*.h")
file(GLOB HEADER_BACKEND_FILES "${IMGUI_BACKENDS_DIR}/*.h")

find_package(sdl REQUIRED)

add_library(
    imgui
    STATIC
    ${IMGUI_SOURCES}
)

if(MSVC)
  target_compile_options(imgui PRIVATE /O2)
else()
  target_compile_options(imgui PRIVATE -O3)
endif()

target_link_libraries(
    imgui
    PUBLIC
    sdl::sdl
)

target_include_directories(
    imgui
    PUBLIC
    $<BUILD_INTERFACE:${IMGUI_DIR}>
    $<INSTALL_INTERFACE:include>
)
install(FILES ${HEADER_FILES} DESTINATION include)
install(FILES ${HEADER_BACKEND_FILES} DESTINATION include)
install(FILES ${IMGUI_DIR}/misc/cpp/imgui_stdlib.h DESTINATION include)

install(
    TARGETS imgui
    EXPORT imguiTargets
    ARCHIVE DESTINATION lib
    LIBRARY DESTINATION lib
    RUNTIME DESTINATION bin
    INCLUDES DESTINATION include
)
