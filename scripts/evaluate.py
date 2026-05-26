---
file_type: python
version: 1.0.0
---

# Evaluation metric computation module
# Follows the evaluation protocol defined in documentation

import json
import os
from pathlib import Path
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.metrics import accuracy_score, f1_score

# Label mapping
LABELS = ['Negative', 'Neutral', 'Positive']
LABEL_CODES = {label: idx for idx, label in enumerate(LABELS)}

# Classification report mapping
def generate_report(y_true, y_pred):
    """Generate metrics in the standard reporting format per protocol definition."""
    report = {
        'accuracy': accuracy_score(y_true, y_pred).round(4),
        'precision_macro': f1_score(y_true, y_pred, average='macro').round(4),
        'recall_macro': f1_score(y_true, y_pred, average='macro').round(4),
        'f1_macro': f1_score(y_true, y_pred, average='macro').round(4),
        'confusion_matrix': confusion_matrix(y_true, y_pred).tolist()
    }
    
    # Per-class metrics
    per_class = classification_report(y_true, y_pred, zero_division=0).split('\n')[2:-2]
    per_class = [line.split() for line in per_class]
    
    # Convert to standardized format
    for i in range(len(LABELS)):
        report[f'precision_{LABELS[i]}'] = per_class[i][1].round(4)
        report[f'recall_{LABELS[i]}'] = per_class[i][2].round(4)
        report[f'f1_{LABELS[i]}'] = per_class[i][3].round(4)
    
    return report

# Main metrics computation function

def compute_metrics(y_true, y_pred):
    """Compute all metrics according to evaluation protocol."""
    report = generate_report(y_true, y_pred)
    
    # Validate targets
    accuracy = report['accuracy']
    precision_macro = report['precision_macro']
    recall_macro = report['recall_macro']
    f1_macro = report['f1_macro']
    
    # Check thresholds
    targets_met = {
        'accuracy_test': accuracy >= 0.85,
        'precision_macro_target': precision_macro >= 0.83,
        'recall_macro_target': recall_macro >= 0.83,
        'f1_macro_target': f1_macro >= 0.83
    }
    
    # Calculate weighted F1 if needed
    # Add weighted metrics calculation here if required by protocol
    
    return {
        'metrics': report,
        'targets_met': targets_met,
        'validation_status': all(targets_met.values())
    }

# Helper function for saving results

def save_evaluation_results(results, experiment_id):
    """Save results to standardized format."""
    output_dir = Path(f'reports/{experiment_id}')
    output_dir.mkdir(exist_ok=True)
    
    # Save JSON metrics
    json_report = {
        'experiment_id': experiment_id,
        **results
    }
    with open(output_dir / 'metrics.json', 'w') as f:
        json.dump(json_report, f, indent=2)
    
    # Save classification report
    with open(output_dir / 'classification_report.txt', 'w') as f:
        f.write(report_to_text(report))
