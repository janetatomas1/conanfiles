
cmake_minimum_required(VERSION 3.28)
project(imgui)

set(CMAKE_CXX_STANDARD 20)
message(${IMGUI_DIR} "aaaa")
set(IMGUI_BACKENDS_DIR ${IMGUI_DIR}/backends)

set(
    IMGUI_SOURCES
    "${IMGUI_DIR}/imgui.cpp"
    "${IMGUI_DIR}/imgui_draw.cpp"
    "${IMGUI_DIR}/imgui_tables.cpp"
    "${IMGUI_DIR}/imgui_widgets.cpp"
    "${IMGUI_DIR}/misc/cpp/imgui_stdlib.cpp"
    "${IMGUI_BACKENDS_DIR}/imgui_impl_opengl3.cpp"
    "${IMGUI_BACKENDS_DIR}/imgui_impl_glfw.cpp"
)
file(GLOB HEADER_FILES "${IMGUI_DIR}/*.h")
file(GLOB HEADER_BACKEND_FILES "${IMGUI_BACKENDS_DIR}/*.h")

add_library(
    imgui
    STATIC
    ${IMGUI_SOURCES}
)

target_link_directories(
    imgui
    PUBLIC
    ${CMAKE_LIBRARY_PATH}
)
target_link_libraries(
    imgui
    PUBLIC
    glfw
)
target_include_directories(
    imgui
    PUBLIC
    ${CMAKE_INCLUDE_PATH}
    ${IMGUI_DIR}
    ${IMGUI_BACKENDS_DIR}
)
install(
    TARGETS imgui
    ARCHIVE DESTINATION lib
)
install(FILES ${HEADER_FILES} DESTINATION include)
install(FILES ${HEADER_BACKEND_FILES} DESTINATION include)
install(FILES ${IMGUI_DIR}/misc/cpp/imgui_stdlib.h DESTINATION include)
