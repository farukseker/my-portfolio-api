import os
from dataclasses import dataclass
from charset_normalizer import from_path


@dataclass
class Requirement:
    name: str
    version: str
    match: bool = False


def get_default_requirements():
    requirements: list[Requirement] = []
    requirements_text = from_path('./requirements.txt')
    for requirement in str(requirements_text.best()).split('\n'):
        requirement = requirement.split('==')
        if len(requirement) == 2:
            requirements.append(
                Requirement(name=requirement[0], version=requirement[1].replace('\r', ''))
            )
    return requirements


def get_new_requirements(venv_path='.venv'):
    requirements: list[Requirement] = []
    pip_freeze_command = f"{venv_path}\\Scripts\\pip freeze"
    pip_freeze_output = os.popen(pip_freeze_command).read()
    for requirement in pip_freeze_output.split('\n'):
        requirement = requirement.split('==')
        if len(requirement) == 2:
            requirements.append(
                Requirement(name=requirement[0], version=requirement[1])
            )
    return requirements


def main():
    default_requirements = get_default_requirements()
    new_requirements = get_new_requirements()
    diff_requirements: list[Requirement] = []
    removed_requirements: list[Requirement] = []
    for new_requirement in new_requirements:
        for default_requirement in default_requirements:
            if new_requirement.name == default_requirement.name:
                new_requirement.match = True
                default_requirement.match = True
                if not new_requirement.version == default_requirement.version:
                    diff_requirements.append(new_requirement)
                break
    for new_requirement in new_requirements:
        if not new_requirement.match:
            diff_requirements.append(new_requirement)
    for default_requirement in default_requirements:
        if not default_requirement.match:
            removed_requirements.append(default_requirement)
    if any([diff_requirements, removed_requirements]):
        print('any')
    print(diff_requirements)
    print(removed_requirements)


if __name__ == "__main__":
    main()

'pass'