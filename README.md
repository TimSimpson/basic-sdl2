
# basic-sdl2

This is a basic version of the SDL2 libraries. They're designed as a drop in replacement for BinCrafter's SDL2 libraries in situations where building those isn't worth the complexity.

## Motivation

The BinCrafter's libraries are excellent, and the SDL2 libs are no exception. However because of the philosophical decision to try to build all optional components of the SDL2 libraries by default, and to rely on Conan packages rather than system ones, there have been times where I've found myself having to compile the universe just to get a simple Hello World app working. Most recently I was bit while trying to build a 32 bit application; I found Conan trying and failing to compile the xorg package.

I don't want to get into an argument about whether or not Conan / BinCrafter's decision to do things a certain way is _correct_, as history has shown me it usually is, but there are times and situations where going through so much trouble just to compile the SDL2 libs is, in my opinion, not worth it.

## Usage

This is designed to be a drop in replacement for the SDL2 libraries by BinCrafters. Of course, if you build a package which depends on this, then every package which depends on your package will try to use my goofy version of SDL2 instead of the BinCrafter's ones. I don't recommend that.

Instead, add an option which will make your package rely on `basic-sdl2` instead of Bincrafter's SDL2. Then, in certain situations, you can set this option in your build profile to bypass building the Bincrafter's SDL2 packages and all of its dependencies if it turns out to be an endless nightmare.

## How it works on Linux

The Conanfile downloads the SDL2 source code, runs `configure` and `make`... and that's it. It should go without saying that the version of SDL2 produced will rely on certain packages being installed first using your system package manager, such as `apt-get`.

## How it works on Windows

It literally just downloads the prebuilt libraries. How lazy is that?
