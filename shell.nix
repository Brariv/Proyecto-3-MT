{ pkgs, ... }:
let
  pipyPackages = pkgs.pypy3Packages;
in
pkgs.mkShell {
  buildInputs = with pipyPackages; [
    graphviz
    pprintpp
    pkgs.pyright
  ];
}
