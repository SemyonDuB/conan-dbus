from conans import ConanFile, CMake, tools


class DbusConan(ConanFile):
    name = "dbus"
    license = "AFL-2.1-or-later"
    url = ""
    homepage = "https://www.freedesktop.org/wiki/Software/dbus"
    description = "D-Bus is a simple system for interprocess communication and coordination."
    topics = ("conan", "dbus")
    settings = "os", "compiler", "build_type", "arch"

    options = {
            "with_x11": [True, False], 
            "with_glib": [True, False],
            "disable_assert": [True, False],
            "disable_checks": [True, False],
            "enable_ansi": [True, False],
            "enable_containers": [True, False],
            "enable_stats": [True, False],
            "enable_verbose_mode": [True, False],
            "gcov_enabled": [True, False],
            "install_system_libs": [True, False],
            "use_output_debug_string": [True, False]}

    default_options = {
            "with_x11": False,
            "with_glib": False,
            "disable_assert": False,
            "disable_checks": False,
            "enable_ansi": False,
            "enable_containers": False,
            "enable_stats": False,
            "enable_verbose_mode": True,
            "gcov_enabled": False,
            "install_system_libs": False,
            "use_output_debug_string": False}

    generators = "cmake_find_package"


    def source(self):

        tools.get(**self.conan_data["sources"][self.version])

        dbus_cmake = tools.os.path.join("dbus-" + self.version, "cmake", "CMakeLists.txt")
        dbus_cmake_tools = tools.os.path.join("dbus-" + self.version, "cmake", 
                "tools", "CMakeLists.txt")

        if self.options.with_glib:
            tools.replace_in_file(dbus_cmake, "GLib2", "glib")
            tools.replace_in_file(dbus_cmake, "GLIB2", "GLIB")

        if self.options.with_x11:
            tools.replace_in_file(dbus_cmake, "X11", "libx11")
            tools.replace_in_file(dbus_cmake_tools, "X11", "libx11")


    def requirements(self):

        self.requires("expat/2.2.9")

        if self.options.with_glib:
            self.requires("glib/2.64.0@bincrafters/stable")

        if self.options.with_x11:
            self.requires("libx11/1.6.8@bincrafters/stable")
            self.requires("libxext/1.3.4@bincrafters/stable")
            self.requires("libxrandr/1.5.2@bincrafters/stable")
            self.requires("libxrender/0.9.10@bincrafters/stable")
            self.requires("libxi/1.7.10@bincrafters/stable")
            self.requires("libxcursor/1.2.0@bincrafters/stable")
            self.requires("libxdamage/1.1.5@bincrafters/stable")
            self.requires("libxfixes/5.0.3@bincrafters/stable")
            self.requires("libxcomposite/0.4.5@bincrafters/stable")
            self.requires("libxinerama/1.1.4@bincrafters/stable")
            self.requires("fontconfig/2.13.91@conan/stable")


    def configure_cmake(self):
        cmake = CMake(self)

        cmake.definitions["DBUS_BUILD_TESTS"] = "OFF"
        cmake.definitions["DBUS_ENABLE_DOXYGEN_DOCS"] = "OFF"
        cmake.definitions["DBUS_ENABLE_XML_DOCS"] = "OFF"

        if self.options.with_x11 == True:
            cmake.definitions["DBUS_BUILD_X11"] = "ON"

        if self.options.with_glib == True:
            cmake.definitions["DBUS_WITH_GLIB"] = "ON"

        if self.options.disable_assert == True:
            cmake.definitions["DBUS_DISABLE_ASSERT"] = "ON"

        if self.options.disable_checks == True:
            cmake.definitions["DBUS_DISABLE_CHECKS"] = "ON"

        if self.options.enable_ansi == True:
            cmake.definitions["DBUS_ENABLE_ANSI"] = "ON"

        if self.options.enable_containers == True:
            cmake.definitions["DBUS_ENABLE_CONTAINERS"] = "ON"

        if self.options.enable_stats == True:
            cmake.definitions["DBUS_ENABLE_STATS"] = "ON"

        if self.options.enable_verbose_mode == False:
            cmake.definitions["DBUS_ENABLE_VERBOSE_MODE"] = "OFF"

        if self.options.gcov_enabled == True:
            cmake.definitions["DBUS_GCOV_ENABLED"] = "ON"

        if self.options.install_system_libs == True:
            cmake.definitions["DBUS_INSTALL_SYSTEM_LIBS"] = "ON"

        if self.options.use_output_debug_string == True:
            cmake.definitions["DBUS_USE_OUTPUT_DEBUG_STRING"] = "ON"

        cmake.configure(source_folder="dbus-{}/cmake".format(self.version))
        
        return cmake


    def build(self):
        cmake = self.configure_cmake()
        cmake.build()


    def package(self):
        cmake = self.configure_cmake()
        cmake.install()

