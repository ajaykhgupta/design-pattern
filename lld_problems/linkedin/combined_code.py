from typing import List, Optional

# ---------- Domain ----------

class UserProfile:
    def __init__(
        self,
        name: str,
        headline: str = "",
        summary: str = "",
        picture: Optional[str] = None,
        experience: Optional[List[str]] = None,
        education: Optional[List[str]] = None,
        skills: Optional[List[str]] = None,
    ):
        self.name = name
        self.headline = headline
        self.summary = summary
        self.picture = picture
        self.experience = experience or []
        self.education = education or []
        self.skills = skills or []

    def update(self, **kwargs):
        for k, v in kwargs.items():
            if hasattr(self, k):
                setattr(self, k, v)

    def __repr__(self):
        return f"UserProfile(name={self.name!r}, headline={self.headline!r})"


class Notification:
    def __init__(self, recipient: "Account", message: str):
        self.recipient = recipient
        self.message = message

    def __repr__(self):
        return f"Notification(to={self.recipient.profile.name}, msg={self.message!r})"


class NotificationService:
    def __init__(self):
        self.notifications: List[Notification] = []

    def notify(self, recipient: "Account", message: str):
        note = Notification(recipient, message)
        self.notifications.append(note)
        recipient.notifications.append(note)
        print(f"[NOTIFY] {recipient.profile.name} → {message}")

    def get_user_notifications(self, user: "Account") -> List[Notification]:
        return user.notifications


class Account:
    def __init__(self, name: str, email: str, password: str):
        self.id = id(self)
        self.email = email
        self.password = password  # Plaintext for demo only!
        self.logged_in = False
        self.profile = UserProfile(name=name)
        self.inbox: List["Message"] = []  # message received
        self.sent: List["Message"] = []
        self.notifications: List[Notification] = []

    def login(self, password: str) -> bool:
        if self.password == password:
            self.logged_in = True
            print(f"[LOGIN] {self.profile.name} logged in")
            return True
        print(f"[LOGIN FAILED] Wrong password for {self.profile.name}")
        return False

    def logout(self):
        if self.logged_in:
            self.logged_in = False
            print(f"[LOGOUT] {self.profile.name} logged out")
        else:
            print(f"[LOGOUT FAILED] {self.profile.name} is not logged in")

    def __repr__(self):
        return f"Account({self.profile.name})"


class Connection:
    def __init__(self, requester: Account, receiver: Account, status: str = "pending"):
        self.requester = requester
        self.receiver = receiver
        self.status = status  # "pending" | "accepted" | "rejected"

    def __repr__(self):
        return f"Connection({self.requester.profile.name} -> {self.receiver.profile.name}, {self.status})"


class ConnectionService:
    def __init__(self, notifier: NotificationService):
        self.connections: List[Connection] = []
        self.notifier = notifier

    def _between(self, a: Account, b: Account):
        for c in self.connections:
            if (c.requester == a and c.receiver == b) or (c.requester == b and c.receiver == a):
                return c
        return None

    def send_request(self, requester: Account, receiver: Account):
        if not requester.logged_in:
            print(f"[ERROR] {requester.profile.name} must log in to send requests")
            return
        if requester == receiver:
            print("[ERROR] Cannot connect to yourself")
            return
        existing = self._between(requester, receiver)
        if existing:
            print(f"[INFO] Connection already exists: {existing}")
            return
        c = Connection(requester, receiver, "pending")
        self.connections.append(c)
        print(f"[SEND] {requester.profile.name} → {receiver.profile.name}")
        self.notifier.notify(receiver, f"{requester.profile.name} sent you a connection request")

    def accept_request(self, receiver: Account, requester: Account):
        c = next((c for c in self.connections
                  if c.requester == requester and c.receiver == receiver and c.status == "pending"), None)
        if not c:
            print(f"[WARN] No pending request from {requester.profile.name} to {receiver.profile.name}")
            return
        c.status = "accepted"
        print(f"[ACCEPT] {receiver.profile.name} accepted {requester.profile.name}")
        self.notifier.notify(requester, f"{receiver.profile.name} accepted your connection request")

    def reject_request(self, receiver: Account, requester: Account):
        c = next((c for c in self.connections
                  if c.requester == requester and c.receiver == receiver and c.status == "pending"), None)
        if not c:
            print(f"[WARN] No pending request from {requester.profile.name} to {receiver.profile.name}")
            return
        c.status = "rejected"
        print(f"[REJECT] {receiver.profile.name} rejected {requester.profile.name}")
        self.notifier.notify(requester, f"{receiver.profile.name} rejected your connection request")

    def get_user_connections(self, user: Account) -> List[Account]:
        result = []
        for c in self.connections:
            if c.status == "accepted":
                if c.requester == user:
                    result.append(c.receiver)
                elif c.receiver == user:
                    result.append(c.requester)
        return result

    def get_pending_requests_for(self, user: Account) -> List[Account]:
        return [c.requester for c in self.connections if c.receiver == user and c.status == "pending"]

    def are_connected(self, a: Account, b: Account) -> bool:
        c = self._between(a, b)
        return c is not None and c.status == "accepted"


