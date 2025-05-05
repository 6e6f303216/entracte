{
  description = "Performing on stage is an unbroken flow of actions";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";

  outputs = { self, nixpkgs }:
    let
      system = "x86_64-linux";
      pkgs = import nixpkgs {
        inherit system;
      };
      pythonEnv = pkgs.python312.withPackages (ps: with ps; [
        psutil
        pyqt6
        pyqt6-sip
        pyinstaller
      ]);
    in {
      devShells.${system}.default = pkgs.mkShell {
        name = "entracte-dev-shell";

        buildInputs = [
          pythonEnv
          pkgs.binutils  
          pkgs.pulseaudio 
        ];

        shellHook = ''
          echo "🐍 Welcome to Entracte Dev Shell"
          echo "💡 Run: pyinstaller main.spec"
        '';
      };

      packages.${system}.default = pkgs.stdenv.mkDerivation {
        name = "entracte-build";
        src = ./.;

        nativeBuildInputs = [ pythonEnv pkgs.python312Packages.pyinstaller ];

        buildPhase = ''
          pyinstaller main.spec
        '';

        installPhase = ''
          mkdir -p $out
          cp -r dist/* $out/
        '';
      };
    };
}
