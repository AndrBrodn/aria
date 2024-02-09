import sys
from llama_cpp import Llama
from huggingface_hub import hf_hub_download


class Llm:
    def __init__(self, params=None):
        self.params = params or {}
        self.model_name = self.params.get('model_name', None)
        self.model_file = self.params.get('model_file', None)
        self.num_gpu_layers = self.params.get('num_gpu_layers', None)
        self.context_length = self.params.get('context_length', None)
        self.streaming_output = self.params.get('streaming_output', None)
        self.chat_format = self.params.get('chat_format', None)
        self.system_message = self.params.get('system_message', None)
        self.verbose = self.params.get('verbose', None)
       
        model_path = hf_hub_download(self.model_name, filename=self.model_file)

        self.llm = Llama(
                    model_path=model_path,
                    n_gpu_layers=self.num_gpu_layers,
                    n_ctx=self.context_length,
                    chat_format=self.chat_format,
                    verbose=self.verbose
                    )

        self.messages = [
                {
                    "role": "system", 
                    "content": self.system_message
                }
            ]

    def get_answer(self, data, ui):
        self.messages.append(
            {
                "role": "user", 
                "content": data
            }
        )
    
        outputs = self.llm.create_chat_completion(
            self.messages,
            stream=self.streaming_output
            )
        if self.streaming_output:
            llm_output = ""
            ui.add_message("aria", "", new_entry=True)
            for i, out in enumerate(outputs):
                if "content" in out['choices'][0]["delta"]:
                    output_chunk_txt = out['choices'][0]["delta"]['content']
                    if i == 1:
                        print('aria:', output_chunk_txt.strip(), end='')
                        ui.add_message("aria", output_chunk_txt.strip(), new_entry=False)
                    else:
                        print(output_chunk_txt, end='')
                        ui.add_message("aria", output_chunk_txt, new_entry=False)
                    sys.stdout.flush()
                    llm_output += output_chunk_txt
            print()
            llm_output = llm_output.strip()  
        else:
            llm_output = outputs["choices"][0]["message"]["content"].strip()

        self.messages.append(
            {
                "role": "assistant", 
                "content": llm_output
            }
        )
        
        return llm_output