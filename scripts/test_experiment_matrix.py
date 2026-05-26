#!/usr/bin/env python3
"""Test script to validate experiment matrix design artifacts."""
import yaml
import csv
import os

def test_experiment_matrix_exists():
    """Test that experiment-matrix.md exists and is non-empty."""
    path = "docs/experiment-matrix.md"
    assert os.path.exists(path), f"{path} does not exist"
    content = open(path).read()
    assert len(content) > 100, f"{path} is too small ({len(content)} chars)"
    # Check required sections
    assert "Experiment Configuration Table" in content, "Missing experiment table"
    assert "EXP-01" in content and "EXP-05" in content, "Missing experiment rows"
    print("[PASS] test_experiment_matrix_exists")

def test_minimal_3_models():
    """Test that at least 3 different models are defined."""
    path = "docs/experiment-matrix.md"
    content = open(path).read()
    models = [
        "Logistic Regression",
        "Linear SVM",
        "IndoBERT",
    ]
    found = [m for m in models if m in content]
    assert len(found) >= 3, f"Only {len(found)} models found: {found}"
    print(f"[PASS] test_minimal_3_models ({len(found)} models)")

def test_experiment_config_valid_yaml():
    """Test that experiment-config.yaml is valid YAML."""
    path = "docs/experiment-config.yaml"
    assert os.path.exists(path), f"{path} does not exist"
    with open(path) as f:
        config = yaml.safe_load(f)
    assert "experiments" in config, "Missing 'experiments' key"
    experiments = config["experiments"]
    assert isinstance(experiments, list), "experiments should be a list"
    assert len(experiments) >= 3, f"Only {len(experiments)} experiments defined (need >= 3)"
    # Verify each experiment has required fields
    for exp in experiments:
        assert "id" in exp, f"Missing 'id' in experiment {exp}"
        assert "model" in exp, f"Missing 'model' in experiment {exp['id']}"
        assert "feature_extraction" in exp, f"Missing 'feature_extraction' in {exp['id']}"
        assert "targets" in exp, f"Missing 'targets' in {exp['id']}"
    print(f"[PASS] test_experiment_config_valid_yaml ({len(experiments)} experiments)")

def test_model_selection_criteria():
    """Test that model selection criteria meet minimum thresholds."""
    path = "docs/experiment-matrix.md"
    content = open(path).read()
    # Check accuracy threshold >= 85% is mentioned
    assert ">= 85%" in content or ">=0.85" in content, "Missing minimum accuracy threshold"
    # Check F1-score criteria
    assert "F1" in content or "f1" in content, "Missing F1 criteria"
    print("[PASS] test_model_selection_criteria")

def test_all_experiments_have_targets():
    """Test that all experiments define accuracy and F1 targets."""
    path = "docs/experiment-config.yaml"
    with open(path) as f:
        config = yaml.safe_load(f)
    for exp in config["experiments"]:
        targets = exp.get("targets", {})
        assert "accuracy_testing" in targets, f"Missing accuracy_testing in {exp['id']}"
        assert "f1_macro" in targets, f"Missing f1_macro in {exp['id']}"
    print("[PASS] test_all_experiments_have_targets")

if __name__ == "__main__":
    tests = [
        test_experiment_matrix_exists,
        test_minimal_3_models,
        test_experiment_config_valid_yaml,
        test_model_selection_criteria,
        test_all_experiments_have_targets,
    ]
    passed = 0
    failed = 0
    for t in tests:
        try:
            t()
            passed += 1
        except Exception as e:
            print(f"[FAIL] {t.__name__}: {e}")
            failed += 1
    print(f"\nResults: {passed} passed, {failed} failed out of {len(tests)} tests")
