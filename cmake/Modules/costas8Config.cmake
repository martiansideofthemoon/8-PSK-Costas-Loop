INCLUDE(FindPkgConfig)
PKG_CHECK_MODULES(PC_COSTAS8 costas8)

FIND_PATH(
    COSTAS8_INCLUDE_DIRS
    NAMES costas8/api.h
    HINTS $ENV{COSTAS8_DIR}/include
        ${PC_COSTAS8_INCLUDEDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/include
          /usr/local/include
          /usr/include
)

FIND_LIBRARY(
    COSTAS8_LIBRARIES
    NAMES gnuradio-costas8
    HINTS $ENV{COSTAS8_DIR}/lib
        ${PC_COSTAS8_LIBDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/lib
          ${CMAKE_INSTALL_PREFIX}/lib64
          /usr/local/lib
          /usr/local/lib64
          /usr/lib
          /usr/lib64
)

INCLUDE(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(COSTAS8 DEFAULT_MSG COSTAS8_LIBRARIES COSTAS8_INCLUDE_DIRS)
MARK_AS_ADVANCED(COSTAS8_LIBRARIES COSTAS8_INCLUDE_DIRS)

