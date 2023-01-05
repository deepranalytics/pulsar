
cmake_minimum_required(VERSION 3.13)

add_definitions(-DCMS_MAJOR_VER=5)
add_definitions(-DCMS_MINOR_VER=0)
add_definitions(-DCMS_REVISION_VER=0)

project(pulsar)
#set(CMAKE_INSTALL_PREFIX ${CMAKE_CURRENT_LIST_DIR}/x64/unix/${CMAKE_BUILD_TYPE})
#set(CMAKE_INSTALL_PREFIX ${CMAKE_CURRENT_LIST_DIR}/x64/windows/${CMAKE_BUILD_TYPE})

# Enable cpp 17 standard.
set(CMAKE_CXX_STANDARD 17)

if(CONAN_EXPORTED) # in conan local cache
    # standard conan installation, deps will be defined in conanfile.py
    # and not necessary to call conan again, conan is already running
    include(${CMAKE_BINARY_DIR}/../conanbuildinfo.cmake)
    conan_basic_setup()
else() # in user space
    # Make sure to use conanfile.py to define dependencies, to stay consistent
    include(${CMAKE_CURRENT_LIST_DIR}/conan/conanbuildinfo.cmake)
    conan_basic_setup()
endif()


# Check current platform architecture.
if (${CMAKE_SIZEOF_VOID_P} EQUAL "8")
    set (CMS_ARCHITECTURE "x64")
else ()
    set (CMS_ARCHITECTURE "x86")
endif ()

# # Create directory where CMSAPI will be copied on installation.
# # For windows it will be project_dir/x64/windows/{Debug/Release}
# # For Linux it will be project_dir/x64/unix/{Debug/Release}
if(CONAN_EXPORTED) # in conan local cache
    set(CMS_DESTINATION_DIR "${CMAKE_BINARY_DIR}/${CMS_ARCHITECTURE}/${CURRENT_SYSTEM_TYPE}/${CMAKE_BUILD_TYPE}")
else()
    set(CMS_DESTINATION_DIR "${CMAKE_CURRENT_SOURCE_DIR}/${CMS_ARCHITECTURE}/${CURRENT_SYSTEM_TYPE}/${CMAKE_BUILD_TYPE}")
endif()

message("destination: ${CMS_DESTINATION_DIR}")
file(MAKE_DIRECTORY ${CMS_DESTINATION_DIR})

if(DEFINED ${CONAN_INSTALL_PREFIX})
    message("Conan Install Prefix Is Given: ${CONAN_INSTALL_PREFIX}")
    set(CMS_INSTALL_DIR ${CONAN_INSTALL_PREFIX})
else()
    message("Building with default install path.")
    set(CMS_INSTALL_DIR "${CMS_DESTINATION_DIR}/../install")
    file(MAKE_DIRECTORY ${CMS_INSTALL_DIR})
endif()

message("install: ${CMS_INSTALL_DIR}")
set(CMS_PARENT_PATH "${CMAKE_CURRENT_LIST_DIR}")

# Add carclient project.
include_directories(${CMAKE_CURRENT_LIST_DIR}/pulsar-client-cpp/include)
include_directories(${CMAKE_CURRENT_LIST_DIR}/pulsar-client-cpp)
add_subdirectory(pulsar-client-cpp)
