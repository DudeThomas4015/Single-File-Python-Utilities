import time
import random
import threading
import os

# Text drawings of the gunslingers
gunslinger1 = """
        ___
     __|___|__
      ('o_o')
      _\\~-~/_  
     //\\__/\\ \\ 
    / )O  O(  \\
    \\ \\    /  /
    )/_|  |_\\°|
   // /(\\/)\\ \\
   /_/      \\_\\
  (_||      ||_)
    \\| |__| |/
     | |  | |
     | |  | |
     |_|  |_|
     /_\\  /_\\
         
       Ready?
"""
gunslinger2 = """
        ___
     __|___|__
      ('o_o')
      _\\~-~/_    ______.
     //\\__/\\ \\ ~(_]---'
    / )O  O( .\\/_)
    \\ \\    / \\_/
    )/_|  |_\\
   // /(\\/)\\ \\
   /_/      \\_\\
  (_||      ||_)
    \\| |__| |/
     | |  | |
     | |  | |
     |_|  |_|
     /_\\  /_\\
         
       DRAW!
"""

gunslinger3 = """
        ___
     __|___|__
            
            
      /\\__/\\ 
      )O  O(  
      \\    /    
      _|  |_   
      /(\\/)\\   
    _/      \\_
    ||      ||
    \\| |__| |/
     | |  | |
     | |  | |
     |_|  |_|
     /_\\  /_\\
         
     Nice Shot!
"""
gunslinger3_1 = """
   
        ___
     __|___|__
            
      /\\__/\\ 
      )O  O(  
      \\    /    
      _|  |_   
      /(\\/)\\   
    _/      \\_
    ||      ||
    \\| |__| |/
     | |  | |
     | |  | |
     |_|  |_|
     /_\\  /_\\
         
     Nice Shot!
"""

gunslinger3_2 = """
   
   
        ___
     __|___|__    
      /\\__/\\ 
      )O  O(  
      \\    /    
      _|  |_   
      /(\\/)\\   
    _/      \\_
    ||      ||
    \\| |__| |/
     | |  | |
     | |  | |
     |_|  |_|
     /_\\  /_\\
         
     Nice Shot!
"""

gunslinger4 = """
        ___
     __|___|__
      ('o_o')
      _\\~-~/_   _  
     //\\__/\\ \\ |0|
    / )O  O( .\\/_)
    \\ \\    / \\_/
    )/_|  |_\\
   // /(\\/)\\ \\
   /_/      \\_\\
  (_||      ||_)
    \\| |__| |/
     | |  | |
     | |  | |
     |_|  |_|
     /_\\  /_\\
         
       BANG!
"""
gunslinger5 = """
        ___
     __|___|__
      ('o_o') .---.
      _\\~-~/_ (\\|/)  
     //\\__/\\ \\--0--
    / )O  O( .(/|\\)
    \\ \\    / \\_/
    )/_|  |_\\
   // /(\\/)\\ \\
   /_/      \\_\\
  (_||      ||_)
    \\| |__| |/
     | |  | |
     | |  | |
     |_|  |_|
     /_\\  /_\\
         
       BANG!
"""
gunslinger6 = """
        ___
     __|___|__
      ('o_o')'.\\|/.'
      _\\~-~/_(\\ _ /) 
     //\\__/\\ - |°| -
    / )O  O( (//_)\\)
    \\ \\    / ,'/|\\'.
    )/_|  |_\\
   // /(\\/)\\ \\
   /_/      \\_\\
  (_||      ||_)
    \\| |__| |/
     | |  | |
     | |  | |
     |_|  |_|
     /_\\  /_\\
         
       BANG!
"""

gunslinger7 = """
        ___
     __|___|__
      ('o_o')'.   .'
      _\\~-~/_   _   '
     //\\__/\\ \\ |°|   '
    / )O  O( .\\/_)   .
    \\ \\    / \\_/    .
    )/_|  |_\\'   '.
   // /(\\/)\\ \\
   /_/      \\_\\
  (_||      ||_)
    \\| |__| |/
     | |  | |
     | |  | |
     |_|  |_|
     /_\\  /_\\
         
       BANG!
"""

class TimeoutInput:
    def __init__(self):
        self.input_received = False
        self.accept_input = False

    def input_with_timeout(self, prompt, timeout):
        def get_input():
            input(prompt)
            if self.accept_input:
                self.input_received = True
            

        thread = threading.Thread(target=get_input)
        thread.start()
        thread.join(timeout)

        if thread.is_alive():
            self.input_received = False

def play_game():
    input("Press Enter to begin the game...")
    
    # Display the initial gunslinger
    print(gunslinger1)
    
    # Wait for a random period between 2 and 25 seconds
    wait_time = random.uniform(1, 12)
    time.sleep(wait_time)
    
    # Display the second picture
    os.system('cls' if os.name == 'nt' else 'clear')
    print(gunslinger2)
    
    # Measure reaction time
    timeout_input = TimeoutInput()
    timeout_input.accept_input = True
    start_time = time.time()
    timeout_input.input_with_timeout("Press Enter as fast as you can!", random.uniform(0.2, 2))
    reaction_time = time.time() - start_time
    
    if timeout_input.input_received:
        # Display the third picture
        os.system('cls' if os.name == 'nt' else 'clear')
        print(gunslinger3)
        time.sleep(.15)
        os.system('cls' if os.name == 'nt' else 'clear')
        print(gunslinger3_1)
        time.sleep(.15)
        os.system('cls' if os.name == 'nt' else 'clear')
        print(gunslinger3_2)
        # Print the reaction time
        print(f"Your reaction time: {reaction_time:.3f} seconds")
        time.sleep(3)
    else:
        # Display the failure picture
        os.system('cls' if os.name == 'nt' else 'clear')
        print(gunslinger4)
        time.sleep(.15)
        os.system('cls' if os.name == 'nt' else 'clear')
        print(gunslinger5)
        time.sleep(.15)
        os.system('cls' if os.name == 'nt' else 'clear')
        print(gunslinger6)
        time.sleep(.15)
        os.system('cls' if os.name == 'nt' else 'clear')
        print(gunslinger7)
        
        print("Too slow!")
        time.sleep(3)
        os._exit(0)

if __name__ == "__main__":
    play_game()