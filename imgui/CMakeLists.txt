
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
    "${IMGUI_BACKENDS_DIR}/imgui_impl_sdlgpu3.cpp"
    "${IMGUI_BACKENDS_DIR}/imgui_impl_wgpu.cpp"
)
file(GLOB HEADER_FILES "${IMGUI_DIR}/*.h")
file(GLOB HEADER_BACKEND_FILES "${IMGUI_BACKENDS_DIR}/*.h")

find_package(sdl REQUIRED)
find_package(Dawn REQUIRED)

add_library(
    imgui
    STATIC
    ${IMGUI_SOURCES}
)

if(MSVC)
  # not in Debug: /O2 can't be combined with CMake's default /RTC1
  target_compile_options(imgui PRIVATE $<$<NOT:$<CONFIG:Debug>>:/O2>)
else()
  target_compile_options(imgui PRIVATE -O3)
endif()

if(APPLE)
  set_source_files_properties("${IMGUI_BACKENDS_DIR}/imgui_impl_wgpu.cpp" PROPERTIES COMPILE_OPTIONS "-x;objective-c++")
endif()

# Vulkan renderer, native only. Its functions are loaded at runtime (ImGui_ImplVulkan_LoadFunctions), so the
# Vulkan loader isn't linked; the app loads it.
if(NOT EMSCRIPTEN)
  find_package(VulkanHeaders REQUIRED)
  target_sources(imgui PRIVATE "${IMGUI_BACKENDS_DIR}/imgui_impl_vulkan.cpp")
  target_compile_definitions(imgui PUBLIC IMGUI_IMPL_VULKAN_NO_PROTOTYPES)
  target_link_libraries(imgui PUBLIC vulkan-headers::vulkan-headers)
endif()

# Dawn-style webgpu.h; also correct for Emscripten's emdawnwebgpu port
target_compile_definitions(imgui PUBLIC IMGUI_IMPL_WEBGPU_BACKEND_DAWN)

target_link_libraries(
    imgui
    PUBLIC
    sdl::sdl
    dawn::webgpu_dawn
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
