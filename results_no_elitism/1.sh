#!/bin/bash

# Check if the current shell is bash
if [ -z "$BASH_VERSION" ]; then
  echo "This script requires bash. Please run it with bash."
  exit 1
fi

folder_path=(
  "200_1000_bs_10_50_8_rpmxo_rim_1_10_30_0"
  "200_1000_bs_10_50_8_rpmxo_rrm_1_10_30_0"
  "200_1000_bs_10_50_8_rpmxo_rsm_1_10_30_0"
  "200_1000_bs_10_50_8_rspxo_rrm_1_10_30_0"
  "200_1000_bs_10_50_8_rspxo_rsm_1_10_30_0"
  "200_1000_bs_10_50_8_rspxo_rim_1_10_30_0"
  "200_1000_bs_10_50_8_uxo_rrm_1_10_30_0"
  "200_1000_bs_10_50_8_uxo_rsm_1_10_30_0"
  "200_1000_bs_10_50_8_uxo_rim_1_10_30_0"
  "200_1000_fps_10_50_8_rpmxo_rrm_1_10_30_0"
  "200_1000_fps_10_50_8_rpmxo_rsm_1_10_30_0"
  "200_1000_fps_10_50_8_rpmxo_rim_1_10_30_0"
  "200_1000_fps_10_50_8_rspxo_rrm_1_10_30_0"
  "200_1000_fps_10_50_8_rspxo_rsm_1_10_30_0"
  "200_1000_fps_10_50_8_rspxo_rim_1_10_30_0"
  "200_1000_fps_10_50_8_uxo_rrm_1_10_30_0"
  "200_1000_fps_10_50_8_uxo_rsm_1_10_30_0"
  "200_1000_fps_10_50_8_uxo_rim_1_10_30_0"
  "200_1000_ts_10_50_8_rpmxo_rrm_1_10_30_0"
  "200_1000_ts_10_50_8_rpmxo_rsm_1_10_30_0"
  "200_1000_ts_10_50_8_rpmxo_rim_1_10_30_0"
  "200_1000_ts_10_50_8_rspxo_rrm_1_10_30_0"
  "200_1000_ts_10_50_8_rspxo_rsm_1_10_30_0"
  "200_1000_ts_10_50_8_rspxo_rim_1_10_30_0"
  "200_1000_ts_10_50_8_uxo_rrm_1_10_30_0"
  "200_1000_ts_10_50_8_uxo_rsm_1_10_30_0"
  "200_1000_ts_10_50_8_uxo_rim_1_10_30_0"
  )

for folder in "${folder_path[@]}"; do
  # Ensure the script is run in the desired directory
  cd $folder_path || exit

  echo "Processing folder: $folder"

  # Initialize previous time and previous file variables
  previous_time=0
  previous_file=""

  # Loop through each file in the directory
  for file in *; do
    if [ -f "$file" ]; then
      # Get the creation time of the file
      creation_time=$(stat --format="%W" "$file")
      if [ "$creation_time" -ne -1 ]; then
        # Calculate and display the time difference if a previous file exists
        if [ "$previous_time" -ne 0 ]; then
          time_diff=$((creation_time - previous_time))
          echo "Time difference between $previous_file and $file: $time_diff seconds"
        fi
        # Update the previous time and file variables
        previous_time=$creation_time
        previous_file=$file
      else
        echo "Creation time not available for $file"
      fi
    fi
  done

  # Move back to the parent directory
  cd ..
done