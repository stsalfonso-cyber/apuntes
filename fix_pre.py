import re
import os

files = [
    'js/try.html', 'js/set.html', 'js/objetos.html', 'js/map.html',
    'js/json.html', 'js/import.html', 'js/funciones.html', 'js/fetch.html',
    'js/estructurasControl.html', 'js/async.html', 'js/arrays.html'
]

base_dir = r'\\server\c$\xampp\htdocs\alfonso\apuntes'

def fix_block(match):
    inner = match.group(1)
    # Fix the tags messed up by previous script
    inner = inner.replace('<<code>', '<code>').replace('</<code>', '</code>')
    # Fix double newlines
    inner = re.sub(r'\n\s*\n', '\n', inner)
    
    lines = inner.split('\n')
    # Clean start/end
    while lines and not lines[0].strip(): lines.pop(0)
    while lines and not lines[-1].strip(): lines.pop(-1)
    
    if not lines: return '<pre class="logica"></pre>'
    
    # Find min indent
    indent = -1
    for line in lines:
        stripped = line.strip()
        if stripped and stripped not in ['<code>', '</code>']:
            m = re.match(r'^(\s*)', line)
            if m:
                l = len(m.group(1))
                if indent == -1 or l < indent:
                    indent = l
    if indent == -1: indent = 0
    
    new_lines = []
    for line in lines:
        stripped = line.strip()
        if stripped in ['<code>', '</code>']:
            new_lines.append(stripped)
        elif stripped:
            new_lines.append(line[indent:] if len(line) >= indent else line.lstrip())
        else:
            new_lines.append('')
            
    # Move <code> to same line as first line of code if possible, or just keep it clean
    # The user wanted valid HTML and no extra whitespace.
    result = '\n'.join(new_lines)
    return f'<pre class="logica">{result}</pre>'

for f in files:
    full_path = os.path.join(base_dir, f.replace('/', '\\'))
    if not os.path.exists(full_path): continue
    
    with open(full_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Target <pre class="logica"> blocks
    new_content = re.sub(r'<pre class="logica">(.*?)</pre>', fix_block, content, flags=re.DOTALL)
    
    # Also target any remaining <p class="logica"> blocks just in case
    # (though they should all be converted by now, but maybe with errors)
    def fix_p_block(match):
        inner = match.group(1)
        inner = inner.replace('&nbsp;', ' ').replace('code>', '<code>')
        inner = re.sub(r'<br\s*/?>\s*\n', '\n', inner)
        inner = re.sub(r'<br\s*/?>', '\n', inner)
        
        lines = inner.split('\n')
        while lines and not lines[0].strip(): lines.pop(0)
        while lines and not lines[-1].strip(): lines.pop(-1)
        
        indent = -1
        for line in lines:
            stripped = line.strip()
            if stripped and stripped not in ['<code>', '</code>']:
                m = re.match(r'^(\s*)', line)
                if m:
                    l = len(m.group(1))
                    if indent == -1 or l < indent: indent = l
        if indent == -1: indent = 0
        
        new_lines = []
        for line in lines:
            stripped = line.strip()
            if stripped in ['<code>', '</code>']: new_lines.append(stripped)
            elif stripped: new_lines.append(line[indent:] if len(line) >= indent else line.lstrip())
            else: new_lines.append('')
        
        return f'<pre class="logica">' + '\n'.join(new_lines) + '</pre>'

    new_content = re.sub(r'<p class="logica">(.*?)</p>', fix_p_block, new_content, flags=re.DOTALL)

    if new_content != content:
        with open(full_path, 'w', encoding='utf-8', newline='\n') as file:
            file.write(new_content)
        print(f'Fixed {f}')
