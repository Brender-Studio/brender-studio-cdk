from utils.blender_render_setup import setup_env_python_path, setup_display, get_environment_variables, validate_environment_variables
from utils.run_blender_command import run_blender_command

def convert_to_boolean(value):
    return True if value.lower() == 'true' else False

def main():
    env_vars = get_environment_variables()
    validate_environment_variables(env_vars)
    env_vars['use_eevee'] = convert_to_boolean(env_vars['use_eevee'])
    print('Valor de use_eevee como booleano:', env_vars['use_eevee'])
    setup_env_python_path(env_vars['bucket_key'])
    setup_display(env_vars['use_eevee'])
    run_blender_command(env_vars)

if __name__ == "__main__":
    main()
