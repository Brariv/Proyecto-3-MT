{ pkgs, ... }:
let
  pipyPackages = pkgs.pypy3Packages;
in
pkgs.mkShell {
  buildInputs = with pipyPackages; [
    pyyaml
    pkgs.pyright
  ];
}
