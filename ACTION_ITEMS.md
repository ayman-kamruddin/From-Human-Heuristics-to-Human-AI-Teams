# Action Items for Repository Publication

**Status**: Phase 1 Complete - Ready for Review
**Date**: 2025-09-30

---

## Immediate Actions (Before Paper Submission)

### Critical (Do This Week) ⚠️

- [ ] **1. Review All Documentation**
  - Read through `README_NEW.md` for accuracy
  - Verify all code paths in `CODE_TO_PAPER_MAPPING.md`
  - Check data column definitions in `DATA_README.md`
  - Confirm figure numbers match manuscript

- [ ] **2. Replace Core Files** (BACKUP FIRST!)
  ```bash
  # Backup originals
  cp README.md README_OLD.md
  cp .gitignore .gitignore_old

  # Replace with new versions
  mv README_NEW.md README.md
  mv .gitignore_new .gitignore
  ```

- [ ] **3. Update GitHub URL Placeholders**
  - Search for `[Repository URL]` in all markdown files
  - Replace with actual GitHub repository URL
  - Files to update:
    - README.md (multiple locations)
    - CODE_TO_PAPER_MAPPING.md
    - DATA_README.md

- [ ] **4. Verify Mendeley Data Link**
  - Confirm DOI is correct: `https://data.mendeley.com/datasets/kpxp5zkh5f/2`
  - Update version number if needed
  - Check that data package structure matches documentation

- [ ] **5. Test Quick Start on Clean Machine**
  - Use a colleague's computer or VM
  - Follow EXACTLY the steps in README.md quick start
  - Document any issues found
  - Time the process (should be < 10 minutes to start)

### Important (Do Before Submission) 📝

- [ ] **6. Match Figure Numbers to Paper**
  - Open final manuscript PDF
  - Verify figure numbering:
    - Figure 2: Task environment ✓ (no code changes needed)
    - Figure 3: Example trajectories → `exp1_BinaryTrace_Analysis.ipynb`
    - Figure 4 (top): Target selection Exp1 → `exp1_TSOverlap_Analysis.ipynb`
    - Figure 4 (bottom): Binary trace Exp1 → `exp1_BinaryTrace_Analysis.ipynb`
    - Figure 5 (top): Target selection Exp2 → `exp2_TargetOverlap_Analysis.ipynb`
    - Figure 5 (bottom): Binary trace Exp2 → `exp2_BinaryTrace_Analysis.ipynb`
  - Update `figure_config.yaml` if numbering changed

- [ ] **7. Update Citation Information**
  - Replace `[Manuscript submitted for publication]` with journal name if accepted
  - Add DOI if available
  - Update author affiliations if changed

- [ ] **8. Add LICENSE File**
  - Consult with lab/institution policy
  - Recommend: MIT License or CC-BY-4.0
  - Create `LICENSE` file in root directory

- [ ] **9. Create GitHub Release**
  - Tag version 1.0 matching paper submission
  - Include release notes summarizing repository contents
  - Link to Mendeley Data in release description

---

## Recommended Enhancements (Do After Submission) 🎯

### High Priority

- [ ] **10. Fix Cross-Platform Path Issues**
  - Review `get_actual_TS_Dynamic_Policy_as_csv.py` lines 24, 134-143
  - Replace `\\` with `pathlib.Path` operations
  - Test on Windows, macOS, and Linux
  - Files to update:
    - `get_actual_TS_Dynamic_Policy_as_csv.py`
    - `get_actual_Dynamic_Policy_as_csv_Human-AA.py`
    - Any other scripts with hardcoded paths

- [ ] **11. Implement Figure Configuration Helper**
  ```python
  # Create Scripts/utils/figure_helper.py
  import yaml
  import matplotlib.pyplot as plt

  def apply_figure_config(fig_name):
      """Apply standardized figure configuration"""
      with open('figure_config.yaml') as f:
          config = yaml.safe_load(f)
      # ... implementation ...
  ```

- [ ] **12. Create Master Configuration File**
  ```python
  # Create Scripts/config.py
  from pathlib import Path

  PROJECT_ROOT = Path(__file__).parent.parent
  DATA_DIR = PROJECT_ROOT / "RAW_EXPERIMENT_DATA"
  RESULTS_DIR = PROJECT_ROOT / "OtherResults"
  # ... etc ...
  ```

### Medium Priority

- [ ] **13. Add Data Validation Script**
  ```python
  # Create Scripts/validate_data.py
  # Checks:
  # - Correct number of sessions
  # - Expected file count per session
  # - CSV format validation
  # - Column completeness
  ```

- [ ] **14. Create Figure Generation Script**
  ```python
  # Create Scripts/generate_all_figures.py
  # Runs all notebooks programmatically
  # Exports figures in multiple formats
  # Verifies against figure_config.yaml
  ```

