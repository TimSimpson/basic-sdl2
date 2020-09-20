
# basic-sdl2

[![Travis Build Status](https://travis-ci.org/TimSimpson/basic-sdl2.svg?branch=master)](https://travis-ci.org/TimSimpson/basic-sdl2)
[ ![Download](https://api.bintray.com/packages/timsimpson/richter/basic-sdl2%3ATimSimpson/images/download.svg) ](https://bintray.com/timsimpson/richter/basic-sdl2%3ATimSimpson/_latestVersion)


A basic version of the SDL2 packages. It's designed as a drop in replacement for BinCrafter's SDL2 libraries in situations where building those may introduce too much complexity, or in cases where it's preferable to use a version you compiled yourself.

This recipe is extremely simple and just calls autoconfig / make.

As of today, the libraries end up being built as shared, even if this is disabled in your profile (there are static libs but they only contain function pointers to the real ones). This is typically how the SDL2 libraries are used.

## Version Number

The version number matches BinCrafter's and the actual SDL2 except it's prefixed with a `b`. So SDL2 2.0.9 is `b2.0.9`.


## Motivation

The BinCrafter's SDL2 packages are excellent, but they involve some complexity. For instance, by default they require dozens of other Conan packages rather than rely on the system packages that are already present.

I don't want to get into an argument about whether or not Conan / BinCrafter's decision to do things a certain way is _correct_, as history has shown me it usually is. In fact I'd recommend in most cases just using the BinCrafter's packages and moving on.

But, if they're giving you hell, you can always try these.

## How it works

The Conanfile downloads the SDL2 source code, runs `configure` and `make`... and that's it. It should go without saying that the version of SDL2 produced will rely on certain packages being installed first using your system package manager, such as `apt-get`.

I've got plans to eventually make the recipe download the prebuilt Windows binaries from the official SDL2 site. For now it probably doesn't work on Windows.

## Usage

This tries to mimic the BinCrafters packages where possible, but of course by it's nature there are limits. If you build a package which depends on this, then every package which depends on your package will try to use this goofy version of SDL2 instead of the BinCrafter's ones. I don't recommend that.

Instead, add an option which will make your package rely on `basic-sdl2` instead of Bincrafter's SDL2. Then, in certain situations, you can set this option in your build profile to bypass building the Bincrafter's SDL2 packages and all of its dependencies if it turns out to be an hassle.
