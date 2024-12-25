#!/usr/bin/env bash

pushd "$APP_DIR" &> /dev/null

if [ ! -d ".venv" ]; then
  echo "[ Pre Launcher | Warning ] Could not find venv. Using system installation"
  launch_command="python3 main.py $@"
else
  launch_command=".venv/bin/python3 main.py $@"
fi

$launch_command

popd &> /dev/null
