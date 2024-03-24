from modal import Stub
import modal
image=(modal.Image.debian_slim(python_version="3.10.8")
                            .pip_install("PyMuPDF",
                                         "anthropic",
                                         "python-dotenv",))
stub = Stub(name="web12", image=image)
