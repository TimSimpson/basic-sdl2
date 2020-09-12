
import os.path
import shutil

import conans
from conans import tools


class GzipDownloader:

    def __init__(self, base_name, url, md5_sum):
        self._base_name = base_name
        self._url = url
        self._md5_sum = md5_sum
        self._gzip_name = "{}.tar.gz".format(self._base_name)

    def _get_gzip_path(self, folder):
        return os.path.join(folder, self._gzip_name)

    def get_extracted_directory(self, folder):
        return os.path.join(folder, self._base_name)

    def _confirm_valid_gzip_file_or_download(self, folder):
        gzip_path = self._get_gzip_path(folder)
        if os.path.exists(gzip_path):
            try:
                tools.check_md5(gzip_path, self._md5_sum)
                return gzip_path
            except BaseException:
                os.remove(gzip_path)

        tools.download(self._url, gzip_path)
        tools.check_md5(gzip_path, self._md5_sum)
        return gzip_path

    def _clean_extracted_directory(self, folder):
        extracted_directory = self.get_extracted_directory(folder)
        if os.path.exists(extracted_directory):
            shutil.rmtree(extracted_directory)

    def download(self, folder):
        gzip_path = self._confirm_valid_gzip_file_or_download(folder)
        self._clean_extracted_directory(folder)
        tools.unzip(gzip_path)


class BasicSdl(conans.ConanFile):
    name = "basic-sdl"
    version = "2.0.8"
    license = ""
    author = ""
    description = "A basic version of the SDL2 libraries"

    settings = "os", "compiler", "build_type", "arch"

    requires = tuple()

    options = {
        "shared": [True, False],
        "sdl2main": [True, False],
    }
    default_options = {
        "shared": False,
        # Emulating what Bincrafters choose, probably by user's requests.
        # I wish I knew why anyone in their right mind would want this.
        "sdl2main": True
    }

    _gzip_downloader = GzipDownloader(
        base_name='SDL2-2.0.8',
        url="https://www.libsdl.org/release/SDL2-2.0.8.tar.gz",
        md5_sum="3800d705cef742c6a634f202c37f263f"
    )

    def source(self):
        self._gzip_downloader.download(self.source_folder)

    def build(self):
        src = self._gzip_downloader.get_extracted_directory(self.source_folder)
        with tools.chdir(self.build_folder):
            atools = conans.AutoToolsBuildEnvironment(self)
            atools.configure(configure_dir=src)
            atools.make()
            atools.install()

    def package(self):
        built_packages = os.path.join(self.build_folder, "package")
        self.copy("*", src=built_packages)


    # Stole some of this from the Bincrafters code.
    @staticmethod
    def _chmod_plus_x(filename):
        if os.name == "posix":
            os.chmod(filename, os.stat(filename).st_mode | 0o111)

    def package_info(self):
        sdl2_config = os.path.join(self.package_folder, "bin", "sdl2-config")
        self._chmod_plus_x(sdl2_config)
        self.output.info("Creating SDL2_CONFIG environment variable: %s" % sdl2_config)
        self.env_info.SDL2_CONFIG = sdl2_config
        self.output.info("Creating SDL_CONFIG environment variable: %s" % sdl2_config)
        self.env_info.SDL_CONFIG = sdl2_config
        self.cpp_info.libs = [lib for lib in tools.collect_libs(self) if "2.0" not in lib]
        if not self.options.sdl2main:
            self.cpp_info.libs = [lib for lib in self.cpp_info.libs]
        else:
            # ensure that SDL2main is linked first
            sdl2mainlib = "SDL2main"
            # if self.settings.build_type == "Debug":
            #     sdl2mainlib = "SDL2maind"
            self.cpp_info.libs.insert(0, self.cpp_info.libs.pop(self.cpp_info.libs.index(sdl2mainlib)))
        self.cpp_info.includedirs.append(os.path.join("include", "SDL2"))
        # if self.settings.os == "Linux":
        #     self.cpp_info.system_libs.extend(["dl", "rt", "pthread"])
        #     if self.options.jack:
        #         self._add_libraries_from_pc("jack")
        #     if self.options.sndio:
        #         self._add_libraries_from_pc("sndio")
        #     if self.options.nas:
        #         self.cpp_info.libs.append("audio")
        #     if self.options.esd:
        #         self._add_libraries_from_pc("esound")
        #     if self.options.directfb:
        #         self._add_libraries_from_pc("directfb")
        #     if self.options.video_rpi:
        #         self.cpp_info.libs.append("bcm_host")
        #         self.cpp_info.includedirs.extend(["/opt/vc/include",
        #                                           "/opt/vc/include/interface/vcos/pthreads",
        #                                           "/opt/vc/include/interface/vmcs_host/linux"])
        #         self.cpp_info.libdirs.append("/opt/vc/lib")
        #         self.cpp_info.sharedlinkflags.append("-Wl,-rpath,/opt/vc/lib")
        #         self.cpp_info.exelinkflags.append("-Wl,-rpath,/opt/vc/lib")
        # elif self.settings.os == "Macos":
        #     self.cpp_info.frameworks.extend(["Cocoa", "Carbon", "IOKit", "CoreVideo", "CoreAudio", "AudioToolbox", "ForceFeedback"])
        # elif self.settings.os == "Windows":
        #     self.cpp_info.system_libs.extend(["user32", "gdi32", "winmm", "imm32", "ole32", "oleaut32", "version", "uuid", "advapi32", "setupapi", "shell32"])
        #     if self.settings.compiler == "gcc":
        #         self.cpp_info.system_libs.append("mingw32")
        self.cpp_info.names["cmake_find_package"] = "SDL2"
        self.cpp_info.names["cmake_find_package_multi"] = "SDL2"
