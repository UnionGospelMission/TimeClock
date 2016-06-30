class LiveFragmentMeta(type):
    def __init__(cls, *args):
        super().__init__(*args)
        cls.instances = []