class Message:
    def __init__(self, sender: Account, receiver: Account, content: str):
        self.sender = sender
        self.receiver = receiver
        self.content = content

    def __repr__(self):
        return f"Message(from={self.sender.profile.name}, to={self.receiver.profile.name}, content={self.content!r})"


class MessagingService:
    def __init__(self, connection_service: ConnectionService, notifier: NotificationService):
        self.connection_service = connection_service
        self.notifier = notifier

    def send_message(self, sender: Account, receiver: Account, content: str):
        if not sender.logged_in:
            print(f"[ERROR] {sender.profile.name} must log in to send messages")
            return
        if not self.connection_service.are_connected(sender, receiver):
            print(f"[ERROR] {sender.profile.name} and {receiver.profile.name} are not connected")
            return
        msg = Message(sender, receiver, content)
        sender.sent.append(msg)
        receiver.inbox.append(msg)
        print(f"[MESSAGE SENT] {sender.profile.name} → {receiver.profile.name}: {content}")
        self.notifier.notify(receiver, f"New message from {sender.profile.name}: {content}")


class AccountService:
    def __init__(self):
        self.accounts: List[Account] = []

    def register(self, name: str, email: str, password: str) -> Account:
        acc = Account(name, email, password)
        self.accounts.append(acc)
        print(f"[REGISTER] Account created for {name}")
        return acc


class JobPosting:
    def __init__(self, title: str, description: str, requirements: List[str], location: str, company: "Company"):
        self.title = title
        self.description = description
        self.requirements = requirements
        self.location = location
        self.company = company

    def __repr__(self):
        return f"JobPosting({self.title} at {self.company.name})"


class Company:
    def __init__(self, name: str, industry: str):
        self.name = name
        self.industry = industry

    def __repr__(self):
        return f"Company({self.name}, {self.industry})"


class JobService:
    def __init__(self, notifier: NotificationService):
        self.jobs: List[JobPosting] = []
        self.notifier = notifier

    def post_job(self, job: JobPosting, audience: List[Account]):
        self.jobs.append(job)
        print(f"[JOB POSTED] {job.title} at {job.company.name}")
        # Notify all users (simple demo: broadcast to audience)
        for user in audience:
            self.notifier.notify(user, f"New job posted: {job.title} at {job.company.name}")


