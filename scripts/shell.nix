{ pkgs ? import <nixpkgs> {} }:
pkgs.mkShell {
    packages = with pkgs; [
        python3
        pyright
        postgresql
        python3Packages.numpy
    ];
}
