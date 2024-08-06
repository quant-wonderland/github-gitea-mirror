{
  description = "The toolkits of devops.";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-23.11";

    nixpkgs-unstable.url = "github:NixOS/nixpkgs/nixos-unstable";

    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, nixpkgs-unstable, ... }@inputs:
    {
      overlays.default = nixpkgs.lib.composeManyExtensions [
        # inputs.numpandas.overlays.default
        (final: prev: {
          pythonPackagesExtensions = prev.pythonPackagesExtensions ++ [
            (py-final: py-prev: {
              github-gitea-mirror = py-final.callPackage ./default.nix { };
            })
          ];
        })
      ];
    } // inputs.flake-utils.lib.eachSystem [ "x86_64-linux" ] (system:
      let
        pkgs = import nixpkgs {
          inherit system;
          config.allowUnfree = true;
          overlays = [ self.overlays.default ];
        };

        pkgs-unstable = import nixpkgs-unstable {
          inherit system;
          config.allowUnfree = true;
        };

        pythonForDevops =
          pkgs.python3.withPackages (pyPkgs: with pyPkgs; [ pygithub ]);

      in {
        # Some of the python tools are developed and packaged with poetry.
        devShells.default = pkgs.mkShell rec {
          name = "deveops-tools";
          packages = with pkgs; [
            poetry
            pkgs-unstable.rclone
            pythonForDevops
            nodePackages.pyright
          ];
          shellHook = ''
            export CONFIG_JSON_PATH="/home/twl/workspace/github-gitea-mirror/src"
          '';
        };

        packages = {
          github-gitea-mirror = pkgs.python3Packages.github-gitea-mirror;
        };
      });
}
