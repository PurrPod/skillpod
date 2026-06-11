#!/usr/bin/env python3
import os
import json
import re
import sys

REPO_BASE_URL = "https://github.com/PurrPod/skillpod/tree/main"
REGISTRY_FILE = "registry.json"
EXTERNAL_FILE = "external.json"
README_FILE = "README.md"

def parse_skill_md(filepath):
    """从 SKILL.md 中提取 YAML frontmatter"""
    meta = {}
    if not os.path.exists(filepath):
        return meta
        
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    match = re.search(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
    if match:
        yaml_text = match.group(1)
        for line in yaml_text.split('\n'):
            if ':' in line:
                k, v = line.split(':', 1)
                meta[k.strip()] = v.strip().strip('"\'')
    return meta

def scan_directory(base_dir, skill_type):
    """扫描目录下的所有子文件夹"""
    skills = {}
    if not os.path.exists(base_dir):
        return skills
        
    for item in sorted(os.listdir(base_dir)):
        skill_dir = os.path.join(base_dir, item)
        if os.path.isdir(skill_dir) and not item.startswith('.'):
            skill_md = os.path.join(skill_dir, 'SKILL.md')
            meta = parse_skill_md(skill_md)
            
            skill_name = meta.get("name", "").strip()
            if not skill_name:
                print(f"❌ 校验失败: [{skill_dir}/SKILL.md] 缺失 'name' 字段！")
                sys.exit(1)
                
            if skill_name != item:
                print(f"❌ 校验失败: 目录 [{skill_dir}] 与其内部 SKILL.md 的 name 字段 ('{skill_name}') 不一致！")
                print(f"💡 修复建议: 请将 SKILL.md 中的 `name: {skill_name}` 修改为 `name: {item}`，或重命名文件夹。")
                sys.exit(1)
            
            skills[item] = {
                "name": skill_name,
                "description": meta.get("description", "暂无描述"),
                "author": meta.get("author", "PurrCat Contributor"),
                "type": skill_type,
                "source_url": f"{REPO_BASE_URL}/{base_dir}/{item}"
            }
            if "tags" in meta:
                skills[item]["tags"] = [t.strip() for t in meta["tags"].strip('[]').split(',')]
    return skills

def generate_markdown_table(skills_dict, target_type):
    """生成 Markdown 表格"""
    lines = [
        "| 技能短名 (Install ID) | 技能名称 | 描述 | 作者 |",
        "| :--- | :--- | :--- | :--- |"
    ]
    
    count = 0
    for short_id, info in sorted(skills_dict.items()):
        if info.get("type") == target_type:
            name = info.get("name", short_id)
            desc = info.get("description", "-")
            author = info.get("author", "-")
            url = info.get("source_url", "#")
            
            lines.append(f"| **`{short_id}`** | [{name}]({url}) | {desc} | {author} |")
            count += 1
            
    if count == 0:
        lines.append("| *(虚位以待)* | 期待你的 PR！ | 提交你的优质技能，让更多人使用。 | - |")
        
    return "\n".join(lines) + "\n"

def update_readme(registry_data):
    """更新 README.md 中的占位符内容"""
    if not os.path.exists(README_FILE):
        return
        
    with open(README_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    off_table = generate_markdown_table(registry_data["skills"], "official")
    content = re.sub(
        r'(\n<!-- BEGIN_OFFICIAL_TABLE -->).*?(\n<!-- END_OFFICIAL_TABLE -->)',
        f'\\g<1>\n{off_table}\\g<2>',
        content,
        flags=re.DOTALL
    )

    com_table = generate_markdown_table(registry_data["skills"], "community")
    content = re.sub(
        r'(\n<!-- BEGIN_COMMUNITY_TABLE -->).*?(\n<!-- END_COMMUNITY_TABLE -->)',
        f'\\g<1>\n{com_table}\\g<2>',
        content,
        flags=re.DOTALL
    )

    with open(README_FILE, 'w', encoding='utf-8') as f:
        f.write(content)

def main():
    print("[*] 正在扫描本地目录...")
    official_skills = scan_directory("official", "official")
    community_skills = scan_directory("community", "community")
    
    all_skills = {**official_skills, **community_skills}
    
    print("[*] 正在合并 external.json...")
    if os.path.exists(EXTERNAL_FILE):
        with open(EXTERNAL_FILE, 'r', encoding='utf-8') as f:
            try:
                external_skills = json.load(f)
                all_skills.update(external_skills)
            except Exception as e:
                print(f"[!] external.json 解析失败: {e}")

    registry = {
        "version": "1.0",
        "repository": "https://github.com/PurrPod/skillpod",
        "skills": all_skills
    }
    
    print("[*] 正在生成 registry.json...")
    with open(REGISTRY_FILE, 'w', encoding='utf-8') as f:
        json.dump(registry, f, indent=2, ensure_ascii=False)
        
    print("[*] 正在更新 README.md...")
    update_readme(registry)
    
    print("[+] 构建完成！")

if __name__ == "__main__":
    main()
