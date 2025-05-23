# Multiplayer Game Instructions

> **Note**: A better README will come once I learn Markdown—thanks for your patience!

## How to Use

1. **Start the Server (Host):**
   - Run `main.py`.
   - Type `host` when prompted.
   - Enter your **local IP address** and a **port number** to host the server.

2. **Clients Connect:**
   - Your friends should also run `main.py`.
   - Type `connect` when prompted.
   - Enter the **host’s public IP address** (or local IP if on the same LAN) and the **same port number**.

3. **Host Must Also Connect:**
   - The host should open another terminal window.
   - Run `main.py`, select `connect`, and connect to their own server using the **same local IP and port**.

4. **Start the Game:**
   - Once everyone is connected, go back to the **host terminal window**.
   - Type `start` to begin the game (it will be prompting for input).

## Important Notes

- **Don't disconnect during the game.**
- All players need to be connected **before** the host starts the game.

---

Thanks for trying this out!