import time
from VALE_core import VALE_core
from VALE_inputhandler import VALE_inputhandler

class VALEMainLoop:
    def __init__(self, config_path: str):
        self.vale = VALE(config_path)
        self.input_handler = VALEInputHandler()
        self.running = True

    def start(self):
        """Start the main loop for VALE."""
        print("VALE system online. Type 'exit' to shut down.")
        while self.running:
            try:
                user_input = input("> ")
                if user_input.lower() == "exit":
                    self.shutdown()
                    break
                
                context = self.vale.get_memory(user_input)
                response = self.vale.process_input(user_input, context)
                print(response)
                
                if self.vale.persona.current_personality != "default":
                    print("[Persona: " + str(self.vale.persona.current_personality) + "]")
                
            except KeyboardInterrupt:
                self.shutdown()
                break
            except Exception as e:
                print("Error: " + str(e))

    def shutdown(self):
        """Shutdown the VALE system."""
        self.running = False
        self.vale.process_input("shutdown")
        print("VALE system offline.")

if __name__ == "__main__":
    main_loop = VALEMainLoop("/home/celtron/vgu/VALE_config.json")
    main_loop.start()
