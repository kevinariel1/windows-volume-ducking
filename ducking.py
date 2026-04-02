import time
from pycaw.utils import AudioUtilities
from pycaw.pycaw import IAudioMeterInformation

# Use __slots__ to save memory if you ever expand this into classes
# For a simple script, avoiding global variables is the best 'pro' move.

def run_ducking():
    # Increase sleep to 1.5s to reduce CPU 'wake-ups'
    # 8GB RAM usually means your CPU is also working hard; let it rest.
    interval = 1.5 
    
    while True:
        try:
            # We only query sessions once per loop to save cycles
            sessions = AudioUtilities.GetAllSessions()
            
            # Use local variables (faster/lighter than globals)
            target_music = None
            is_priority_playing = False

            for session in sessions:
                if not session.Process: continue
                
                name = session.Process.name().lower()
                
                if name == "chrome.exe":
                    meter = session._ctl.QueryInterface(IAudioMeterInformation)
                    if meter.GetPeakValue() > 0.005:
                        is_priority_playing = True
                
                if name == "spotify.exe":
                    target_music = session.SimpleAudioVolume

            if target_music:
                current_vol = target_music.GetMasterVolume()
                # Duck to 0.1 if priority is active, else 1.0
                new_vol = 0.1 if is_priority_playing else 1.0
                
                if round(current_vol, 2) != new_vol:
                    target_music.SetMasterVolume(new_vol, None)
                    
            # Explicitly clear the sessions list to help Garbage Collection
            del sessions 

        except Exception:
            pass
            
        time.sleep(interval)

if __name__ == "__main__":
    run_ducking()