class SearchService:
    @staticmethod
    def search_users(users: List[Account], keyword: str) -> List[Account]:
        results = [(u, SearchService._rank_text(f"{u.profile.name} {u.profile.headline}", keyword))
                   for u in users]
        return [u for u, score in sorted(results, key=lambda x: x[1], reverse=True) if score > 0]

    @staticmethod
    def search_companies(companies: List[Company], keyword: str) -> List[Company]:
        results = [(c, SearchService._rank_text(f"{c.name} {c.industry}", keyword))
                   for c in companies]
        return [c for c, score in sorted(results, key=lambda x: x[1], reverse=True) if score > 0]

    @staticmethod
    def search_jobs(jobs: List[JobPosting], keyword: str) -> List[JobPosting]:
        results = [(j, SearchService._rank_text(f"{j.title} {j.description} {j.location}", keyword))
                   for j in jobs]
        return [j for j, score in sorted(results, key=lambda x: x[1], reverse=True) if score > 0]

    @staticmethod
    def _rank_text(text: str, keyword: str) -> int:
        return text.lower().count(keyword.lower())

# # ---------- Demo Flow ----------

# # main 1
# accounts = AccountService()
# connections = ConnectionService()
# messaging = MessagingService(connections)

# # Register users
# A = accounts.register("A", "a@example.com", "1234")
# B = accounts.register("B", "b@example.com", "1234")
# C = accounts.register("C", "c@example.com", "1234")
# D = accounts.register("D", "d@example.com", "1234")

# # Login users
# A.login("1234")
# B.login("1234")
# C.login("1234")
# D.login("1234")

# # Send connection requests to B
# connections.send_request(A, B)
# connections.send_request(C, B)
# connections.send_request(D, B)

# # B accepts A and C, rejects D
# connections.accept_request(B, A)
# connections.accept_request(B, C)
# connections.reject_request(B, D)

# # Messaging between connected users
# messaging.send_message(A, B, "Hey B, how are you?")
# messaging.send_message(B, A, "I’m good, thanks!")
# messaging.send_message(C, B, "Hi B, long time no see!")

# # Trying to message without connection
# messaging.send_message(D, B, "Hello?")  # Should fail

# # View inbox/sent for B
# print("[B's inbox]", messaging.view_inbox(B))
# print("[B's sent]", messaging.view_sent(B))

# # Companies
# company1 = Company("TechCorp", "Software")
# company2 = Company("DataX", "Analytics")

# # Jobs
# job1 = JobPosting("Backend Developer", "Work on APIs", ["Python"], "NY", company1)
# job2 = JobPosting("Data Engineer", "Build pipelines", ["SQL"], "SF", company2)

# # Search Examples
# print("Search Users:", SearchService.search_users(accounts.accounts, "developer"))
# print("Search Companies:", SearchService.search_companies([company1, company2], "software"))
# print("Search Jobs:", SearchService.search_jobs([job1, job2], "python"))



# main 2

# ---------- Demo Flow ----------

notifier = NotificationService()
accounts = AccountService()
connections = ConnectionService(notifier)
messaging = MessagingService(connections, notifier)
jobs = JobService(notifier)

# Register users
A = accounts.register("A", "a@example.com", "1234")
B = accounts.register("B", "b@example.com", "1234")
C = accounts.register("C", "c@example.com", "1234")
D = accounts.register("D", "d@example.com", "1234")

# Login users
A.login("1234")
B.login("1234")
C.login("1234")
D.login("1234")

# Send connection requests to B
connections.send_request(A, B)


connections.send_request(C, B)
connections.send_request(D, B)

# B accepts A and C, rejects D
connections.accept_request(B, A)
connections.accept_request(B, C)
connections.reject_request(B, D)

# Messaging between connected users
messaging.send_message(A, B, "Hey B, how are you?")
messaging.send_message(B, A, "I’m good, thanks!")
messaging.send_message(C, B, "Hi B, long time no see!")

# Trying to message without connection
messaging.send_message(D, B, "Hello?")  # Should fail

# Companies and Jobs
company1 = Company("TechCorp", "Software")
job1 = JobPosting("Backend Developer", "Work on APIs", ["Python"], "NY", company1)
jobs.post_job(job1, accounts.accounts)  # notify all users

# View notifications for B
print("[B's notifications]", notifier.get_user_notifications(B))