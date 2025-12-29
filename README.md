# <img src="https://github.com/germanespinosa/otpdoor/blob/main/logo.png?raw=true" width="48" height="48" valign="middle"> OTPdoor

[![PyPI version](https://img.shields.io/pypi/v/otpdoor.svg)](https://pypi.org/project/otpdoor/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**OTPdoor** is a premium, lightweight Python authentication backend designed specifically for **Nginx `auth_request`**. Protect any application behind Nginx with industry-standard 2FA in minutes using a modern, glassmorphic UI.

---

## ✨ Key Features

-   **🌐 Browser-First Setup**: Install and configure everything from your browser.
-   **🔒 Encrypted Storage**: All TOTP secrets are stored AES-encrypted in your configuration file.
-   **🏢 Multi-Domain Support**: Manage independent applications with separate secrets, sessions, and themes from a single portal.
-   **🛡️ Protected Config**: The configuration portal is secured by the `default` domain's 2FA.
-   **💎 Premium UI**: Modern glassmorphic interface with **Light** and **Dark** modes.
-   **🚀 Production Grade**: Powered by **Waitress** for high-performance WSGI delivery.

---

## 🚀 Quick Start

### 1. Install
```shell
pip install otpdoor
```

### 2. Launch
Provide a secret key for cookie encryption and start in configuration mode:
```shell
export OTPDOOR_COOKIE_SECRET="your-secure-key"
python -m otpdoor -c
```

### 3. Setup via Browser
1.  Go to `http://localhost:8080/_config`.

> [!WARNING]
> **CRITICAL SECURITY STEP**: Login with the default secret **`BASE32SECRET3232`** and immediately click **"Generate New Secret"** for the `default` domain. Using the well-known default secret in production is extremely dangerous.

*   *Scan this QR for quick access:*  
    ![Default QR](https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=otpauth%3A%2F%2Ftotp%2FOTPdoor%3Aadmin%3Fsecret%3DBASE32SECRET3232%26issuer%3DOTPdoor)

4.  Use the **"Create New Domain"** section to protect other apps.

> [!NOTE]
> Accessing any configuration now requires you to be logged into the `default` domain.

---

## 🛰️ Nginx Integration

Protect your apps by passing the `domain` parameter in the `auth_request`:

```nginx
location / {
    auth_request /_check;
    error_page 401 = @error401;
    proxy_pass http://your_app;
}

location = /_check {
    internal;
    proxy_pass http://otpdoor_backend/_check?domain=myapp;
}

location @error401 {
    return 302 $scheme://$http_host/_auth?domain=myapp&originator=$request_uri;
}
```

---

## 🛠️ Configuration Reference

| Variable | Description | Default |
| :--- | :--- | :--- |
| `OTPDOOR_COOKIE_SECRET` | Key for session & config encryption. | `super-secret-key` |
| `OTPDOOR_CONFIG_FILE` | Path to encrypted domain storage. | `otpdoor_config.json` |
| `OTPDOOR_TOTP_SECRET` | Initial fallback secret (use `BASE32SECRET3232`). | `BASE32SECRET3232` |
| `OTPDOOR_THEME` | Default UI theme (`dark` or `light`). | `dark` |

---

## 📄 License
Released under the **MIT License**.

---
*Created with ❤️ by [German Espinosa](https://github.com/germanespinosa)*
