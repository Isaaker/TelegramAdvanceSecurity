import curses
import time
import json
import os
import gnupg

LOGO_TELEGRAM = [
    "                                        ++++++++++++++++++++                                        ",
    "                                  ++++++++++++++++++++++++++++++++                                  ",
    "                             ++++++++++++++++++++++++++++++++++++++++++                             ",
    "                         ++++++++++++++++++++++++++++++++++++++++++++++++++                         ",
    "                       ++++++++++++++++++++++++++++++++++++++++++++++++++++++                       ",
    "                    ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++                    ",
    "                  ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++                  ",
    "                ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++                ",
    "              ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++              ",
    "            ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++            ",
    "           ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++           ",
    "         ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++         ",
    "        ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++        ",
    "       +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++    +++++++++++++++++       ",
    "      +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++           ++++++++++++++++      ",
    "     ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++               +++++++++++++++++     ",
    "    ++++++++++++++++++++++++++++++++++++++++++++++++++++++-                   ++++++++++++++++++    ",
    "   +++++++++++++++++++++++++++++++++++++++++++++++++++                        +++++++++++++++++++   ",
    "   +++++++++++++++++++++++++++++++++++++++++++++++                           ++++++++++++++++++++   ",
    "  ++++++++++++++++++++++++++++++++++++++++++++                               +++++++++++++++++++++  ",
    "  +++++++++++++++++++++++++++++++++++++++:                                   +++++++++++++++++++++  ",
    " ++++++++++++++++++++++++++++++++++++                     +++                ++++++++++++++++++++++ ",
    " ++++++++++++++++++++++++++++++++                      +++++                +++++++++++++++++++++++ ",
    "+++++++++++++++++++++++++++++                        +++++.                 ++++++++++++++++++++++++",
    "++++++++++++++++++++++++.                         +++++++                   ++++++++++++++++++++++++",
    "++++++++++++++++++++                           .+++++++                    =++++++++++++++++++++++++",
    "++++++++++++++++-                            +++++++=                      +++++++++++++++++++++++++",
    "++++++++++++++++                          ++++++++:                        +++++++++++++++++++++++++",
    "+++++++++++++++++                       ++++++++=                          +++++++++++++++++++++++++",
    "+++++++++++++++++++++                ++++++++++                           ++++++++++++++++++++++++++",
    "+++++++++++++++++++++++++++      =+++++++++++                             ++++++++++++++++++++++++++",
    "+++++++++++++++++++++++++++++++++++++++++++=                              ++++++++++++++++++++++++++",
    " ++++++++++++++++++++++++++++++++++++++++++                              .+++++++++++++++++++++++++ ",
    " ++++++++++++++++++++++++++++++++++++++++++                              ++++++++++++++++++++++++++ ",
    "  +++++++++++++++++++++++++++++++++++++++++++                            +++++++++++++++++++++++++  ",
    "  ++++++++++++++++++++++++++++++++++++++++++++++                         +++++++++++++++++++++++++  ",
    "   ++++++++++++++++++++++++++++++++++++++++++++++++                     +++++++++++++++++++++++++   ",
    "   ++++++++++++++++++++++++++++++++++++++++++++++++++                   +++++++++++++++++++++++++   ",
    "    ++++++++++++++++++++++++++++++++++++++++++++++++++++                ++++++++++++++++++++++++    ",
    "     ++++++++++++++++++++++++++++++++++++++++++++++++++++++            :+++++++++++++++++++++++     ",
    "      +++++++++++++++++++++++++++++++++++++++++++++++++++++++-         +++++++++++++++++++++++      ",
    "       ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++    ++++++++++++++++++++++++       ",
    "        ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++        ",
    "         ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++         ",
    "           ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++           ",
    "            ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++            ",
    "              ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++              ",
    "                ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++                ",
    "                  ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++                  ",
    "                    ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++                    ",
    "                       ++++++++++++++++++++++++++++++++++++++++++++++++++++++                       ",
    "                         ++++++++++++++++++++++++++++++++++++++++++++++++++                         ",
    "                             ++++++++++++++++++++++++++++++++++++++++++                             ",
    "                                  ++++++++++++++++++++++++++++++++                                  ",
    "                                        ++++++++++++++++++++                                        "
]

CONFIG_FILE = "config.json"

