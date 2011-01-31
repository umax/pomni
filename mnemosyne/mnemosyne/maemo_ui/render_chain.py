from mnemosyne.libmnemosyne.render_chain import RenderChain
from mnemosyne.maemo_ui.renderers import Html

class MaemoRenderChain(RenderChain):
    id = 'default'
    filters = []
    renderers = [Html]
