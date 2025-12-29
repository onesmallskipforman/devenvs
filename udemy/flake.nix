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
          python313
          python313Packages.numpy
          python313Packages.matplotlib
      ];
      #
      # shellHook = ''
      #     export LD_LIBRARY_PATH=${pkgs.stdenv.cc.cc.lib}/lib:$LD_LIBRARY_PATH
      #   '';
    };

  in
  { inherit devShells; };
}
