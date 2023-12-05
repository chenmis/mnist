#!/usr/bin/env bash

function is_gnu_sed(){
  sed --version >/dev/null 2>&1
}

PROTOS_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

python3 -m grpc_tools.protoc -I "${PROTOS_DIR}" --python_out="${PROTOS_DIR}" --grpc_python_out="${PROTOS_DIR}" "${PROTOS_DIR}"/mnist.proto

# Use Sed-replace to fix a known import issue: https://github.com/protocolbuffers/protobuf/issues/1491#issuecomment-438138293
if is_gnu_sed; then
  cd "${PROTOS_DIR}" && sed -i -E 's/^import.*_pb2/from . &/g' ./*pb2*.py
else
  cd "${PROTOS_DIR}" && sed -i '' -E 's/^import.*_pb2/from . &/g' ./*pb2*.py
fi
