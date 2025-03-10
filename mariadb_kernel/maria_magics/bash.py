"""This class implements the %%bash magic command"""

help_text = """
The %%bash magic command has the following syntax:
    > %%bash [bash commands]
The %%bash magic command allows you to execute bash commands in the notebook environment.

Any bash command that can be executed from the command line can be used with %%bash.
You can execute commands like file manipulation, system calls, etc., directly from the notebook.

If you need to run multiple lines of bash commands, you can do so by including them inside the cell.

The output of the bash commands will be displayed after execution.
"""

from mariadb_kernel.maria_magics.line_magic import LineMagic
import subprocess

class Bash(LineMagic):
    def __init__(self, args):
        self.args_list = args.strip()

    def name(self):
        return "%%bash"

    def help(self):
        return help_text

    def execute(self, kernel, data):
        # Execute the bash command using subprocess
        try:
            result = subprocess.run(self.args_list, shell=True, capture_output=True, text=True)
            output = result.stdout
            error_output = result.stderr

            if result.returncode != 0:
                kernel._send_message("stderr", f"Error executing bash command:\n{error_output}")
                return

            # If the command runs successfully, send the output
            display_content = {
                "data": {"text/html": f"<pre>{output}</pre>"},
                "metadata": {},
            }
            kernel.send_response(kernel.iopub_socket, "display_data", display_content)
        except Exception as e:
            kernel._send_message("stderr", f"An error occurred while executing the bash command: {str(e)}")
