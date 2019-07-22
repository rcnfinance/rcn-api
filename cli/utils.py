import os
import string


def touch(path):
    with open(path, 'a'):
        os.utime(path, None)


def list_contracts():
    path = 'listener/src/contracts/'
    directories = [d.name for d in os.scandir(path) if d.is_dir() and not d.name.startswith("__") and not d.name == "debtModel"]

    return directories


def new_event(event_name, contract_name):
    # event_name snake_case
    # contract_name snake_case
    contracts_root = "listener/src/contracts"
    contract_path = os.path.join(
        contracts_root,
        snake2camel(contract_name)
    )
    opcode = "{event_name}_{contract_name}".format(
        event_name=event_name,
        contract_name=contract_name
    )
    data = {
        "event_name": snake2uppercamel(event_name),
        "opcode": opcode
    }
    # template handler
    event_template = open("cli/event_handler.template")
    t = string.Template(event_template.read())
    event_template.close()

    event_file = open(os.path.join(contract_path, "handlers", "{}.py".format(event_name)), "w")
    event_file.write(t.substitute(data))
    event_file.close()

    # template commit processor
    commit_template = open("cli/event_commit_processor.template")
    t = string.Template(commit_template.read())
    commit_template.close()

    commit_file = open(os.path.join(contract_path, "commit_processors", "{}.py".format(event_name)), "w")
    commit_file.write(t.substitute(data))
    commit_file.close()


def snake2camel(snake_case_text):
    components = snake_case_text.split('_')
    return components[0] + ''.join(x.title() for x in components[1:])


def snake2uppercamel(snake_case_text):
    components = snake_case_text.split('_')
    return ''.join(x.title() for x in components)


def new_contract(contract_name):
    contracts_root = "listener/src/contracts"
    # contract_name "loan_manager"
    # nueva carpeta camelcase
    contract_path = os.path.join(
        contracts_root,
        snake2camel(contract_name)
    )
    os.mkdir(contract_path)
    os.mkdir(os.path.join(contract_path, "commit_processors"))
    os.mkdir(os.path.join(contract_path, "handlers"))
    touch(os.path.join(contract_path, "__init__.py"))
    touch(os.path.join(contract_path, "abi.json"))

    # template contract.py
    data = {
        "contract_address": contract_name.upper() + "_ADDRESS",
        "contract_name": snake2uppercamel(contract_name)
    }
    contract_template = open("cli/contract.template")
    t = string.Template(contract_template.read())
    contract_template.close()

    contract_file = open(os.path.join(contract_path, "{}.py".format(contract_name)), "w")
    contract_file.write(t.substitute(data))
    contract_file.close()
