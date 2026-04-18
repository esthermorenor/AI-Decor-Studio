#!/usr/bin/env python3
"""Servidor local para visualizar AI Decor Studio."""

from __future__ import annotations

import argparse
import http.server
import socketserver
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
WEB_DIR = BASE_DIR / "web"
DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 4173


class ReusableTCPServer(socketserver.TCPServer):
    allow_reuse_address = True


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Inicia un servidor local para abrir la app en tu navegador."
    )
    parser.add_argument("--host", default=DEFAULT_HOST, help=f"Host (default: {DEFAULT_HOST})")
    parser.add_argument(
        "--port", type=int, default=DEFAULT_PORT, help=f"Puerto (default: {DEFAULT_PORT})"
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Valida que la carpeta web exista y termina sin iniciar servidor.",
    )
    return parser


def main() -> None:
    args = build_parser().parse_args()

    if not WEB_DIR.exists():
        raise SystemExit("No se encontró la carpeta 'web'.")

    if args.check:
        print(f"OK: contenido detectado en {WEB_DIR}")
        return

    handler = http.server.SimpleHTTPRequestHandler

    print("🚀 AI Decor Studio en local")
    print(f"📁 Sirviendo archivos desde: {WEB_DIR}")
    print(f"🌐 URL: http://{args.host}:{args.port}")
    print("(Ctrl+C para detener)")

    with ReusableTCPServer((args.host, args.port), lambda *a, **kw: handler(*a, directory=str(WEB_DIR), **kw)) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServidor detenido.")


if __name__ == "__main__":
    main()
