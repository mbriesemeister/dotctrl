# dotctrl

#### Description
Fully automated environment setup using Ansible, designed for consistent, repeatable, and modular configuration across systems.

#### 📖 Usage

**Installation**

This playbook includes a custom shell script located at `bin/dotctrl`.  
Run it to automatically install all required dependencies and start the Ansible setup process:

```bash
bash -c "$(curl -fsSL https://raw.githubusercontent.com/mbriesemeister/dotctrl/main/bin/dotctrl-base)"
```

Alternatively, you can clone the repository and run the script manually:

```bash
chmod +x bin/dotctrl-base
```
```bash
./bin/dotctrl-base
```

The script handles package installation, environment preparation, and triggers the Ansible playbook to configure your system.

---

## Execution Control (Tags & Extra Vars)

### Tags (`-t`)
You can target specific roles or components instead of running the entire playbook by passing tags via `-t` (or `--tags`):

```bash
# Run only the lazygit role
ansible-playbook playbooks/dotctrl.yml -t lazygit -K
```

### Extra Vars (`-e`)
Control which phase of the selected roles is executed by passing extra variables via `-e`:

* `-e only_config=true`
* `-e only_install=true`

| Variable | Executed Tasks |
| :--- | :--- |
| *(none)* | Full run (Installation & Configuration) |
| `only_config=true` | Configuration only |
| `only_install=true` | Installation only |
| Both set to `true` | Nothing (skips all tasks) |

### Combined Examples
Combine tags and extra vars for granular control over your setup:

```bash
# Apply only the configuration for Waybar
ansible-playbook playbooks/dotctrl.yml -t waybar -e only_config=true -K

# Run only the installation for Waybar
ansible-playbook playbooks/dotctrl.yml -t waybar -e only_install=true -K
```

---