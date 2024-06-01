#!/bin/bash

# List of folders to process
csv_files_path=(
  "/200_1000_bs_10_50_8_rpmxo_rim_1_10_30_0"
  "200_1000_bs_10_50_8_rpmxo_rsm_1_10_30_0"
  "200_1000_bs_10_50_8_rpmxo_rim_1_10_30_0"
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

# Function to calculate time differences in a single folder
calculate_time_diff() {
  local folder="$1"
  echo "Processing folder: $folder"

  previous_time=0
  previous_file=""

  # Loop through each file in the folder
  for file in "$folder"/*; do
    if [ -f "$file" ]; then
      creation_time=$(stat --format="%W" "$file")
      if [ "$creation_time" -ne -1 ]; then
        if [ "$previous_time" -ne 0 ]; then
          time_diff=$((creation_time - previous_time))
          echo "Time difference between $previous_file and $file: $time_diff seconds"
        fi
        previous_time=$creation_time
        previous_file=$file
      else
        echo "Creation time not available for $file"
      fi
    fi
  done

  echo
}

# Process each folder in the list
for folder in "${folders[@]}"; do
  echo "Hello"
  if [ -d "$folder" ]; then
    calculate_time_diff "$folder"
  else
    echo "Directory not found: $folder"
  fi
done
