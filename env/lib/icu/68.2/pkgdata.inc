GENCCODE_ASSEMBLY_TYPE=-a gcc-darwin
SO=dylib
SOBJ=dylib
A=a
LIBPREFIX=lib
LIB_EXT_ORDER=.68.2.dylib
COMPILE=x86_64-apple-darwin13.4.0-clang -DU_ATTRIBUTE_DEPRECATED= -D_FORTIFY_SOURCE=2 -isystem /Users/jsheppar/Dropbox (University of Oregon)/GitHub/snow_depth/env/include -mmacosx-version-min=10.9   -DU_HAVE_STRTOD_L=1 -DU_HAVE_XLOCALE_H=1 -DU_HAVE_STRING_VIEW=1  -march=core2 -mtune=haswell -mssse3 -ftree-vectorize -fPIC -fPIE -fstack-protector-strong -O2 -pipe -isystem /Users/jsheppar/Dropbox (University of Oregon)/GitHub/snow_depth/env/include -fdebug-prefix-map=/Users/runner/miniforge3/conda-bld/icu_1635409387295/work=/usr/local/src/conda/icu-68.2 -fdebug-prefix-map=/Users/jsheppar/Dropbox (University of Oregon)/GitHub/snow_depth/env=/usr/local/src/conda-prefix -std=c11 -Wall -pedantic -Wshadow -Wpointer-arith -Wmissing-prototypes -Wwrite-strings   -fno-common -c
LIBFLAGS=-I/Users/jsheppar/Dropbox (University of Oregon)/GitHub/snow_depth/env/include  -dynamic
GENLIB=x86_64-apple-darwin13.4.0-clang -dynamiclib -dynamic -march=core2 -mtune=haswell -mssse3 -ftree-vectorize -fPIC -fPIE -fstack-protector-strong -O2 -pipe -isystem /Users/jsheppar/Dropbox (University of Oregon)/GitHub/snow_depth/env/include -fdebug-prefix-map=/Users/runner/miniforge3/conda-bld/icu_1635409387295/work=/usr/local/src/conda/icu-68.2 -fdebug-prefix-map=/Users/jsheppar/Dropbox (University of Oregon)/GitHub/snow_depth/env=/usr/local/src/conda-prefix -std=c11 -Wall -pedantic -Wshadow -Wpointer-arith -Wmissing-prototypes -Wwrite-strings   -Wl,-pie -Wl,-headerpad_max_install_names -Wl,-dead_strip_dylibs -Wl,-rpath,/Users/jsheppar/Dropbox (University of Oregon)/GitHub/snow_depth/env/lib -L/Users/jsheppar/Dropbox (University of Oregon)/GitHub/snow_depth/env/lib -Wl,-rpath,/Users/jsheppar/Dropbox (University of Oregon)/GitHub/snow_depth/env/lib 
LDICUDTFLAGS=
LD_SONAME=-Wl,-compatibility_version -Wl,68 -Wl,-current_version -Wl,68.2 -install_name /Users/jsheppar/Dropbox (University of Oregon)/GitHub/snow_depth/env/lib/
RPATH_FLAGS=
BIR_LDFLAGS=
AR=x86_64-apple-darwin13.4.0-ar
ARFLAGS=r -c
RANLIB=x86_64-apple-darwin13.4.0-ranlib
INSTALL_CMD=/usr/bin/install -c