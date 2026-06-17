import re
import os

files = [
    'js/try.html', 'js/set.html', 'js/objetos.html', 'js/map.html',
    'js/json.html', 'js/import.html', 'js/funciones.html', 'js/fetch.html',
    'js/estructurasControl.html', 'js/async.html', 'js/arrays.html'
]

base_dir = r'\\server\c$\xampp\htdocs\alfonso\apuntes'

def process_file(file_path):
    full_path = os.path.join(base_dir, file_path.replace('/', '\\'))
    if not os.path.exists(full_path):
        print(f'File not found: {full_path}')
        return
    
    with open(full_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Regex to find <p class="logica"> ... </p> blocks
    pattern = re.compile(r'<p class="logica">(.*?)</p>', re.DOTALL)

    def replace_block(match):
        inner = match.group(1)
        
        # 1. Replace &nbsp; with space
        inner = inner.replace('&nbsp;', ' ')
        
        # 2. Fix typo code> -> <code>
        inner = inner.replace('code>', '<code>')
        
        # 3. Replace <br> with newline
        inner = re.sub(r'<br\s*/?>', '\n', inner)
        
        # 4. Dedent
        lines = inner.split('\n')
        
        # Find min indent
        indent = -1
        for line in lines:
            stripped = line.strip()
            if stripped and stripped not in ['<code>', '</h4>', '</code>']:
                m = re.match(r'^(\s*)', line)
                if m:
                    l = len(m.group(1))
                    if indent == -1 or l < indent:
                        indent = l
        
        if indent == -1: indent = 0
        
        new_lines = []
        for line in lines:
            if line.strip() in ['<code>', '</code>']:
                new_lines.append(line.strip())
            elif line.strip():
                new_lines.append(line[indent:] if len(line) >= indent else line.lstrip())
            else:
                new_lines.append('')
        
        # Remove empty lines at start/end
        while new_lines and not new_lines[0].strip():
            new_lines.pop(0)
        while new_lines and not new_lines[-1].strip():
            new_lines.pop(-1)
            
        return f'<pre class="logica">' + '\n'.join(new_lines) + '</pre>'

    new_content = pattern.sub(replace_block, content)
    
    if new_content != content:
        with open(full_path, 'w', encoding='utf-8', newline='\n') as f:
            f.write(new_content)
        print(f'Updated {file_path}')
    else:
        print(f'No matches in {file_path}')

for f in files:
    process_file(f)