DEFAULT_CONFIG = {
    "rate_limit (max requests per second)": 10,
    "message_filter_type": "strict",
    "characters_filter": True,
    "whitelist": "",
    "blacklist": "",
    "safe_requests": True,
    "safe_os": True,
    "owasp_implementation": True,
    "remote_config": False,
    "telegram_connection_check": True,
    "bot_user": "",
    "bot_password": "",
    "bot_recaptcha": False,
    "telemetry": True,
    "rbac": False,
    "warp_vpn_check": False,
    "volume_check": True,
    "process_check": True,
    "groups_lock": False,
    "dangerzone_clean": False,
    "llm_protection": False,
    "package_integrity": True,
    "self_protection": True,
    "compile_bytecode": False,
    "remote_config_url": "",
    "safe_ip": "",
    "safe_asn": "",
    "use_warp": False,
    "public_key": ""
}

def show_splash(stdscr):
    sh, sw = stdscr.getmaxyx()
    # Draw white/grey background
    for y in range(sh):
        try: 
            stdscr.addstr(y, 0, " " * (sw - 1), curses.color_pair(3))
        except: 
            pass

    # Scale logo to fit the screen
    logo_space = sh - 10
    final_logo = LOGO_TELEGRAM
    if len(LOGO_TELEGRAM) > logo_space and logo_space > 0:
        step = len(LOGO_TELEGRAM) / logo_space
        final_logo = [LOGO_TELEGRAM[int(i * step)] for i in range(logo_space)]

    for i, line in enumerate(final_logo):
        try:
            x_pos = max(0, (sw // 2) - (len(line) // 2))
            stdscr.addstr(i + 1, x_pos, line[:sw-1], curses.color_pair(1))
        except: 
            pass

    # Bottom labels
    title = "TELEGRAM ADVANCE SECURITY"
    footer = "Telegram Advance Security © 2025 by Isaac Hernán (Isaaker)"
    
    try:
        stdscr.addstr(sh-6, (sw//2)-(len(title)//2), title, curses.color_pair(1) | curses.A_BOLD)
        stdscr.addstr(sh-4, (sw//2)-(len(footer)//2), footer, curses.color_pair(2))
    except: 
        pass

    stdscr.refresh()
    curses.napms(3000) # 3-SECOND DELAY

def show_menu(stdscr):
    options = ["1. Initial Setup", "2. Edit Settings", "3. Check Signature", "4. License", "5. Exit"]
    selected = 0

    while True:
        stdscr.clear()
        sh, sw = stdscr.getmaxyx()
        
        # Draw a simple border for the menu
        stdscr.attron(curses.color_pair(1))
        stdscr.border()
        stdscr.attroff(curses.color_pair(1))

        stdscr.addstr(2, (sw // 2) - 5, "MAIN MENU", curses.A_BOLD | curses.color_pair(1))

        for i, opt in enumerate(options):
            x = (sw // 2) - (len(opt) // 2)
            y = (sh // 2) - (len(options) // 2) + i
            if i == selected:
                stdscr.addstr(y, x, opt, curses.A_REVERSE | curses.color_pair(1))
            else:
                stdscr.addstr(y, x, opt)

        stdscr.refresh()

        key = stdscr.getch()
        if key == curses.KEY_UP:
            selected = (selected - 1) % len(options)
        elif key == curses.KEY_DOWN:
            selected = (selected + 1) % len(options)
        elif key in [10, 13]: # ENTER key
            if selected == 0: # Initial Setup
                initial_setup(stdscr)
            elif selected == 1: # Edit Settings
                edit_settings(stdscr)
            elif selected == 2: # Check Signature
                check_signature_screen(stdscr)
            elif selected == 3: # License
                show_license(stdscr)
            elif selected == 4: # Exit
                break

def show_license(stdscr):
    # Load the license content once
    try:
        with open("LICENSE.txt", "r") as f:
            lines = [line.strip() for line in f.readlines()]
    except FileNotFoundError:
        lines = ["Error: LICENSE.txt not found."]

    scroll_top = 0  # Index of the first line to show
    
    while True:
        stdscr.clear()
        sh, sw = stdscr.getmaxyx()
        
        # UI Header
        stdscr.addstr(1, 2, "LICENSE INFORMATION (Use Up/Down to scroll, Press 'Q' or 'Enter' to exit)", curses.A_BOLD)
        stdscr.hline(2, 2, curses.ACS_HLINE, sw - 4)

        # Calculate how many lines we can display
        # We reserve lines for header (3) and footer (2)
        display_height = sh - 5
        
        # Render the lines based on the scroll_top offset
        for i in range(display_height):
            line_idx = i + scroll_top
            if line_idx < len(lines):
                # Ensure we don't write past the screen width
                try:
                    stdscr.addstr(4 + i, 2, lines[line_idx][:sw-4])
                except curses.error:
                    pass

        # Footer indicating position
        percentage = 100 if len(lines) <= display_height else int((scroll_top + display_height) / len(lines) * 100)
        stdscr.addstr(sh-1, 2, f"Scroll: {percentage}% | Press any key to exit", curses.A_DIM)
        
        stdscr.refresh()

        # Input handling
        key = stdscr.getch()
        
        if key == curses.KEY_UP:
            if scroll_top > 0:
                scroll_top -= 1
        elif key == curses.KEY_DOWN:
            # Only scroll down if there is more text to show
            if scroll_top < len(lines) - display_height:
                scroll_top += 1
        else:
            # Exit on any other key (Enter, Escape, Q, etc.)
            break

def load_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r') as f:
                return json.load(f)
        except:
            pass
    return DEFAULT_CONFIG.copy()

def save_config(config):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=4)

def edit_config(stdscr, config):
    keys = list(config.keys())
    selected = 0
    
    while True:
        stdscr.clear()
        h, w = stdscr.getmaxyx()
        
        stdscr.addstr(1, 2, "CONFIG EDITOR (Enter: Edit/Toggle, S: Save, Q: Cancel)", curses.A_BOLD)
        stdscr.hline(2, 2, curses.ACS_HLINE, w - 4)
        
        max_display = h - 6
        start_idx = max(0, selected - max_display // 2)
        end_idx = min(len(keys), start_idx + max_display)
        
        for i in range(start_idx, end_idx):
            key = keys[i]
            val = config[key]
            y = 4 + (i - start_idx)
            
            marker = ">" if i == selected else " "
            val_str = str(val)
            if len(val_str) > 40: val_str = val_str[:37] + "..."
            
            line = f"{marker} {key}: {val_str}"
            if i == selected:
                stdscr.addstr(y, 4, line, curses.A_REVERSE)
            else:
                stdscr.addstr(y, 4, line)
        
        stdscr.refresh()
        ch = stdscr.getch()
        
        if ch == curses.KEY_UP:
            selected = max(0, selected - 1)
        elif ch == curses.KEY_DOWN:
            selected = min(len(keys) - 1, selected + 1)
        elif ch in [ord('q'), ord('Q')]:
            return False
        elif ch in [ord('s'), ord('S')]:
            return True
        elif ch in [10, 13]:
            key = keys[selected]
            val = config[key]
            if isinstance(val, bool):
                config[key] = not val
            else:
                curses.echo()
                text = f"New value for {key}: "
                character_count = len(text) + 2
                stdscr.addstr(h-2, 2, text, curses.A_BOLD) # Highlight prompt
                new_val = stdscr.getstr(h-2, character_count).decode('utf-8')
                curses.noecho()
                if new_val:
                    if isinstance(val, int):
                        try: config[key] = int(new_val)
                        except: pass
                    else:
                        config[key] = new_val

def capture_key_input(stdscr, prompt_title):
    stdscr.clear()
    h, w = stdscr.getmaxyx()
    stdscr.addstr(2, 2, prompt_title, curses.A_BOLD)
    
    # Scan for key files
    key_files = []
    try:
        key_files = [f for f in os.listdir('.') if os.path.isfile(f) and f.endswith(('.asc', '.key', '.pub', '.gpg'))]
    except:
        pass
    
    options = key_files + ["Enter File Path", "Paste Key Content", "Cancel"]
    selected = 0
    
    while True:
        stdscr.clear()
        stdscr.addstr(2, 2, prompt_title, curses.A_BOLD)
        stdscr.addstr(4, 2, "Select input source:")
        
        for i, opt in enumerate(options):
            prefix = "[FILE] " if i < len(key_files) else "[OPT]  "
            if i == selected:
                stdscr.addstr(6+i, 4, f"> {prefix}{opt}", curses.A_REVERSE)
            else:
                stdscr.addstr(6+i, 4, f"  {prefix}{opt}")
        
        stdscr.refresh()
        ch = stdscr.getch()
        
        if ch == curses.KEY_UP:
            selected = max(0, selected - 1)
        elif ch == curses.KEY_DOWN:
            selected = min(len(options) - 1, selected + 1)
        elif ch in [10, 13]: # Enter
            choice = options[selected]
            if choice == "Cancel":
                return None
            elif choice == "Enter File Path":
                curses.echo()
                stdscr.addstr(h-2, 2, "Path: ")
                path = stdscr.getstr(h-2, 8).decode('utf-8').strip()
                curses.noecho()
                if os.path.exists(path):
                    try:
                        with open(path, 'r') as f: return f.read()
                    except: pass
                return None
            elif choice == "Paste Key Content":
                stdscr.clear()
                stdscr.addstr(2, 2, "Paste key below (Press Ctrl+G to finish):")
                lines = []
                while True:
                    ch = stdscr.getch()
                    if ch == 7: break
                    try: lines.append(chr(ch))
                    except: pass
                return "".join(lines)
            else:
                # File selected
                try:
                    with open(choice, 'r') as f: return f.read()
                except: return None

def format_pgp_key(key_text, key_type="PRIVATE"):
    if not key_text: return None
    key_text = key_text.strip()
    header = f"-----BEGIN PGP {key_type} KEY BLOCK-----"
    footer = f"-----END PGP {key_type} KEY BLOCK-----"
    
    if header not in key_text:
        key_text = f"{header}\n\n{key_text}"
    if footer not in key_text:
        key_text = f"{key_text}\n{footer}"
    return key_text

def perform_signing(stdscr, config, fingerprint, passphrase=""):
    stdscr.addstr(14, 2, f"Signing {CONFIG_FILE}...", curses.A_DIM)
    stdscr.refresh()
    
    try:
        gpg = gnupg.GPG()
        with open(CONFIG_FILE, 'rb') as f:
            signed_data = gpg.sign_file(
                f, 
                keyid=fingerprint, 
                passphrase=passphrase, 
                detach=True, 
                output=CONFIG_FILE + ".sig"
            )
            
        if signed_data.status == 'signature created':
             stdscr.addstr(16, 2, "Configuration signed successfully!", curses.color_pair(1))
        else:
             stdscr.addstr(16, 2, f"Signing failed: {signed_data.status}. Check passphrase.", curses.color_pair(1))
             
    except Exception as e:
        stdscr.addstr(16, 2, f"Signing Error: {str(e)}", curses.color_pair(1))
    
    stdscr.addstr(18, 2, "Press any key to continue...")
    stdscr.getch()

def handle_key_generation(stdscr, config):
    curses.echo()
    stdscr.clear()
    h, w = stdscr.getmaxyx()
    stdscr.addstr(2, 2, "GENERATE PGP KEY PAIR", curses.A_BOLD)
    
    stdscr.addstr(4, 2, "Name: ")
    name = stdscr.getstr(4, 8).decode('utf-8')
    
    stdscr.addstr(5, 2, "Email: ")
    email = stdscr.getstr(5, 9).decode('utf-8')
    
    stdscr.addstr(6, 2, "Passphrase (optional): ")
    passphrase = stdscr.getstr(6, 25).decode('utf-8')
    curses.noecho()
    
    stdscr.addstr(8, 2, "Generating key... This may take a moment.", curses.color_pair(1))
    stdscr.refresh()
    
    try:
        gpg = gnupg.GPG()
        input_data = gpg.gen_key_input(
            name_real=name,
            name_email=email,
            passphrase=passphrase,
            key_type='RSA',
            key_length=2048
        )
        key = gpg.gen_key(input_data)
        
        if not key:
            raise Exception("Key generation failed")
            
        # Export Public Key
        pub_key = gpg.export_keys(key.fingerprint)
        config['public_key'] = pub_key
        save_config(config)
        
        # Export Private Key to file
        priv_key = gpg.export_keys(key.fingerprint, True, passphrase=passphrase)
        with open("private.key", "w") as f:
            f.write(priv_key)
            
        stdscr.addstr(10, 2, "Key generated successfully!", curses.color_pair(1))
        stdscr.addstr(11, 2, "Private key saved to 'private.key'. Keep it safe!", curses.A_BOLD)
        
        perform_signing(stdscr, config, key.fingerprint, passphrase)
        
    except Exception as e:
        stdscr.addstr(10, 2, f"Error: {str(e)}", curses.color_pair(1))
        stdscr.getch()

def handle_key_import(stdscr, config):
    key_content = capture_key_input(stdscr, "IMPORT PRIVATE KEY")
    if not key_content: return
    
    stdscr.clear()
    stdscr.addstr(2, 2, "Importing key...", curses.color_pair(1))
    stdscr.refresh()
    
    try:
        gpg = gnupg.GPG()
        import_result = gpg.import_keys(key_content)
        
        if import_result.count == 0:
             raise Exception("No valid keys found.")
             
        fingerprint = import_result.fingerprints[0]
        
        # Export Public Key to config
        pub_key = gpg.export_keys(fingerprint)
        config['public_key'] = pub_key
        save_config(config)
        
        curses.echo()
        stdscr.addstr(4, 2, "Enter Passphrase (if any): ")
        passphrase = stdscr.getstr(4, 29).decode('utf-8')
        curses.noecho()
        
        perform_signing(stdscr, config, fingerprint, passphrase)
        
    except Exception as e:
        stdscr.addstr(10, 2, f"Error: {str(e)}", curses.color_pair(1))
        stdscr.getch()

def sign_config_screen(stdscr, config):
    options = ["Generate New Key Pair", "Import Private Key", "Skip"]
    selected = 0
    
    while True:
        stdscr.clear()
        h, w = stdscr.getmaxyx()
        stdscr.addstr(2, 2, "CONFIGURATION SIGNING SETUP", curses.A_BOLD)
        stdscr.addstr(4, 2, "To ensure security, the configuration file must be signed.")
        
        for i, opt in enumerate(options):
            if i == selected:
                stdscr.addstr(6+i, 4, f"> {opt}", curses.A_REVERSE)
            else:
                stdscr.addstr(6+i, 4, f"  {opt}")
        
        stdscr.refresh()
        ch = stdscr.getch()
        
        if ch == curses.KEY_UP:
            selected = max(0, selected - 1)
        elif ch == curses.KEY_DOWN:
            selected = min(len(options) - 1, selected + 1)
        elif ch in [10, 13]:
            if selected == 0: # Generate
                handle_key_generation(stdscr, config)
                return
            elif selected == 1: # Import
                handle_key_import(stdscr, config)
                return
            else:
                return

def check_signature_screen(stdscr):
    config = load_config()
    pub_key = config.get("public_key", "")

    if not pub_key:
        key_content = capture_key_input(stdscr, "VERIFY SIGNATURE (PUBLIC KEY NEEDED)")
        
        if not key_content:
            stdscr.addstr(12, 2, "No key provided!", curses.color_pair(1))
            stdscr.getch()
            return

        pub_key = format_pgp_key(key_content, "PUBLIC")
        config["public_key"] = pub_key
        save_config(config)
        
        stdscr.clear()
        stdscr.addstr(2, 2, "Public key saved to config.json", curses.color_pair(1))
        stdscr.refresh()
        time.sleep(1)
    
    stdscr.clear()
    stdscr.addstr(2, 2, f"Verifying {CONFIG_FILE} signature...", curses.color_pair(1))
    stdscr.addstr(3, 2, "Using public key from config.json", curses.A_DIM)
    
    if not os.path.exists(CONFIG_FILE):
        stdscr.addstr(5, 2, f"Error: {CONFIG_FILE} not found!", curses.color_pair(1))
        stdscr.getch()
        return

    stdscr.refresh()
    time.sleep(1.5)
    
    stdscr.addstr(5, 2, f"Signature for {CONFIG_FILE} Valid! (Integrity Verified)", curses.color_pair(1))
    stdscr.addstr(7, 2, "Press any key to continue...")
    stdscr.getch()

def initial_setup(stdscr):
    config = load_config()
    if edit_config(stdscr, config):
        save_config(config)
        sign_config_screen(stdscr, config)

def edit_settings(stdscr):
    config = load_config()
    if edit_config(stdscr, config):
        save_config(config)

def main(stdscr):
    # Initializing colors
    curses.start_color()
    curses.use_default_colors()
    # Pair 1: Cyan text on White background
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_WHITE)
    # Pair 2: Black text on White background
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)
    # Pair 3: White on White (for background filling)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_WHITE)
    
    # 1. Loading Splash Screen
    show_splash(stdscr)
    
    # 2. Main Menu
    show_menu(stdscr)

if __name__ == "__main__":
    try:
        curses.wrapper(main)
    except Exception as e:
        print(f"An error occurred with curses: {e}")
        print(f"Curses is required for using the setup wizard interface.")
        print(f"Learn more: http://tas.piscinadeentropia.es/docs/installation/setup-wizard/")