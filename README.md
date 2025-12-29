# 🚪 OTPdoor

[![PyPI version](https://img.shields.io/pypi/v/otpdoor.svg)](https://pypi.org/project/otpdoor/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Versions](https://img.shields.io/pypi/pyversions/otpdoor.svg)](https://pypi.org/project/otpdoor/)

**OTPdoor** is a premium, lightweight Python authentication backend designed specifically for **Nginx `auth_request`**. It provides a modern, glassmorphic UI for TOTP (Time-based One-Time Password) entry, allowing you to protect any application behind Nginx with industry-standard 2FA in minutes.

---

## ✨ Key Features

-   **🌐 Multi-Domain Support**: Protect multiple independent applications with a single OTPdoor instance. Each domain has its own secret, session length, and theme.
-   **💎 Premium UI**: Modern, glassmorphic login interface with support for **Light** and **Dark** modes.
-   **📱 Mobile Ready**: 6-digit segmented input optimized for mobile numeric keypads.
-   **⚙️ Runtime Config**: A dedicated `/_config` portal (protected by CLI flag) to generate secrets and manage session durations on the fly.
-   **🚀 Production Grade**: Powered by **Waitress**, ensuring stable and high-performance WSGI delivery.
-   **🔒 Security Focused**:
    -   AES-128 encrypted session cookies (Fernet).
    -   Customizable cookie security (Secure, HttpOnly, SameSite).
    -   Persistent JSON-based configuration.

---

## 🚀 Quick Start

### 1. Installation
```shell
pip install otpdoor
```

### 2. Basic Configuration
Export the two essential environment variables to get started with the `default` domain:
```shell
# Your 16-character Base32 secret (or generate one with --add-domain)
export OPTDOOR_TOTP_SECRET="BASE32SECRET3232"

# A secure key for encrypting cookies (e.g., from `cryptography.fernet.Fernet.generate_key()`)
export OPTDOOR_COOKIE_SECRET="your-fernet-key-here"
```

### 3. Launch the Server
```shell
# Run without -c in production. Use -c only to access /_config for setup.
python -m otpdoor -a 127.0.0.1 -p 8080
```

---

## 🏢 Multi-Domain Management

OTPdoor is designed to scale. You can manage distinct "domains" from the CLI:

```shell
# Create a new domain for your internal tool
python -m otpdoor --add-domain internal_site

# List all configured domains
python -m otpdoor --list-domains
```

Access domain-specific configuration or login pages by adding `?domain=name` to the URL.

---

## 🛰️ Nginx Integration

The most common use case for OTPdoor is as an external authenticator for Nginx.

### Sample Configuration
```nginx
upstream otpdoor_backend {
    server 127.0.0.1:8080;
}

server {
    listen 80;
    server_name myapp.example.com;

    location / {
        # 1. Direct auth check
        auth_request /_check;
        error_page 401 = @error401;
        
        proxy_pass http://your_app_backend;
    }

    # 2. Internal check endpoint (passes domain context)
    location = /_check {
        internal;
        proxy_pass http://otpdoor_backend/_check?domain=myapp;
        proxy_pass_request_body off;
        proxy_set_header Content-Length "";
    }

    # 3. Authentication page
    location /_auth {
        proxy_pass http://otpdoor_backend/_auth?domain=myapp;
        proxy_set_header Host $host;
    }

    # 4. Redirect to login on 401
    location @error401 {
        return 302 $scheme://$http_host/_auth?domain=myapp&originator=$request_uri;
    }
}
```

---

## 🛠️ Configuration Reference

Settings can be managed via environment variables:

| Variable | Description | Default |
| :--- | :--- | :--- |
| `OPTDOOR_TOTP_SECRET` | Primary secret for the `default` domain. | `BASE32SECRET3232` |
| `OPTDOOR_COOKIE_SECRET` | Key used for session encryption. | `super-secret-key` |
| `OPTDOOR_CONFIG_FILE` | Path to persistent domain storage. | `optdoor_config.json` |
| `OPTDOOR_SESSION_DURATION`| Session length in seconds. | `86400` (1 Day) |
| `OPTDOOR_THEME` | Default UI theme (`dark` or `light`). | `dark` |
| `OPTDOOR_COOKIE_SECURE` | Enforce HTTPS for cookies. | `true` |

---

## 📄 License

OTPdoor is released under the **MIT License**. See [LICENSE](LICENSE) for more details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---
*Created with ❤️ by [German Espinosa](https://github.com/germanespinosa)*
