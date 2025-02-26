# app/koyeb_cli.py
import subprocess
import logging

class KoyebCLI:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def _run_command(self, command):
        """Run a shell command and return the output."""
        try:
            result = subprocess.run(
                command,
                shell=True,
                check=True,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            return result.stdout
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Command failed: {e.stderr}")
            return f"Error: {e.stderr}"
        except Exception as e:
            self.logger.error(f"Unexpected error: {str(e)}")
            return f"Unexpected error: {str(e)}"

    def get_logs(self, service_name):
        """Fetch logs for a Koyeb service."""
        command = f"koyeb service logs {service_name}"
        return self._run_command(command)

    def redeploy(self, service_name):
        """Trigger a redeploy for a Koyeb service."""
        command = f"koyeb service redeploy {service_name}"
        return self._run_command(command)

    def list_services(self):
        """List all Koyeb services."""
        command = "koyeb service list"
        return self._run_command(command)
