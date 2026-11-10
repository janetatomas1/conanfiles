
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
    "${IMGUI_BACKENDS_DIR}/imgui_impl_sdl3.cpp"
)
file(GLOB HEADER_FILES "${IMGUI_DIR}/*.h")
file(GLOB HEADER_BACKEND_FILES "${IMGUI_BACKENDS_DIR}/*.h")

# Renderer backends, set by the recipe's options
option(IMGUI_OPENGL "Build imgui_impl_opengl3" ON)
option(IMGUI_SDLGPU "Build imgui_impl_sdlgpu3" ON)
option(IMGUI_WEBGPU "Build imgui_impl_wgpu" ON)
option(IMGUI_VULKAN "Build imgui_impl_vulkan" ON)
option(IMGUI_TEST_ENGINE "Build Dear ImGui Test Engine into the library" OFF)

find_package(sdl REQUIRED)

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

if(IMGUI_OPENGL)
  target_sources(imgui PRIVATE "${IMGUI_BACKENDS_DIR}/imgui_impl_opengl3.cpp")
endif()

if(IMGUI_SDLGPU)
  target_sources(imgui PRIVATE "${IMGUI_BACKENDS_DIR}/imgui_impl_sdlgpu3.cpp")
endif()

if(IMGUI_WEBGPU)
  find_package(Dawn REQUIRED)
  target_sources(imgui PRIVATE "${IMGUI_BACKENDS_DIR}/imgui_impl_wgpu.cpp")
  # Dawn-style webgpu.h; also correct for Emscripten's emdawnwebgpu port
  target_compile_definitions(imgui PUBLIC IMGUI_IMPL_WEBGPU_BACKEND_DAWN)
  target_link_libraries(imgui PUBLIC dawn::webgpu_dawn)
endif()

# Vulkan renderer, native only (the recipe has no vulkan option on Emscripten). Its functions are loaded at
# runtime (ImGui_ImplVulkan_LoadFunctions), so the Vulkan loader isn't linked; the app loads it.
if(IMGUI_VULKAN)
  find_package(VulkanHeaders REQUIRED)
  target_sources(imgui PRIVATE "${IMGUI_BACKENDS_DIR}/imgui_impl_vulkan.cpp")
  target_compile_definitions(imgui PUBLIC IMGUI_IMPL_VULKAN_NO_PROTOTYPES)
  target_link_libraries(imgui PUBLIC vulkan-headers::vulkan-headers)
endif()

# Dear ImGui Test Engine, in the same library: imgui calls its hooks (IMGUI_ENABLE_TEST_ENGINE), and both have to
# be built with the same defines. Its coroutines run on std::thread.
if(IMGUI_TEST_ENGINE)
  file(GLOB IMGUI_TEST_ENGINE_SOURCES "${IMGUI_TEST_ENGINE_DIR}/*.cpp")
  file(GLOB IMGUI_TEST_ENGINE_HEADERS "${IMGUI_TEST_ENGINE_DIR}/*.h")
  target_sources(imgui PRIVATE ${IMGUI_TEST_ENGINE_SOURCES})
  target_compile_definitions(imgui PUBLIC IMGUI_ENABLE_TEST_ENGINE IMGUI_TEST_ENGINE_ENABLE_COROUTINE_STDTHREAD_IMPL=1)
  target_include_directories(imgui PUBLIC $<BUILD_INTERFACE:${IMGUI_TEST_ENGINE_DIR}>)
  find_package(Threads REQUIRED)
  target_link_libraries(imgui PUBLIC Threads::Threads)
  # Its headers include "imgui.h", so they go next to imgui's; the capture tool includes thirdparty/stb.
  install(FILES ${IMGUI_TEST_ENGINE_HEADERS} DESTINATION include)
  install(DIRECTORY ${IMGUI_TEST_ENGINE_DIR}/thirdparty DESTINATION include FILES_MATCHING PATTERN "*.h")
endif()

target_link_libraries(imgui PUBLIC sdl::sdl)

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
