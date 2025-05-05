{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = with pkgs; [
    python312
    python312Packages.pyqt6
    python312Packages.pyqt6-sip
    python312Packages.pyinstaller
    pulseaudio
  ];
}
