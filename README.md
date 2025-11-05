# dotctrl

#### Description
Fully automated environment setup using Ansible — designed for consistent, repeatable, and modular configuration across systems.

#### 📖 Usage

**Installation**

This playbook includes a custom shell script located at `bin/dotctrl`.  
Run it to automatically install all required dependencies and start the Ansible setup process:

```bash
bash -c "$(curl -fsSL https://raw.githubusercontent.com/mbriesemeister/dotctrl/main/bin/dotctrl)"
```

Alternatively, you can clone the repository and run the script manually:

```bash
chmod +x bin/dotctrl
```
```bash
./bin/dotctrl
```

The script handles package installation, environment preparation, and triggers the Ansible playbook to configure your system.
