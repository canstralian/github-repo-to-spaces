import gradio as gr
from huggingface_hub import HfApi
from git import Repo
import uuid 
from slugify import slugify

def clone(profile: gr.OAuthProfile, oauth_token: gr.OAuthToken, repo_git, repo_hf):
    folder = str(uuid.uuid4())
    cloned_repo = Repo.clone_from(repo_git, folder)

    #Upload to HF
    api = HfApi(token=oauth_token.token)
    api.create_repo(
        f"{profile.username}/{slugify(repo_hf)}",
        repo_type="space",
    )
    api.upload_folder(
        folder_path=folder,
        repo_id=f"{profile.username}/{slugify(repo_hf)}",
        repo_type="space",
    )
    return f"https://huggingface.co/{profile.username}/{slugify(repo_hf)}"


with gr.Blocks() as demo:
    gr.LoginButton()
    with gr.Row():
        with gr.Column():
            repo_git = gr.Textbox(label="GitHub Repository")
            repo_hf = gr.Textbox(label="Hugging Face Space name")
        with gr.Column():
            output = gr.Textbox(label="Output repo")
    btn = gr.Button("Bring over!")
    btn.click(fn=clone, inputs=[repo_git, repo_hf], outputs=output)

if __name__ == "__main__":
    demo.launch()
