{
  description = "A flake that provides nixpkgs outputs with custom packages";
  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
  inputs.nocture = {
    url = "https://github.com/usenocturne/nocturne/releases/download/v3.0.0/nocturne_image_v3.0.0.zip";
    flake = false;
  };
  inputs.flashthing = {
    url = "https://github.com/JoeyEamigh/flashthing/releases/download/v0.1.5/flashthing-cli-linux-x86_64";
    flake = false;
  };

  outputs = { self, nixpkgs }:
  let
    system = "x86_64-linux";
    # using import so i can configure nix
    # pkgs = nixpkgs.legacyPackages.${system};
    pkgs = import nixpkgs { inherit system; config.allowUnfree = true; };

    devShells.${system}.default = pkgs.mkShell {
      packages = with pkgs; [
          # pyamlboot
          # chromium # for terbium.app
          # TODO: need to download
          # https://github.com/bishopdynamics/superbird-tool
          # https://github.com/usenocturne/nocturne/releases/download/v3.0.0/nocturne_image_v3.0.0.zip
      ];
    };

  in
  { inherit devShells; };
}
