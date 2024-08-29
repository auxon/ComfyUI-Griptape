from griptape.drivers import OllamaPromptDriver

from .gtUIBasePromptDriver import gtUIBasePromptDriver

default_port = "11434"
default_base_url = "http://127.0.0.1"


class gtUIOllamaPromptDriver(gtUIBasePromptDriver):
    @classmethod
    def INPUT_TYPES(s):
        inputs = super().INPUT_TYPES()

        inputs["required"].update(
            {
                "model": ((), {}),
                "base_url": ("STRING", {"default": default_base_url}),
                "port": ("STRING", {"default": default_port}),
            }
        )
        inputs["optional"].update({})

        return inputs

    FUNCTION = "create"

    def create(self, **kwargs):
        model = kwargs.get("model", None)
        base_url = kwargs.get("base_url", default_base_url)
        port = kwargs.get("port", default_port)
        stream = kwargs.get("stream", False)
        temperature = kwargs.get("temperature", None)
        max_attempts = kwargs.get("max_attempts_on_fail", None)
        use_native_tools = kwargs.get("use_native_tools", False)
        max_tokens = kwargs.get("max_tokens", None)

        params = {}

        if model:
            params["model"] = model
        if stream:
            params["stream"] = stream
        if temperature:
            params["temperature"] = temperature
        if max_attempts:
            params["max_attempts"] = max_attempts
        if base_url and port:
            params["host"] = f"{base_url}:{port}"
        if use_native_tools:
            params["use_native_tools"] = use_native_tools
        if max_tokens > 0:
            params["max_tokens"] = max_tokens
        try:
            driver = OllamaPromptDriver(**params)
            return (driver,)
        except Exception as e:
            print(f"Error creating driver: {e}")
            return (None, str(e))
