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
        (siglo.override { python3 = python-with-distutils; })
        itd
      ];
    };
  in
  { inherit devShells; };
}
