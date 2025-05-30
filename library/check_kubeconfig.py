#!/usr/bin/python

from ansible.module_utils.basic import AnsibleModule
import os


def main():
    module = AnsibleModule(argument_spec={})

    # Get KUBECONFIG environment variable
    kubeconfig_path = os.environ.get("KUBECONFIG")

    if not kubeconfig_path:
        module.fail_json(
            msg="❌ The KUBECONFIG environment variable is not set."
        )

    # Check if file exists
    if not os.path.isfile(kubeconfig_path):
        module.fail_json(
            msg=f"❌ The KUBECONFIG file does not exist at: {kubeconfig_path}.",
            kubeconfig_path=kubeconfig_path
        )

    # Check if file is readable
    try:
        with open(kubeconfig_path, "r") as f:
            f.readline()  # Try reading a line to verify access
    except Exception as e:
        module.fail_json(
            msg=f"❌ The KUBECONFIG file exists but is not readable: {str(e)}",
            kubeconfig_path=kubeconfig_path
        )

    module.exit_json(
        changed=False,
        msg=f"✅ KUBECONFIG is set, the file exists, and is readable at: {kubeconfig_path}.",
        kubeconfig_path=kubeconfig_path
    )


if __name__ == "__main__":
    main()
