build:
    #!/usr/bin/env bash
    cd sources
    python build_sprite.py

    cp *.css ../docs/
    cp *.html ../docs/
    cp *.js ../docs/

run:
    python -m http.server --directory docs --bind 127.0.0.1 8080