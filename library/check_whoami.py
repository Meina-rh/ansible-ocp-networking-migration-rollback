#!/usr/bin/python
from ansible.module_utils.basic import AnsibleModule
import time


def run_command_with_retries(module, command, retries=3, delay=3):
    """Execute a shell command with retries on failure."""
    for attempt in range(retries):
        rc, stdout, stderr = module.run_command(command)

        if rc == 0:
            return stdout.strip(), None  # Success

        if attempt < retries - 1:
            module.warn(f"Retrying in {delay} seconds due to error: {stderr.strip()}")
            time.sleep(delay)  # Wait before retrying
        else:
            return None, f"Command failed after {retries} attempts: {stderr.strip()}"

    return None, "Unknown error"


def check_cluster_admin(module):
    """Check if the current user has cluster-admin rights."""
    # Get current user
    user_command = "oc whoami"
    user, error = run_command_with_retries(module, user_command)

    if error:
        return None, f"Failed to execute `{user_command}`. Ensure `oc` client is configured correctly."

    # Check if the user can perform all actions (indicating cluster-admin rights)
    check_admin_command = "oc auth can-i '*' '*' --all-namespaces"
    admin_rights, error = run_command_with_retries(module, check_admin_command)

    if error:
        return None, f"Failed to verify cluster-admin rights. Error: {error}"

    # If the user is system:admin OR has full privileges
    if "yes" in admin_rights or user == "system:admin":
        return user, None
    return user, "User does not have `cluster-admin` rights."


def run_module():
    module = AnsibleModule(argument_spec={})

    user, error = check_cluster_admin(module)

    if error:
        module.fail_json(msg=f"Current user `{user}` does not have `cluster-admin` rights. {error}")

    module.exit_json(changed=False, message=f"User `{user}` has `cluster-admin` privileges.")


if __name__ == "__main__":
    run_module()
