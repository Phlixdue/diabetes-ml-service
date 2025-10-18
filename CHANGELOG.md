# Changelog

All notable changes to this project will be documented in this file.

## [0.2.0] - 2025-10-18

### Changed
- Switched the regression model from `LinearRegression` to `Ridge` (alpha=1.0).
- **Reason**: To improve model generalization and robustness through L2 regularization, which helps prevent overfitting.

### Performance
| Version | Model               | Test RMSE |
|---------|---------------------|-----------|
| v0.1    | LinearRegression    | 53.85     |
| v0.2    | Ridge               | **53.78** |

---

## [0.1.0] - 2025-10-18

### Added
- Initial release of the Diabetes Prediction API.
- Baseline model using `StandardScaler` and `LinearRegression`.
- CI/CD pipeline with GitHub Actions for automated testing and releases.