# Changelog

All notable changes to Gateway-Ripper will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-11-14

### Added
- Initial release of Gateway-Ripper
- Web crawling and JavaScript extraction
- Payment gateway detection (Stripe, Braintree, Checkout.com, PayPal, Square, Razorpay, Mollie)
- API key extraction
- Configuration extraction
- Python code generation for Stripe
- Python code generation for Braintree
- CLI interface with argument parsing
- Colored console output
- Verbose logging mode
- Output file support
- Comprehensive documentation (README, INSTALL, EXAMPLES, CONTRIBUTING)
- MIT License
- Test demo files

### Features
- Automatic gateway fingerprinting
- Confidence scoring for detections
- Multi-gateway support
- Test card information
- Error handling and validation
- URL normalization
- SSL warning suppression

### Supported Gateways
- ✅ Stripe (Full support)
- ✅ Braintree (Full support)
- 🚧 Checkout.com (Detection only)
- 🚧 PayPal (Detection only)
- 🚧 Square (Detection only)
- 🚧 Razorpay (Detection only)
- 🚧 Mollie (Detection only)

## [Unreleased]

### Planned
- Code generation for remaining gateways
- GraphQL payment API support
- Cryptocurrency gateway support
- Web UI
- Automated testing framework
- Mobile app payment flow analysis
- Plugin system for custom gateways

---

[1.0.0]: https://github.com/yourusername/gateway-ripper/releases/tag/v1.0.0
