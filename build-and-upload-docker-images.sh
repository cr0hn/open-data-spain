#!/usr/bin/env bash

VERSION=$(poetry version -s)

echo "[*] Building and uploading docker image for version $VERSION"
docker build -t ods .

if [ $? -ne 0 ]; then
    echo "[!] Error building docker image"
    exit 1
fi

echo "[*] Tagging and pushing docker image for version $VERSION"
docker tag ods "registry-k3s.gorriato.eu/ods:$VERSION"

if [ $? -ne 0 ]; then
    echo "[!] Error tagging docker image"
    exit 1
fi

echo "[*] Pushing docker image for version $VERSION"
docker push "registry-k3s.gorriato.eu/ods:$VERSION"

if [ $? -ne 0 ]; then
    echo "[!] Error pushing docker image"
    exit 1
fi