- [ ] **15. Reorganize Script Directory**
  ```
  Scripts/
  ├── experiment_1/
  │   ├── 01_compute_target_selection.py
  │   ├── 02_compute_dtw_overlap.py
  │   ├── 03_compute_binary_traces.py
  │   └── 04_statistical_analysis.R
  ├── experiment_2/
  │   └── ... (similar structure)
  └── utils/
      ├── figure_helper.py
      └── data_validation.py
  ```

---

## Testing Checklist ✅

### Before Replacing Files

- [ ] Run `python -m py_compile` on all .py files
- [ ] Check YAML validity: `python -c "import yaml; yaml.safe_load(open('Scripts/figure_config.yaml'))"`
- [ ] Verify all markdown links work (use a linter)
- [ ] Spell-check all documentation

### After Replacing Files

- [ ] Verify Git status shows expected changes
- [ ] Test one complete analysis pipeline (Exp1 or Exp2)
- [ ] Check that figures are generated successfully
- [ ] Confirm statistical analyses run without errors

---

## Communication Plan 📢

### With Co-Authors

- [ ] **Email Draft** (to send to co-authors):
  ```
  Subject: Repository Refactoring Complete - Action Required

  Dear colleagues,

  I've completed Phase 1 refactoring of our code repository for the
  "From Human Heuristics to Human-AI Teams" paper. The repository is
  now reviewer-ready with comprehensive documentation.

  **Key Improvements**:
  - Complete README with 3-command quick start
  - Code-to-paper mapping document
  - Comprehensive data dictionary
  - Standardized figure configuration
  - Dependency management (requirements.txt)

  **Action Required from You**:
  1. Review new documentation for accuracy (especially your sections)
  2. Test the quick start guide on your machine
  3. Verify figure numbers match the final manuscript
  4. Approve changes before I push to GitHub

  **Files to Review**:
  - README_NEW.md (primary documentation)
  - CODE_TO_PAPER_MAPPING.md (links code to paper)
  - DATA_README.md (data format documentation)

  Please review by [DATE] so we can finalize before submission.

  Best,
  [Your name]
  ```

### With Journal

- [ ] **Supplementary Materials Statement**:
  ```
  "All data and code required to reproduce the analyses and figures
  in this manuscript are publicly available. Raw experimental data
  are deposited at Mendeley Data (DOI: 10.17632/kpxp5zkh5f.2).
  Complete analysis code, including step-by-step reproduction
  instructions, is available at https://github.com/[YOUR-ORG]/
  From-Human-Heuristics-to-Human-AI-Teams."
  ```

---

## Timeline Estimate ⏱️

**Immediate Actions (Critical)**: 2-3 hours
- File review: 1 hour
- Testing: 1-2 hours
- Updates: 30 minutes

**Important Actions**: 2-3 hours
- Figure verification: 1 hour
- Citation updates: 30 minutes
- GitHub setup: 1-1.5 hours

**Total Time to Publication-Ready**: **4-6 hours**

---

## Success Criteria 🎯

Repository is publication-ready when:

✅ **Documentation**
- [ ] A reviewer can clone and reproduce results independently
- [ ] Quick start guide takes < 10 minutes
- [ ] Every paper figure mapped to code
- [ ] Data format fully documented

✅ **Code Quality**
- [ ] All scripts run without errors
- [ ] Figures match paper exactly
- [ ] Cross-platform compatibility (or documented workarounds)
- [ ] Dependencies specified

✅ **Accessibility**
- [ ] README is clear and concise
- [ ] Examples work out-of-the-box
- [ ] Troubleshooting guide addresses common issues
- [ ] License specified

✅ **Reproducibility**
- [ ] External reviewer confirms reproduction
- [ ] All analysis outputs match expected values
- [ ] Statistical results match paper

---

## Support Resources 🆘

### If You Get Stuck

1. **Documentation Issues**
   - Re-read relevant section in `REFACTORING_SUMMARY.md`
   - Check examples in `CODE_TO_PAPER_MAPPING.md`

2. **Technical Issues**
   - Review `DATA_README.md` for data format
   - Check `requirements.txt` for dependencies
   - See troubleshooting in `README.md`

3. **Need Help?**
   - Consult original `Scripts/README.md` for legacy instructions
   - Review paper methods section for scientific context
   - Ask co-authors for clarification

---

## Notes

- Keep `README_OLD.md` and `.gitignore_old` as backups
- Don't delete any existing files until repository is proven working
- Test on multiple platforms if possible (Windows, Mac, Linux)
- Consider asking a colleague unfamiliar with the project to test the quick start

---

## Version History

- **v1.0** (2025-09-30): Phase 1 complete - Documentation and configuration
- **v1.1** (Planned): Phase 2 - Code organization
- **v2.0** (Future): Full automation with master pipeline script

---

*Good luck with the paper submission! 🚀*