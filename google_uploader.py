import urequests
import gc
from secrets import secrets

class GoogleUploader:
    def __init__(self):
        self.url = secrets['google_url']
        
    def sync_from_file(self, logger, display_man):
        lines = logger.read_all()
        if not lines: return
        
        display_man.show_uploading()
        print(f"start sync: {len(lines)}records")
        all_ok = True
        
        for line in lines:
            line = line.strip()
            if not line: continue
            
            # encoding characters
            d, t, m = line.split(',')
            m_safe = m.replace(" ", "%20").replace(":", "%3A").replace("^", "%5E")
            full_url = f"{self.url}?date={d}&time={t}&mood={m_safe}"
            
            resp = None # initialzing
            try:
                resp = urequests.get(full_url)
                
                # handling HTTP 302 redirect(if needed)
                if resp.status_code == 302:
                    new_url = resp.headers.get("Location")
                    resp.close() # close earlier response
                    resp = urequests.get(new_url)
                
                # check final uploading
                if resp.status_code == 200 and "Success" in resp.text:
                    print(f"uploading success: {m}")
                else:
                    all_ok = False
                    print(f"failed uploadig(status code): {resp.status_code}")
            
            except Exception as e:
                print(f"network error: {e}")
                all_ok = False
                break # escape
                
            finally:
                if resp:
                    resp.close() # memory off
            pass
        
        if all_ok:
            logger.clear()
            print("success uploading & removing all logs!")
            
        gc.collect()  # garbage collecting
        print(f"memory optimalized: {gc.mem_free()}bytes free")
        