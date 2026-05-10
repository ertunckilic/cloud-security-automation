# MFA Best Practices - AWS Security

## What is MFA?

Multi-Factor Authentication (MFA) requires two or more methods to verify identity:
- **Something you know**: Password
- **Something you have**: Phone, hardware token
- **Something you are**: Biometric (fingerprint)

## Why MFA Matters

- 99.9% of attacks are prevented with MFA
- Protects against password breaches
- Essential for IAM users with AWS console access
- Required for production environments

## MFA Types in AWS

### 1. Virtual MFA Devices
- **Apps**: Google Authenticator, Microsoft Authenticator, Authy
- **Cost**: Free
- **Pros**: Easy to set up, portable
- **Cons**: Phone loss = access lost

### 2. Hardware MFA Devices
- **Types**: U2F keys, hardware tokens
- **Cost**: $50-150
- **Pros**: Most secure, backup options
- **Cons**: More expensive

### 3. SMS MFA (Not Recommended)
- **Cons**: Vulnerable to SIM swapping, interception

## MFA Setup Steps

1. Open AWS Console → Security Credentials
2. Click "Assign MFA device"
3. Choose "Virtual MFA device"
4. Scan QR code with authenticator app
5. Enter two consecutive codes
6. Store backup codes safely

## MFA Policy Implementation

The `mfa-policy.json` enforces:

- Users MUST have MFA to perform actions
- Users CAN set up MFA without MFA (bootstrap)
- Users CANNOT bypass MFA
- Root account MUST have MFA

## Best Practices

✅ **DO:**
- Enable MFA for root account
- Enforce MFA for all IAM users
- Use virtual MFA on multiple devices
- Store backup codes in secure location
- Rotate MFA devices periodically

❌ **DON'T:**
- Share MFA codes
- Use SMS for MFA
- Rely on only one MFA device
- Disable MFA
- Store codes in plaintext

## Backup Codes

When setting up MFA:
1. Save backup codes to secure location
2. Print and store in safe
3. Use only if phone is lost
4. Generate new codes after using backup codes

## MFA Recovery

If you lose your phone:
1. Use backup codes
2. Contact AWS Support
3. Use alternate MFA device
4. Remove and re-setup MFA

## Compliance & Standards

- **AWS Well-Architected**: Requires MFA
- **SOC 2**: Requires MFA for privileged access
- **PCI-DSS**: Requires MFA for remote access
- **ISO 27001**: Requires strong authentication

## Account ID
- **AWS Account**: 054037138082
- **MFA Device**: arn:aws:iam::054037138082:mfa/Authapp
- **Setup Date**: Sep 04 2025

## References
- [AWS MFA Documentation](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_mfa.html)
- [AWS Security Best Practices](https://aws.amazon.com/architecture/security-identity-compliance/)
