#!/bin/bash
echo " ===================== Forward Benchmarking ===================== "
echo "🚀 Step 1: Running data collector"
python collector.py 

echo " ===================== Selection & Validation & Segmentation ===================== "
echo "📦 Step 2-3: (1) Select:[[Journal Source & Pub Date]] (2) Validate (3) Segment abstract to 3 sections"
python validate_and_segment.py

echo " ===================== Data Flipping ===================== "
echo "🎯 Step 4: Flip the result section"
python flip_result.py

echo " ===================== Data Validation ===================== "
echo "🔍 Step 5: Validate the flipped results"
python validate_flip.py

echo " ===================== Data Benchmarking ===================== "
echo "📦 Step 6: Build up benchmark files and pack them up into json | csv | parquet"
python build_bench.py

echo "✅ All steps completed!"
echo " ===================== Forward Benchmarking Completed ===================== "