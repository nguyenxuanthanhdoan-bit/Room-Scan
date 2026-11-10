import argparse
import json
import numpy as np

def calculate_metrics(predicted_dims: dict, ground_truth_dims: dict):
    """
    Computes Mean Absolute Error (MAE) and percentage error against laser ground truth.
    """
    errors = {}
    for key in ["width", "length", "height", "area"]:
        pred = predicted_dims.get(key, 0.0)
        gt = ground_truth_dims.get(key, 0.0)
        abs_err = abs(pred - gt)
        pct_err = (abs_err / gt) * 100 if gt > 0 else 0.0
        errors[key] = {
            "predicted": pred,
            "ground_truth": gt,
            "absolute_error": round(abs_err, 3),
            "percentage_error": round(pct_err, 2)
        }
    return errors

def main():
    print("=== RoomScan AI Ground Truth Benchmark Evaluator ===")
    print("Comparing AI pipeline predictions against Bosch/Leica Laser distance ground truth...")
    
    # Sample evaluation demo
    gt = {"width": 3.82, "length": 4.25, "height": 2.80, "area": 16.23}
    pred = {"width": 3.85, "length": 4.20, "height": 2.80, "area": 16.17}
    
    metrics = calculate_metrics(pred, gt)
    print(json.dumps(metrics, indent=2))

if __name__ == "__main__":
    main()
