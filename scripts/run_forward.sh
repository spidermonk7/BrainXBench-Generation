#!/bin/bash
echo " ===================== Forward Benchmarking ===================== "
echo "🚀 Step 1: Running data collector"
python collector.py 

echo " ===================== Selection & Validation & Segmentation ===================== "
echo "📦 Step 2-3: (1) Select:[[Journal Source & Pub Date]] (2) Validate (3) Segment abstract to 3 sections"
python generate_forward.py --stage S_V_S

echo " ===================== Data Flipping ===================== "
echo "🎯 Step 4: Flip the result section"
python generate_forward.py --stage flip

echo " ===================== Data Validation ===================== "
echo "🔍 Step 5: Validate the flipped results"
python generate_forward.py --stage validate

echo " ===================== Data Benchmarking ===================== "
echo "📦 Step 6: Build up benchmark files and pack them up into json | csv | parquet"
python build_bench.py -T forward -B BrainX-20JFM                                                                                                                                                                                                                                                                                 JFM

echo "✅ All steps completed!"
echo " ===================== Forward Benchmarking Completed ===================== "