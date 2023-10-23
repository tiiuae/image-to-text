#!/usr/bin/env python3
from local_llm import Agent, Pipeline, ChatTemplates

from local_llm.plugins import (
    UserPrompt, ChatQuery, PrintStream, 
    RivaASR, RivaTTS, 
    AudioOutputDevice, AudioOutputFile
)

from local_llm.utils import ArgParser, print_table

from termcolor import cprint


class VoiceChat(Agent):
    """
    Uses ASR + TTS to chat with LLM
    """
    def __init__(self, **kwargs):
        super().__init__()

        # ASR
        self.asr = RivaASR(**kwargs)
    
        self.asr.add(PrintStream(partial=False, prefix='## ', color='blue'), RivaASR.OutputFinal)
        self.asr.add(PrintStream(partial=False, prefix='>> ', color='magenta'), RivaASR.OutputPartial)
    
        # LLM
        self.llm = ChatQuery(**kwargs)
    
        self.llm.add(PrintStream(color='green'))
        self.llm.add(self.on_eos)
        
        self.asr.add(self.llm, RivaASR.OutputFinal)  # submit ASR sentences to the LLM
        
        # TTS
        self.tts = RivaTTS(**kwargs)
        self.llm.add(self.tts, ChatQuery.OutputWords)
        
        # Audio Output
        self.audio_output_device = kwargs.get('audio_output_device')
        self.audio_output_file = kwargs.get('audio_output_file')
        
        if self.audio_output_device is not None:
            self.audio_output_device = AudioOutputDevice(**kwargs)
            self.tts.add(self.audio_output_device)
        
        if self.audio_output_file is not None:
            self.audio_output_file = AudioOutputFile(**kwargs)
            self.tts.add(self.audio_output_file)
        
        # CLI prompts
        self.cli = UserPrompt(interactive=True, **kwargs)
        self.cli.add(self.llm)
        
        self.pipeline = [self.cli, self.asr]

    def on_eos(self, input):
        if input.endswith('</s>'):
            print_table(self.llm.model.stats)
            #self.print_input_prompt()

    """
    def print_input_prompt(self):
        if self.interactive:
            cprint('>> PROMPT: ', 'blue', end='', flush=True)
    """ 
        
if __name__ == "__main__":
    from local_llm.utils import ArgParser

    parser = ArgParser(extras=ArgParser.Defaults+['asr', 'tts', 'audio_output'])
    args = parser.parse_args()
    
    agent = VoiceChat(**vars(args)).run() 
    