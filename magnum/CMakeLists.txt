cmake_minimum_required(VERSION 3.5...3.10)
project(phony)

add_subdirectory(corrade EXCLUDE_FROM_ALL)
add_subdirectory(magnum EXCLUDE_FROM_ALL)

add_executable(
    phony
    main.cpp
)

target_link_libraries(
    phony
    PRIVATE
#    Magnum::Application
    Magnum::GL
    Magnum::Magnum
    Magnum::Shaders
)
