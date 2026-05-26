#!/usr/bin/env python3
"""Test script to validate reproducibility policy artifacts."""
import os
import yaml

def test_reproducibility_docs_exist():
    """Test that reproducibility-policy.md exists."""
    assert os.path.exists('docs/reproducibility-policy.md'), "Missing reproducibility-policy.md"
    content = open('docs/reproducibility-policy.md').read()
    assert len(content) > 200, "reproducibility-policy.md too small"
    assert 'Random Seed Configuration' in content, "Missing Random Seed section"
    assert 'Artifacts Wajib Disimpan' in content, "Missing artifacts section"
    assert 'Dependency Locking' in content, "Missing dependency locking section"
    print('[PASS] test_reproducibility_docs_exist')

def test_requirements_exists():
    """Test that requirements.txt exists and contains key dependencies."""
    assert os.path.exists('requirements.txt'), "Missing requirements.txt"
    content = open('requirements.txt').read()
    assert 'numpy' in content, "Missing numpy in requirements"
    assert 'pandas' in content, "Missing pandas in requirements"
    assert 'scikit-learn' in content, "Missing scikit-learn in requirements"
    assert 'google-play-scraper' in content, "Missing google-play-scraper in requirements"
    assert 'python>=' in content, "Missing python version constraint"
    print('[PASS] test_requirements_exists')

if __name__ == "__main__":
    test_reproducibility_docs_exist()
    test_requirements_exists()
    print("\nAll reproducibility policy tests passed!")