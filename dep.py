import os
import re
from collections import defaultdict

start_directory = '.'

shorthand_pattern = re.compile(r"implementation ['\"]([\w\.-]+:[\w\.-]+):[^'\"]+['\"]")
detailed_pattern = re.compile(
    r"implementation\s*\(\s*group:\s*['\"]([\w\.-]+)['\"],\s*name:\s*['\"]([\w\.-]+)['\"]"
)

dependency_projects = defaultdict(set)

def normalize_dependency(group, artifact):
    return f"{group}:{artifact}"

for root, dirs, files in os.walk(start_directory):
    for file in files:
        if file == 'build.gradle':
            file_path = os.path.join(root, file)
            with open(file_path, 'r', encoding='utf-8') as gradle_file:
                for line in gradle_file:
                    shorthand_match = shorthand_pattern.search(line)
                    detailed_match = detailed_pattern.search(line)
                    if shorthand_match:
                        group_artifact = shorthand_match.group(1)
                        dependency_projects[group_artifact].add(root)
                    elif detailed_match:
                        group, artifact = detailed_match.groups()
                        dependency = normalize_dependency(group, artifact)
                        dependency_projects[dependency].add(root)

table_data = []
column_width = 50  
for dependency, projects in sorted(dependency_projects.items()):
    formatted_projects = '\n'.join([' ' * (column_width + 3) + project for project in projects])
    table_data.append([dependency, formatted_projects])

print(f"{'Dependency':<{column_width}} | Projects")
print("-" * 88)
for row in table_data:
    projects_lines = row[1].split('\n')
    print(f"{row[0]:<{column_width}} | {projects_lines[0].strip()}")
    for project_line in projects_lines[1:]:
        print(f"{' ':<{column_width}} | {project_line.strip()}")

    print("-" * 88)