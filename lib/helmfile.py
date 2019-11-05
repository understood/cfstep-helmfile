import os
import sys
import subprocess

def run_command(helmfile_command):
    proc = subprocess.Popen(full_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output = proc.communicate()
    print(output)
    if proc.returncode != 0:
        sys.exit(1)
    return b''.join(output).strip().decode()  # only save stdout into output, ignore stderr

# def create_global_options_list(global_options):
#     print(global_options)
#     options = []
#     option_list = ''
#     global_options_dict = dict(x.split(' ') for x in global_options.split(';'))
#     for key, value in global_options_dict.items():
#         options.append("{} {}".format(key, value))
#         option_list = ' '.join(options)
#     return option_list

def main():

    # Take in Variables from Environment

    # Command List Executed in Order Provided
    commands = os.getenv('COMMANDS')

    # Global Options

    helm_binary = os.getenv('HELM_BINARY')
    helm_file = os.getenv('FILE')
    environment = os.getenv('ENVIRONMENT')
    state_values_set = os.getenv('STATE_VALUES_SET')
    state_values_file = os.getenv('STATE_VALUES_FILE')
    quiet = os.getenv('QUIET')
    kube_context = os.getenv('KUBE_CONTEXT')
    log_level = os.getenv('LOG_LEVEL')
    namespace = os.getenv('NAMESPACE')
    selector = os.getenv('SELECTOR')
    allow_no_matching_release = os.getenv('ALLOW_NO_MATCHING_RELEASE')
    interactive = os.getenv('INTERACTIVE')
    helm_help = os.getenv('HELP')
    version = os.getenv('VERSION')

    # Combine Global Options

    global_options = []

    if helm_binary:
        global_options.append("--helm_binary %s"%(helm_binary))
    if helm_file:
        global_options.append("--file %s"%(helm_file))
    if environment:
        global_options.append("--environment %s"%(environment))
    if state_values_set:
        global_options.append("--state-values-set %s"%(state_values_set))
    if state_values_file:
        global_options.append("--state-values-file %s"%(state_values_file))
    if quiet: 
        global_options.append("--quiet")
    if kube_context:
        global_options.append("--kube-context %s"%(kube_context))
    if log_level:
        global_options.append("--log-level %s"%(log_level))
    if namespace:
        global_options.append("--namespace %s"%(namespace))
    if selector:
        global_options.append("--selector %s"%(selector))
    if allow_no_matching_release:
        global_options.append("--allow-no-matching-release")
    if interactive: 
        global_options.append("--interactive")
    if helm_help: 
        global_options.append("--help")
    if version: 
        global_options.append("--version")

    global_options_list = ' '.join(global_options)

    # GLOBAL OPTIONS:
    #    --helm-binary value, -b value           path to helm binary
    #    --file helmfile.yaml, -f helmfile.yaml  load config from file or directory. defaults to helmfile.yaml or `helmfile.d`(means `helmfile.d/*.yaml`) in this preference
    #    --environment default, -e default       specify the environment name. defaults to default
    #    --state-values-set value                set state values on the command line (can specify multiple or separate values with commas: key1=val1,key2=val2)
    #    --state-values-file value               specify state values in a YAML file
    #    --quiet, -q                             Silence output. Equivalent to log-level warn
    #    --kube-context value                    Set kubectl context. Uses current context by default
    #    --log-level value                       Set log level, default info
    #    --namespace value, -n value             Set namespace. Uses the namespace set in the context by default, and is available in templates as {{ .Namespace }}
    #    --selector value, -l value              Only run using the releases that match labels. Labels can take the form of foo=bar or foo!=bar.
    #                                            A release must match all labels in a group in order to be used. Multiple groups can be specified at once.
    #                                            --selector tier=frontend,tier!=proxy --selector tier=backend. Will match all frontend, non-proxy releases AND all backend releases.
    #                                            The name of a release can be used as a label. --selector name=myrelease
    #    --allow-no-matching-release             Do not exit with an error code if the provided selector has no matching releases.
    #    --interactive, -i                       Request confirmation before attempting to modify clusters
    #    --help, -h                              show help
    #    --version, -v                           print the version

    # Command Options

    # deps command

    deps_args = os.getenv('DEPS_ARGS')
    deps_skip_repos = os.getenv('DEPS_SKIP_REPOS')

    # OPTIONS:
    # --args value                   pass args to helm exec
    # --skip-repos helm repo update  skip running helm repo update before running `helm dependency build`

    dep_options = []

    if deps_args: 
        dep_options.append("--arg %s"%(deps_args))
    if deps_skip_repos:
        dep_options.append("--skip-repos")

    dep_options_list = ' '.join(dep_options)

    # repos command

    repos_args = os.getenv('REPOS_ARGS')

    # OPTIONS:
    # --args value  pass args to helm exec

    repos_options = []

    if repos_args: 
        repos_options.append("--arg %s"%(repos_args))

    repos_options_list = ' '.join(repos_options)

    # diff command

    diff_args = os.getenv('DIFF_ARGS')
    diff_set = os.getenv('DIFF_SET')
    diff_values = os.getenv('DIFF_VALUES')
    diff_skip_deps = os.getenv('DIFF_SKIP_DEPS')
    diff_detailed_exitcode = os.getenv('DIFF_DETAILED_EXITCODE')
    diff_suppress_secrets = os.getenv('DIFF_SUPRESS_SECRETS')
    diff_concurrency = os.getenv('DIFF_CONCURRENCY')
    diff_context = os.getenv('DIFF_CONTEXT')

    # OPTIONS:
    # --args value                  pass args to helm exec
    # --set value                   additional values to be merged into the command
    # --values value                additional value files to be merged into the command
    # --skip-deps helm repo update  skip running helm repo update and `helm dependency build`
    # --detailed-exitcode           return a non-zero exit code when there are changes
    # --suppress-secrets            suppress secrets in the output. highly recommended to specify on CI/CD use-cases
    # --concurrency value           maximum number of concurrent helm processes to run, 0 is unlimited (default: 0)
    # --context value               output NUM lines of context around changes (default: 0)

    diff_options = []

    if diff_args: 
        diff_options.append("--arg %s"%(diff_args))
    if diff_set: 
        diff_options.append("--set %s"%(diff_set))
    if diff_values: 
        diff_options.append("--values %s"%(diff_values))
    if diff_skip_deps:
        diff_options.append("--skip-deps")
    if diff_detailed_exitcode:
        diff_options.append("--detailed-exitcode")
    if diff_suppress_secrets:
        diff_options.append("--suppress-secrets")
    if diff_concurrency:
        diff_options.append("--concurrency %s"%(diff_concurrency))
    if diff_context:
        diff_options.append("--context %s"%(diff_context))

    diff_options_list = ' '.join(diff_options)

    # template command

    template_args = os.getenv('TEMPLATE_ARGS')
    template_set = os.getenv('TEMPLATE_SET')
    template_values = os.getenv('TEMPLATE_VALUES')
    template_output_dir = os.getenv('TEMPLATE_SUPRESS_SECRETS')
    template_concurrency = os.getenv('TEMPLATE_CONCURRENCY')
    template_skip_deps = os.getenv('TEMPLATE_SKIP_DEPS')

    # OPTIONS:
    # --args value                  pass args to helm template
    # --set value                   additional values to be merged into the command
    # --values value                additional value files to be merged into the command
    # --output-dir value            output directory to pass to helm template (helm template --output-dir)
    # --concurrency value           maximum number of concurrent downloads of release charts (default: 0)
    # --skip-deps helm repo update  skip running helm repo update and `helm dependency build`

    template_options = []

    if template_args: 
        template_options.append("--arg %s"%(template_args))
    if template_set: 
        template_options.append("--set %s"%(template_set))
    if template_values: 
        template_options.append("--values %s"%(template_values))
    if template_output_dir:
        template_options.append("--output-dir %s"%(template_output_dir))
    if template_concurrency:
        template_options.append("--concurrency %s"%(template_concurrency))
    if template_skip_deps:
        template_options.append("--skip-deps")

    template_options_list = ' '.join(template_options)

    # lint

    lint_args = os.getenv('LINT_ARGS')
    lint_set = os.getenv('LINT_SET')
    lint_values = os.getenv('LINT_VALUES')
    lint_concurrency = os.getenv('LINT_CONCURRENCY')
    lint_skip_deps = os.getenv('LINT_SKIP_DEPS')
    
    # OPTIONS:
    # --args value                  pass args to helm exec
    # --set value                   additional values to be merged into the command
    # --values value                additional value files to be merged into the command
    # --concurrency value           maximum number of concurrent downloads of release charts (default: 0)
    # --skip-deps helm repo update  skip running helm repo update and `helm dependency build`

    lint_options = []

    if template_args: 
        template_options.append("--arg %s"%(template_args))
    if template_set: 
        template_options.append("--set %s"%(template_set))
    if template_values: 
        template_options.append("--values %s"%(lint_values))
    if lint_concurrency:
        lint_options.append("--concurrency %s"%(lint_concurrency))
    if lint_skip_deps:
        lint_options.append("--skip-deps")

    lint_options_list = ' '.join(lint_options)

    # sync

    sync_set = os.getenv('SYNC_SET')
    sync_values = os.getenv('SYNC_VALUES')
    sync_concurrency = os.getenv('SYNC_CONCURRENCY')
    sync_args = os.getenv('SYNC_ARGS')
    sync_skip_deps = os.getenv('SYNC_SKIP_DEPS')
    
    # OPTIONS:
    # --set value                   additional values to be merged into the command
    # --values value                additional value files to be merged into the command
    # --concurrency value           maximum number of concurrent helm processes to run, 0 is unlimited (default: 0)
    # --args value                  pass args to helm exec
    # --skip-deps helm repo update  skip running helm repo update and `helm dependency build`

    # apply

    apply_set = os.getenv('APPLY_SET')
    apply_values = os.getenv('APPLY_VALUES')
    apply_concurrency = os.getenv('APPLY_CONCURRENCY')
    apply_context = os.getenv('APPLY_CONTEXT')
    apply_args = os.getenv('APPLY_ARGS')
    apply_suppress_secrets = os.getenv('APPLY_SUPPRESS_SECRETS')  
    apply_skip_deps = os.getenv('APPLY_SKIP_DEPS')

    # OPTIONS:
    # --set value                   additional values to be merged into the command
    # --values value                additional value files to be merged into the command
    # --concurrency value           maximum number of concurrent helm processes to run, 0 is unlimited (default: 0)
    # --context value               output NUM lines of context around changes (default: 0)
    # --args value                  pass args to helm exec
    # --suppress-secrets            suppress secrets in the diff output. highly recommended to specify on CI/CD use-cases
    # --skip-deps helm repo update  skip running helm repo update and `helm dependency build`

    # status command

    status_concurrency = os.getenv('STATUS_CONCURRENCY')
    status_args = os.getenv('STATUS_ARGS')

    # OPTIONS:
    # --concurrency value  maximum number of concurrent helm processes to run, 0 is unlimited (default: 0)
    # --args value         pass args to helm exec

    # delete command

    delete_concurrency = os.getenv('DELETE_CONCURRENCY')
    delete_args = os.getenv('DELETE_ARGS')
    delete_purge = os.getenv('DELETE_PURGE')

    # OPTIONS:
    # --concurrency value  maximum number of concurrent helm processes to run, 0 is unlimited (default: 0)
    # --args value         pass args to helm exec
    # --purge              purge releases i.e. free release names and histories

    # destroy command

    destroy_concurrency = os.getenv('DESTROY_CONCURRENCY')
    destroy_args = os.getenv('DESTROY_ARGS')

    # OPTIONS:
    # --concurrency value  maximum number of concurrent helm processes to run, 0 is unlimited (default: 0)
    # --args value         pass args to helm exec

    # test command

    test_cleanup = os.getenv('TEST)_CLEANUP')
    test_args = os.getenv('TEST_ARGS')
    test_timeout = os.getenv('TEST_TIMEOUT')
    test_concurrency = os.getenv('TEST_CONCURRENCY')

    # Combine Options

    test_options = []

    # OPTIONS:
    # --cleanup            delete test pods upon completion
    # --args value         pass additional args to helm exec
    # --timeout value      maximum time for tests to run before being considered failed (default: 300)
    # --concurrency value  maximum number of concurrent helm processes to run, 0 is unlimited (default: 0)

    # Loop through helmfile commands from COMMANDS array

    for command in commands:
        command_list = "%s_options_list"%(command)
        command_options_list = command_list
        helmfile_command = "helmfile %s %s %s"%(global_options_list, command, command_options_list)
        print(helmfile_command)
        #run_command(helmfile_command)

    # COMMANDS:
    #      deps      update charts based on the contents of requirements.yaml
    #      repos     sync repositories from state file (helm repo add && helm repo update)
    #      charts    DEPRECATED: sync releases from state file (helm upgrade --install)
    #      diff      diff releases from state file against env (helm diff)
    #      template  template releases from state file against env (helm template)
    #      lint      lint charts from state file (helm lint)
    #      sync      sync all resources from state file (repos, releases and chart deps)
    #      apply     apply all resources from state file only when there are changes
    #      status    retrieve status of releases in state file
    #      delete    DEPRECATED: delete releases from state file (helm delete)
    #      destroy   deletes and then purges releases
    #      test      test releases from state file (helm test)

    # Loop through helmfile commands from COMMANDS array

if __name__ == "__main__":
    main()
