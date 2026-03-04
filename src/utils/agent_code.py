from src.models.project import Project


def generate_agent_code(project: Project) -> str:
    first_letter_list = [word[0] for word in project.name.split()]
    code = "".join(first_letter_list).upper()
    project.agent_seq += 1
    return f"AG-{code}-{project.agent_seq:03d}"
