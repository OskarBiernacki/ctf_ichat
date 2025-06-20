# CTF IChat

Messenger-like chat, vulnerable to attacks. It is known for its large number of scammers who spam users. Are you able to access the admin secret?

CTF IChat — a fun and interactive chat application designed specifically for Capture The Flag (CTF) challenges. This project includes a variety of bot users with humorous and obvious scam messages to make the experience more engaging — but beware, there's more going on under the hood than meets the eye.

## Features

- User registration and login
- Real-time chat with other users (yes, there's an easter egg!)
- Bot users with funny and scammy messages
- Admin bot that reads user messages
- Hidden vulnerabilities for CTF-style exploitation

## Installation

This application requires **Docker Compose** to run. If you have it installed, just run:

```bash
docker compose up
```
The application will start and listen by default on port `5000`.
Visit http://localhost:5000 in your browser to start.

If you want to change the port, edit `docker-compose.yaml` 

## Bots
The project includes a colorful cast of bot users with obviously scammy and funny messages. Some examples:
* PrinceNigerian: "Greetings! I am a Nigerian prince in need of your help to transfer $10 million. Please send your bank details."
* CryptoKing: "Invest in my new cryptocurrency and double your money overnight! Just send 1 BTC to my wallet."
* LotteryLover: "Congratulations! You've won the international lottery! Claim your $1 million prize by sending a $100 processing fee."

* RichUncle: "Hello! I am your long-lost rich uncle. I need your help to unlock my inheritance. Please send $500 for legal fees."
* FakeGuru: "Join my exclusive investment club and become a millionaire! Just pay a $200 membership fee."

Each bot adds character to the app — and some may even help (or distract) you in your exploit attempts.


## Spoiler Details
- Register a new user or log in with an existing account.
- Join the chat and interact with both real users and bots.\
- Explore the intentionally vulnerable environment.
- Look out for hidden flags through:
    * Stored XSS attacks
    * JWT token cracking

Yes — spoiler alert — the app contains vulnerabilities! If you're curious or want a head start:

- There's a JWT token used for authentication... but it's not as secure as it looks.
- The admin bot executes JavaScript using a headless Chrome driver, simulating a real browser. This makes stored XSS attacks not only possible but also practical for stealing tokens or triggering unintended behavior — just like in real-world scenarios.


## Authors
This CTF was created by Oskar Biernacki for CTF_PJATK_2025.