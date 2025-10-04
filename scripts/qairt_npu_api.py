import modules.scripts as scripts

class Script(scripts.Script):
    def title(self):
        return "QAiRT NPU API"

    def show(self, is_img2img):
        return False  # No UI

    def ui(self, is_img2img):
        return []

    def run(self, p, *args):
        pass  # No processing