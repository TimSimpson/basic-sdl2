
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
    name = "basic-sdl2"
    version = "2.0.9"
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
        base_name='SDL2-2.0.9',
        url="https://www.libsdl.org/release/SDL2-2.0.9.tar.gz",
        md5_sum="f2ecfba915c54f7200f504d8b48a5dfe"
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
            # BinCrafter's does the following. Maybe I'm not building this
            # thing correctly?
            # if self.settings.build_type == "Debug":
            #     sdl2mainlib = "SDL2maind"
            self.cpp_info.libs.insert(0, self.cpp_info.libs.pop(self.cpp_info.libs.index(sdl2mainlib)))
        self.cpp_info.includedirs.append(os.path.join("include", "SDL2"))

        # Bincrafter's version establishes a million library dependencies here.

        self.cpp_info.names["cmake_find_package"] = "SDL2"
        self.cpp_info.names["cmake_find_package_multi"] = "SDL2"
