#!/bin/bash
echo " ===================== Forward Benchmarking ===================== "
echo "🚀 Step 1: Split PDF data and generate questions"
python generate_backward.py 

echo " ===================== Build up benchmark files and pack them up into json | csv | parquet ===================== "
echo "📦 Step 2: Build up benchmark files and pack them up into json | csv | parquet"
python build_bench.py -T backward -B BrainX-Koch-hard