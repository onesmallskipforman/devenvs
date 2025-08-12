{
  description = "A flake that provides nixpkgs outputs with custom packages";
  inputs.nix-ros-overlay.url = "github:lopsided98/nix-ros-overlay/master";
  inputs.nixpkgs.follows = "nix-ros-overlay/nixpkgs";  # IMPORTANT!!!
  # TODO: not sure if needed
  inputs.nixgl.url = "github:nix-community/nixGL";

  outputs = { self, nixpkgs, nix-ros-overlay, nixgl }:
  let
    system = "x86_64-linux";
    pkgs = import nixpkgs {
      inherit system;
      config.allowUnfree = true;
      overlays = [
        nix-ros-overlay.overlays.default
        nixgl.overlay
      ];
    };

    devShells.${system}.default = pkgs.mkShell {
      name = "ROS Project";
      packages = with pkgs; [
          tio
          minicom
          picocom
          python313Packages.digi-xbee
          python313Packages.zigpy-xbee
          # pkgs.nixgl.auto.nixGLDefault

          # ros
          (with pkgs.rosPackages.jazzy; buildEnv {
            paths = [
              ros-core
              plotjuggler
              plotjuggler-ros
              ros2cli
              ros2bag
              ros2topic
              ros2node
              ros2param
              ros2run
              ros2pkg
            ];
          })
      ];
    };

  in
  { inherit devShells; };
  nixConfig = {
    extra-substituters = [ "https://ros.cachix.org" ];
    extra-trusted-public-keys = [ "ros.cachix.org-1:dSyZxI8geDCJrwgvCOHDoAfOm5sV1wCPjBkKL+38Rvo=" ];
  };
}
