cmake_minimum_required(VERSION 3.28)
project(sdl3webgpu C)

find_package(sdl REQUIRED)
find_package(Dawn REQUIRED)

add_library(
    sdl3webgpu
    STATIC
    "${SDL3WEBGPU_DIR}/sdl3webgpu.c"
)

if(APPLE)
  target_compile_options(sdl3webgpu PRIVATE -x objective-c)
endif()

if(EMSCRIPTEN)
  target_compile_definitions(sdl3webgpu PRIVATE WEBGPU_BACKEND_EMDAWNWEBGPU)
endif()

target_link_libraries(
    sdl3webgpu
    PUBLIC
    sdl::sdl
    dawn::webgpu_dawn
)

target_include_directories(
    sdl3webgpu
    PUBLIC
    $<BUILD_INTERFACE:${SDL3WEBGPU_DIR}>
    $<INSTALL_INTERFACE:include>
)
install(FILES "${SDL3WEBGPU_DIR}/sdl3webgpu.h" DESTINATION include)

install(
    TARGETS sdl3webgpu
    EXPORT sdl3webgpuTargets
    ARCHIVE DESTINATION lib
    LIBRARY DESTINATION lib
    RUNTIME DESTINATION bin
    INCLUDES DESTINATION include
)
