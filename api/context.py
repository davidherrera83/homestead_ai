from fastapi import FastAPI
import markdown
import os

app = FastAPI()
_root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

@app.get('/getHHContext')
def get_homestead_context():
    md_file_path = os.path.join(_root_dir, 'hh_context.md')
    with open(md_file_path, 'r') as file:
        md_content = file.read()
        html_content = markdown.markdown(md_content)
    return {"content": html_content}
