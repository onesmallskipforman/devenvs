{
  description = "A flake that provides nixpkgs outputs with custom packages";
  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";

  outputs = { self, nixpkgs }:
  let
    system = "x86_64-linux";
    # using import so i can configure nix
    # pkgs = nixpkgs.legacyPackages.${system};
    pkgs = import nixpkgs { inherit system; config.allowUnfree = true; };

    devShells.${system}.default = pkgs.mkShell {
      packages = with pkgs; [
        bear
        clang-tools
        cmake
        codespell
        conan
        cppcheck
        doxygen
        gdb
        gtest
        lcov
        vcpkg
        vcpkg-tool

        # arm
        gcc-arm-embedded
        stm32flash
      ];
    };

  in
  { inherit devShells; };
}
