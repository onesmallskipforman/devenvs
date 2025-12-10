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
        texlive.combined.scheme-full
        texlab
        tectonic
        zathura
        inkscape # for latex drawings
        enscript # converts textfile to postscript (use with ps2pdf)
        entr     # run arbitrary commands when files change, for live edit
        ghostscript # installs ps2pdf
      ];
    };

  in
  { inherit devShells; };
}
